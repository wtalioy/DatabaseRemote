import unittest
from dbrm import Select, Insert, Update, Delete, Engine, Session, Table, Column, Integer, String

class TestQueryBuilder(unittest.TestCase):
    
    def test_select_query(self):
        # Test basic select
        query = Select("name", "age").from_("employees").where("age > 30")
        expected = "SELECT name, age FROM employees WHERE age > 30"
        self.assertEqual(query.build(), expected)
        
        # Test with multiple conditions
        query = Select("id", "name").from_("employees").where("age > 30").where("salary < 50000")
        expected = "SELECT id, name FROM employees WHERE age > 30 AND salary < 50000"
        self.assertEqual(query.build(), expected)
        
        # Test with order by
        query = Select("*").from_("employees").order_by("age")
        expected = "SELECT * FROM employees ORDER BY age"
        self.assertEqual(query.build(), expected)
        
        # Test with limit and offset
        query = Select("*").from_("employees").limit(10).offset(5)
        expected = "SELECT * FROM employees LIMIT 10 OFFSET 5"
        self.assertEqual(query.build(), expected)
        
        # Test with group by and having
        query = Select("department", "AVG(salary)").from_("employees").group_by("department").having("AVG(salary) > 50000")
        expected = "SELECT department, AVG(salary) FROM employees GROUP BY department HAVING AVG(salary) > 50000"
        self.assertEqual(query.build(), expected)
        
    def test_join_query(self):
        query = Select("e.name", "d.department_name").from_("employees e").join(
            "departments d", "e.dept_id = d.id"
        )
        expected = "SELECT e.name, d.department_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id"
        self.assertEqual(query.build(), expected)
    
    def test_insert_query(self):
        # Test insert with values
        insert = Insert("employees")
        insert._values = {"id": 1, "name": "John", "age": 30}  # Direct access for testing
        sql, params = insert.build()
        
        expected_sql = "INSERT INTO employees (id, name, age) VALUES (?, ?, ?)"
        expected_params = [1, "John", 30]
        
        self.assertEqual(sql, expected_sql)
        self.assertEqual(params, expected_params)
    
    def test_update_query(self):
        # Test update with values
        update = Update("employees").set(name="John", age=35).where("id = 1")
        sql, params = update.build()
        
        # Note: Since dictionaries don't guarantee order, we'll check parts of the query
        self.assertIn("UPDATE employees SET", sql)
        self.assertIn("name = ?", sql)
        self.assertIn("age = ?", sql)
        self.assertIn("WHERE id = 1", sql)
        
        # Check parameters (could be in any order based on dict iteration)
        self.assertEqual(set(params), {"John", 35})
    
    def test_delete_query(self):
        # Test delete
        delete = Delete("employees").where("id = 1")
        expected = "DELETE FROM employees WHERE id = 1"
        self.assertEqual(delete.build(), expected)
        
        # Test delete with multiple conditions
        delete = Delete("employees").where("age > 60").where("department = 'HR'")
        expected = "DELETE FROM employees WHERE age > 60 AND department = 'HR'"
        self.assertEqual(delete.build(), expected)

class TestTableDefinition(unittest.TestCase):
    def setUp(self):
        # Define a simple test table
        class TestEmployee(Table):
            __tablename__ = 'test_employees'
            id = Column(Integer, primary_key=True)
            name = Column(String, nullable=False)
            age = Column(Integer)
            
        self.TestEmployee = TestEmployee
        
    def test_table_definition(self):
        # Check table attributes
        self.assertEqual(self.TestEmployee.__tablename__, 'test_employees')
        self.assertTrue('id' in self.TestEmployee._columns)
        self.assertTrue('name' in self.TestEmployee._columns)
        self.assertTrue('age' in self.TestEmployee._columns)
        
        # Check column properties
        id_col = self.TestEmployee._columns['id']
        self.assertEqual(id_col.type, Integer)
        self.assertTrue(id_col.primary_key)
        
        name_col = self.TestEmployee._columns['name']
        self.assertEqual(name_col.type, String)
        self.assertFalse(name_col.nullable)

if __name__ == '__main__':
    unittest.main()
