import pandas as pd
from .engine import Engine
from .session import Session
from .schema import Table, Column

def infer_schema_from_dataframe(df, table_name):
    """Infer SQL schema from a pandas DataFrame."""
    from .utils import DTYPE_MAPPING
    
    columns = []
    for col_name, dtype in df.dtypes.items():
        dtype_name = dtype.name if hasattr(dtype, 'name') else str(dtype)
        
        # Handle text fields that might be longer than VARCHAR(255)
        if dtype_name == "object" and df[col_name].notna().any():
            length = df[col_name].str.len().max() if hasattr(df[col_name], 'str') else 0
            if length and length > 255:
                dtype_name = "text"
                
        sql_type = DTYPE_MAPPING.get(dtype_name, 'VARCHAR(255)')
        columns.append(f"{col_name} {sql_type}")
    
    create_query = f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(columns) + "\n)"
    return create_query

def _insert_dataframe_to_table(df, table_name, session):
    """Insert a DataFrame into an existing table."""
    # Generate column list
    columns = df.columns.tolist()
    columns_str = ', '.join(columns)
    
    # Generate placeholders
    placeholders = ', '.join(['?' for _ in columns])
    
    # Prepare insert query
    insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
    # Execute in batches
    with session.begin():
        for _, row in df.iterrows():
            session.execute(insert_query, tuple(row))

def transfer_csv(
    csv_file,
    table_name,
    engine=None,
    if_exists='fail',
    chunk_size=None,
    **pandas_kwargs
):
    """
    Transfer data from CSV to SQL database.
    
    Parameters:
    -----------
    csv_file : str
        Path to the CSV file
    table_name : str
        Name of the target SQL table
    engine : Engine, optional
        Database engine to use. If None, creates one from environment variables.
    if_exists : str
        How to behave if the table already exists: 'fail', 'replace', or 'append'
    chunk_size : int, optional
        If set, read the file in chunks of specified size
    pandas_kwargs : dict
        Additional keyword arguments for pd.read_csv()
    """
    engine = engine or Engine.from_env()
    
    with Session(engine) as session:
        # Check if table exists
        exists_query = f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
        try:
            result = session.execute(exists_query).fetchone()
            table_exists = result[0] > 0
        except:
            # If information_schema query fails, try direct query
            try:
                session.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
                table_exists = True
            except:
                table_exists = False
        
        if table_exists:
            if if_exists == 'fail':
                raise ValueError(f"Table '{table_name}' already exists")
            elif if_exists == 'replace':
                session.execute(f"DROP TABLE {table_name}")
                table_exists = False
        
        # Process in chunks if specified
        if chunk_size:
            # Read first chunk to infer schema
            first_chunk = pd.read_csv(csv_file, nrows=1, **pandas_kwargs)
            
            if not table_exists:
                # Create table from schema
                create_query = infer_schema_from_dataframe(first_chunk, table_name)
                session.execute(create_query)
                session.commit()
            
            # Process in chunks
            for chunk in pd.read_csv(csv_file, chunksize=chunk_size, **pandas_kwargs):
                _insert_dataframe_to_table(chunk, table_name, session)
        else:
            # Read entire file
            df = pd.read_csv(csv_file, **pandas_kwargs)
            
            if not table_exists:
                # Create table from schema
                create_query = infer_schema_from_dataframe(df, table_name)
                session.execute(create_query)
                session.commit()
            
            # Insert all data
            _insert_dataframe_to_table(df, table_name, session)
