from .utils import DTYPE_MAPPING

class Column:
    """Represents a database column."""
    
    def __init__(self, type_=None, primary_key=False, nullable=True, 
                 unique=False, default=None, autoincrement=False):
        self.type = type_
        self.primary_key = primary_key
        self.nullable = nullable
        self.unique = unique
        self.default = default
        self.autoincrement = autoincrement
        self.name = None
        
    def __set_name__(self, owner, name):
        self.name = name


class TableBase:
    """Base class for all table definitions."""
    
    @classmethod
    def __init_subclass__(cls):
        cls.__tablename__ = getattr(cls, '__tablename__', cls.__name__.lower())
        cls._columns = {}
        
        for name, attr in cls.__dict__.items():
            if isinstance(attr, Column):
                attr.__set_name__(cls, name)
                cls._columns[name] = attr
    
    @classmethod
    def create(cls, session):
        """Create this table in the database."""
        columns = []
        for name, column in cls._columns.items():
            type_name = column.type.__name__ if hasattr(column.type, '__name__') else str(column.type)
            sql_type = DTYPE_MAPPING.get(type_name, 'VARCHAR(255)')
            nullable = "NOT NULL" if not column.nullable else "NULL"
            pk = "PRIMARY KEY" if column.primary_key else ""
            autoinc = "AUTO_INCREMENT" if column.autoincrement else ""
            unique = "UNIQUE" if column.unique else ""
            
            columns.append(f"{name} {sql_type} {nullable} {pk} {autoinc} {unique}".strip())
        
        create_sql = f"CREATE TABLE IF NOT EXISTS {cls.__tablename__} (\n  " + ",\n  ".join(columns) + "\n)"
        session.execute(create_sql)
        session.commit()
        return True
    
    @classmethod
    def drop(cls, session):
        """Drop this table from the database."""
        drop_sql = f"DROP TABLE IF EXISTS {cls.__tablename__}"
        session.execute(drop_sql)
        session.commit()
        return True
        
    @classmethod
    def table_exists(cls, session):
        """Check if this table exists in the database."""
        try:
            session.execute(f"SELECT 1 FROM {cls.__tablename__} LIMIT 1")
            return True
        except Exception:
            return False

# Create a base class for declarative table definitions
Table = TableBase
