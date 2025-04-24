from contextlib import contextmanager

class Session:
    """Manages database operations and transactions."""
    
    def __init__(self, engine):
        self.engine = engine
        self._connection = None
        self._cursor = None
        self._transaction_level = 0
    
    def __enter__(self):
        self._connection = self.engine.connect()
        self._cursor = self._connection.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()
            self._connection = None
        
    def execute(self, query, params=None):
        """Execute a raw SQL query."""
        if params:
            self._cursor.execute(query, params)
        else:
            self._cursor.execute(query)
        return self._cursor
    
    def fetchall(self):
        """Fetch all results from the last query."""
        return self._cursor.fetchall()
    
    def fetchone(self):
        """Fetch one result from the last query."""
        return self._cursor.fetchone()
    
    @contextmanager
    def begin(self):
        """Begin a transaction."""
        self._transaction_level += 1
        if self._transaction_level == 1:
            self._connection.autocommit = False
        try:
            yield self
            if self._transaction_level == 1:
                self._connection.commit()
        except Exception:
            if self._transaction_level == 1:
                self._connection.rollback()
            raise
        finally:
            self._transaction_level -= 1
            if self._transaction_level == 0:
                self._connection.autocommit = True
    
    def commit(self):
        """Commit the current transaction."""
        self._connection.commit()
    
    def rollback(self):
        """Roll back the current transaction."""
        self._connection.rollback()
        
    def executemany(self, query, params_seq):
        """Execute a query with multiple parameter sets."""
        self._cursor.executemany(query, params_seq)
        return self._cursor
