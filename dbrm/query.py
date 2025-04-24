class Select:
    """Builds SELECT queries in a fluent interface style."""
    
    def __init__(self, *columns):
        self.columns = columns or ["*"]
        self.from_table = None
        self.where_clauses = []
        self.order_by_columns = []
        self.limit_count = None
        self.offset_count = None
        self.group_by_columns = []
        self.having_clauses = []
        self.join_clauses = []
    
    def from_(self, table):
        """Specify the FROM table."""
        if hasattr(table, '__tablename__'):
            self.from_table = table.__tablename__
        else:
            self.from_table = table
        return self
    
    def where(self, condition):
        """Add a WHERE condition."""
        self.where_clauses.append(condition)
        return self
    
    def order_by(self, *columns):
        """Add ORDER BY columns."""
        self.order_by_columns.extend(columns)
        return self
    
    def limit(self, count):
        """Set the LIMIT count."""
        self.limit_count = count
        return self
    
    def offset(self, count):
        """Set the OFFSET count."""
        self.offset_count = count
        return self
    
    def group_by(self, *columns):
        """Add GROUP BY columns."""
        self.group_by_columns.extend(columns)
        return self
    
    def having(self, condition):
        """Add a HAVING condition."""
        self.having_clauses.append(condition)
        return self
    
    def join(self, table, condition, join_type="INNER"):
        """Add a JOIN clause."""
        if hasattr(table, '__tablename__'):
            table_name = table.__tablename__
        else:
            table_name = table
        self.join_clauses.append((join_type, table_name, condition))
        return self
    
    def build(self):
        """Build the SQL query string."""
        if not self.from_table:
            raise ValueError("No FROM table specified")
        
        columns = ", ".join(str(col) for col in self.columns)
        sql = f"SELECT {columns} FROM {self.from_table}"
        
        # Add JOIN clauses
        for join_type, table, condition in self.join_clauses:
            sql += f" {join_type} JOIN {table} ON {condition}"
        
        # Add WHERE clauses
        if self.where_clauses:
            sql += " WHERE " + " AND ".join(self.where_clauses)
        
        # Add GROUP BY
        if self.group_by_columns:
            sql += " GROUP BY " + ", ".join(self.group_by_columns)
        
        # Add HAVING
        if self.having_clauses:
            sql += " HAVING " + " AND ".join(self.having_clauses)
        
        # Add ORDER BY
        if self.order_by_columns:
            sql += " ORDER BY " + ", ".join(self.order_by_columns)
        
        # Add LIMIT and OFFSET
        if self.limit_count is not None:
            sql += f" LIMIT {self.limit_count}"
        
        if self.offset_count is not None:
            sql += f" OFFSET {self.offset_count}"
        
        return sql
    
    def execute(self, session):
        """Execute this query using the provided session."""
        return session.execute(self.build())


class Insert:
    """Builds INSERT queries."""
    
    def __init__(self, table):
        if hasattr(table, '__tablename__'):
            self.table = table.__tablename__
        else:
            self.table = table
        self._values = {}
    
    def values(self, **kwargs):
        """Set the values to insert."""
        self._values.update(kwargs)
        return self
    
    def build(self):
        """Build the SQL query string."""
        columns = ", ".join(self._values.keys())
        placeholders = ", ".join(["?" for _ in self._values])
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        params = list(self._values.values())
        return sql, params
    
    def execute(self, session):
        """Execute this query using the provided session."""
        sql, params = self.build()
        return session.execute(sql, params)


class Update:
    """Builds UPDATE queries."""
    
    def __init__(self, table):
        if hasattr(table, '__tablename__'):
            self.table = table.__tablename__
        else:
            self.table = table
        self.set_values = {}
        self.where_clauses = []
    
    def set(self, **kwargs):
        """Set the values to update."""
        self.set_values.update(kwargs)
        return self
    
    def where(self, condition):
        """Add a WHERE condition."""
        self.where_clauses.append(condition)
        return self
    
    def build(self):
        """Build the SQL query string."""
        set_clause = ", ".join([f"{k} = ?" for k in self.set_values.keys()])
        sql = f"UPDATE {self.table} SET {set_clause}"
        
        params = list(self.set_values.values())
        
        if self.where_clauses:
            sql += " WHERE " + " AND ".join(self.where_clauses)
        
        return sql, params
    
    def execute(self, session):
        """Execute this query using the provided session."""
        sql, params = self.build()
        return session.execute(sql, params)


class Delete:
    """Builds DELETE queries."""
    
    def __init__(self, table):
        if hasattr(table, '__tablename__'):
            self.table = table.__tablename__
        else:
            self.table = table
        self.where_clauses = []
    
    def where(self, condition):
        """Add a WHERE condition."""
        self.where_clauses.append(condition)
        return self
    
    def build(self):
        """Build the SQL query string."""
        sql = f"DELETE FROM {self.table}"
        
        if self.where_clauses:
            sql += " WHERE " + " AND ".join(self.where_clauses)
        
        return sql
    
    def execute(self, session):
        """Execute this query using the provided session."""
        return session.execute(self.build())
