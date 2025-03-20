import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from dbrm.remote import transfer_csv
from dbrm.sqltable import SQLTable


class TestTransferCSV(unittest.TestCase):
    def setUp(self):
        # 使用真实的CSV文件数据
        self.csv_file = 'data/sample_data.csv'
        self.test_data = pd.read_csv(self.csv_file)
        
        # Mock cursor
        self.mock_cursor = MagicMock()
        
        # 设置 execute 方法的行为
        def execute_side_effect(sql):
            if "SELECT 1 FROM" in sql:
                raise Exception("Table does not exist")
            # 其他 SQL 语句正常执行
            return None
            
        self.mock_cursor.execute.side_effect = execute_side_effect
        self.mock_cursor.executemany = MagicMock()
        self.mock_cursor.commit = MagicMock()

    @patch('dbrm.remote.get_cursor')
    def test_transfer_csv_sql_generation(self, mock_get_cursor):
        # 设置 mock
        mock_get_cursor.return_value = self.mock_cursor
        
        # 执行函数
        transfer_csv(self.csv_file, 'employee_table', if_exists='replace')
        
        # 验证生成的 SQL
        expected_create_sql = (
            "CREATE TABLE IF NOT EXISTS employee_table "
            "(姓名 VARCHAR(255), 年龄 INTEGER, 出生日期 VARCHAR(255), "
            "工资 DOUBLE, 是否在职 BOOLEAN, 邮箱 VARCHAR(255), "
            "部门 VARCHAR(255), 评分 DOUBLE)"
        )
        
        # 检查是否调用了正确的 SQL 语句
        create_calls = [call[0][0] for call in self.mock_cursor.execute.call_args_list]
        self.assertIn(expected_create_sql, create_calls)
        
        # 验证插入语句的模板
        expected_insert_template = (
            "INSERT INTO employee_table "
            "(姓名, 年龄, 出生日期, 工资, 是否在职, 邮箱, 部门, 评分) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        
        # 检查插入语句
        insert_call = self.mock_cursor.executemany.call_args_list[0]
        self.assertEqual(insert_call[0][0], expected_insert_template)
        
        # 检查插入的第一行数据
        inserted_data = insert_call[0][1][0]
        self.assertEqual(inserted_data, 
                        ('张三', 28, '1995-03-15', 12500.50, True, 
                         'zhangsan@email.com', '研发部', 4.5))
        
        # 验证所有数据都被正确传入
        self.assertEqual(len(insert_call[0][1]), len(self.test_data))


if __name__ == '__main__':
    unittest.main()