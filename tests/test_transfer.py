import unittest
from unittest.mock import MagicMock, patch, call
import pandas as pd
from dbrm import Engine, Session
from dbrm.remote import transfer_csv, infer_schema_from_dataframe


class TestTransferCSV(unittest.TestCase):
    def setUp(self):
        # 使用真实的CSV文件数据
        self.csv_file = 'data/sample_data.csv'
        self.test_data = pd.read_csv(self.csv_file)
        
        # Mock engine and session
        self.mock_engine = MagicMock()
        self.mock_session = MagicMock()
        self.mock_cursor = MagicMock()
        
        # Configure session's execute method to return cursor
        self.mock_session.execute.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = [0]  # Table doesn't exist
        
        # Setup context manager simulation
        self.mock_session.__enter__.return_value = self.mock_session
        self.mock_session.__exit__.return_value = None

    @patch('dbrm.remote.Session')
    def test_transfer_csv_sql_generation(self, mock_session_class):
        # Setup mocks
        mock_session_class.return_value = self.mock_session
        
        # Execute function
        transfer_csv(
            csv_file=self.csv_file, 
            table_name='employee_table', 
            engine=self.mock_engine,
            if_exists='replace'
        )
        
        # Verify create table SQL generation
        # First determine what the schema should be
        create_query = infer_schema_from_dataframe(self.test_data, 'employee_table')
        
        # Check if the create query was executed
        create_calls = [call[0][0] for call in self.mock_session.execute.call_args_list 
                       if 'CREATE TABLE' in call[0][0]]
        self.assertTrue(any('employee_table' in call for call in create_calls))
        
        # Find any execute calls with INSERT INTO
        insert_calls = [call[0][0] for call in self.mock_session.execute.call_args_list 
                        if 'INSERT INTO employee_table' in call[0][0]]
        self.assertTrue(len(insert_calls) > 0)
        
        # Check that all data rows were processed
        self.assertEqual(
            len([call for call in self.mock_session.execute.call_args_list 
                if 'INSERT INTO employee_table' in call[0][0]]), 
            len(self.test_data)
        )
        
    @patch('dbrm.remote.Session')
    def test_transfer_csv_with_existing_table(self, mock_session_class):
        # Setup mocks for existing table
        mock_session = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # Table exists
        mock_session.execute.return_value = mock_cursor
        mock_session.__enter__.return_value = mock_session
        mock_session.__exit__.return_value = None
        mock_session_class.return_value = mock_session
        
        # Execute function with 'replace' option
        transfer_csv(
            csv_file=self.csv_file, 
            table_name='employee_table',
            engine=self.mock_engine,
            if_exists='replace'
        )
        
        # Check if DROP TABLE was executed
        drop_calls = [call[0][0] for call in mock_session.execute.call_args_list 
                     if 'DROP TABLE' in call[0][0]]
        self.assertTrue(len(drop_calls) > 0)
        
    @patch('dbrm.remote.Session')
    def test_transfer_csv_fail_if_exists(self, mock_session_class):
        # Setup mocks for existing table
        mock_session = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # Table exists
        mock_session.execute.return_value = mock_cursor
        mock_session.__enter__.return_value = mock_session
        mock_session.__exit__.return_value = None
        mock_session_class.return_value = mock_session
        
        # Check that ValueError is raised with 'fail' option
        with self.assertRaises(ValueError):
            transfer_csv(
                csv_file=self.csv_file, 
                table_name='employee_table',
                engine=self.mock_engine,
                if_exists='fail'
            )


if __name__ == '__main__':
    unittest.main()