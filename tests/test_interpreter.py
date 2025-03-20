from dbrm.sqlinterpreter import *
import unittest


class TestSQLInterpreter(unittest.TestCase):
    
    def test_create_table(self):
        # Test basic table creation
        column_info = (
            ('id', 'int', None),
            ('name', 'object', 50),
            ('age', 'int', None),
            ('salary', 'float', None)
        )
        expected = "CREATE TABLE employees (id INTEGER, name VARCHAR(50), age INTEGER, salary FLOAT)"
        self.assertEqual(create_table('employees', column_info), expected)
        
        # Test with invalid data type
        with self.assertRaises(ValueError):
            create_table('employees', (('id', 'invalid_type', None),))
    
    def test_drop_table(self):
        expected = "DROP TABLE employees"
        self.assertEqual(drop_table('employees'), expected)

    def test_where(self):
        # Test with string condition
        expected = "WHERE age > 30"
        self.assertEqual(where('age > 30'), expected)
        
        # Test with tuple conditions
        expected = "WHERE age > 30 AND salary < 50000"
        self.assertEqual(where(('age > 30', 'salary < 50000')), expected)
    
    def test_select(self):
        # Test with string arguments
        expected = "SELECT name, age FROM employees WHERE age > 30"
        self.assertEqual(select('name, age', 'employees', 'age > 30'), expected)
        
        # Test with tuple arguments
        expected = "SELECT id, name FROM employees WHERE age > 30 AND salary < 50000"
        self.assertEqual(select(('id', 'name'), 'employees', ('age > 30', 'salary < 50000')), expected)
    
    def test_insert(self):
        # Test with string columns and single value
        expected = "INSERT INTO employees (id) VALUES (1)"
        self.assertEqual(insert('employees', 'id', 1), expected)
        
        # Test with tuple columns and values
        expected = "INSERT INTO employees (id, name, age) VALUES (1, 'John', 30)"
        self.assertEqual(insert('employees', ('id', 'name', 'age'), (1, 'John', 30)), expected)
        
        # Test with mismatched columns and values
        with self.assertRaises(ValueError):
            insert('employees', ('id', 'name'), (1,))
    
    def test_update(self):
        # Test with string columns and single value
        expected = "UPDATE employees SET salary = 50000 WHERE id = 1"
        self.assertEqual(update('employees', 'salary', 50000, ('id = 1')), expected)
        
        # Test with tuple columns and values
        expected = "UPDATE employees SET name = 'John', age = 35 WHERE id = 1 AND department = 'IT'"
        self.assertEqual(update('employees', ('name', 'age'), ('John', 35), ('id = 1', "department = 'IT'")), expected)
        
        # Test with mismatched columns and values
        with self.assertRaises(ValueError):
            update('employees', ('name', 'age'), (30,), 'id = 1')
    
    def test_delete(self):
        # Test with string condition
        expected = "DELETE FROM employees WHERE id = 1"
        self.assertEqual(delete('employees', 'id = 1'), expected)
        
        # Test with tuple conditions
        expected = "DELETE FROM employees WHERE age > 60 AND department = 'HR'"
        self.assertEqual(delete('employees', 'age > 60 AND department = \'HR\''), expected)
    
    def test_like(self):
        expected = "LIKE '%Smith%'"
        self.assertEqual(like('%Smith%'), expected)
    
    def test_union(self):
        query1 = "SELECT * FROM employees WHERE department = 'IT'"
        query2 = "SELECT * FROM contractors WHERE department = 'IT'"
        expected = "SELECT * FROM employees WHERE department = 'IT' UNION SELECT * FROM contractors WHERE department = 'IT'"
        self.assertEqual(union(query1, query2), expected)
    
    def test_order_by(self):
        # Test ascending order (default)
        expected = "ORDER BY age ASC"
        self.assertEqual(order_by('age'), expected)
        
        # Test descending order
        expected = "ORDER BY salary DESC"
        self.assertEqual(order_by('salary', ascending=False), expected)
    
    def test_group_by(self):
        # Test with string column
        expected = "GROUP BY department"
        self.assertEqual(group_by('department'), expected)
        
        # Test with tuple columns
        expected = "GROUP BY department, job_title"
        self.assertEqual(group_by(('department', 'job_title')), expected)
    
    def test_join(self):
        # Test inner join (default)
        expected = "SELECT * FROM employees INNER JOIN departments ON employees.dept_id = departments.id"
        self.assertEqual(select('*', join('employees', 'departments', 'INNER', 'employees.dept_id = departments.id')), expected)
        
        # Test left join
        expected = "SELECT * FROM employees LEFT JOIN departments ON employees.dept_id = departments.id"
        self.assertEqual(select('*', join('employees', 'departments', 'LEFT', 'employees.dept_id = departments.id')), expected)
        
        # Test with multiple conditions
        expected = "SELECT * FROM employees INNER JOIN departments ON employees.dept_id = departments.id AND employees.location = departments.location"
        self.assertEqual(select('*', join('employees', 'departments', 'INNER', ('employees.dept_id = departments.id', 'employees.location = departments.location'))), expected)
        
        # Test with invalid join type
        with self.assertRaises(ValueError):
            join('employees', 'departments', 'INVALID', 'employees.dept_id = departments.id')
    
    def test_add_column(self):
        expected = "ALTER TABLE employees ADD COLUMN email VARCHAR"
        self.assertEqual(add_column('employees', 'email', 'object'), expected)
        
        # Test with invalid data type
        with self.assertRaises(ValueError):
            add_column('employees', 'score', 'invalid_type')
    
    def test_drop_column(self):
        expected = "ALTER TABLE employees DROP COLUMN email"
        self.assertEqual(drop_column('employees', 'email'), expected)
    
    def test_modify_column(self):
        expected = "ALTER TABLE employees MODIFY COLUMN salary FLOAT"
        self.assertEqual(modify_column('employees', 'salary', 'float'), expected)
        
        # Test with invalid data type
        with self.assertRaises(ValueError):
            modify_column('employees', 'salary', 'invalid_type')
    
    def test_rename_column(self):
        expected = "ALTER TABLE employees CHANGE COLUMN old_name new_name INTEGER"
        self.assertEqual(rename_column('employees', 'old_name', 'new_name', 'int'), expected)
        
        # Test with invalid data type
        with self.assertRaises(ValueError):
            rename_column('employees', 'old_name', 'new_name', 'invalid_type')
    
    def test_add_primary_key(self):
        # Test with string column
        expected = "ALTER TABLE employees ADD PRIMARY KEY (id)"
        self.assertEqual(add_primary_key('employees', 'id'), expected)
        
        # Test with tuple columns
        expected = "ALTER TABLE employees ADD PRIMARY KEY (id, dept_id)"
        self.assertEqual(add_primary_key('employees', ('id', 'dept_id')), expected)
    
    def test_add_foreign_key(self):
        expected = "ALTER TABLE employees ADD FOREIGN KEY (dept_id) REFERENCES departments (id)"
        self.assertEqual(add_foreign_key('employees', 'dept_id', 'departments', 'id'), expected)
    
    def test_rename_table(self):
        expected = "ALTER TABLE employees RENAME TO staff"
        self.assertEqual(rename_table('employees', 'staff'), expected)
    
    def test_create_database(self):
        expected = "CREATE DATABASE company"
        self.assertEqual(create_database('company'), expected)
    
    def test_drop_database(self):
        expected = "DROP DATABASE company"
        self.assertEqual(drop_database('company'), expected)
    
    def test_use_database(self):
        expected = "USE company"
        self.assertEqual(use_database('company'), expected)


if __name__ == '__main__':
    unittest.main()
