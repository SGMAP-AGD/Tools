import unittest
import pg_tools
import pandas as pd


class TestPGToolsMethods(unittest.TestCase):

    def test_conn_string(self):
        conn_string = pg_tools.get_conn_string(host="localhost",
                                               dbname="postgres",
                                               user="username",
                                               password="commonpassword",
                                               client_encoding="some-" +
                                               "exotic-encoding")
        expected_string = "host='localhost' " + \
                          "dbname='postgres' " + \
                          "user='username' " + \
                          "password='commonpassword' " + \
                          "client_encoding='some-exotic-encoding'"
        self.assertEqual(conn_string, expected_string)

    def test_export_table(self):
        table_name = "iris_unittest"
        iris = pd.read_csv("https://raw.github.com/pydata"
                           "/pandas/master/pandas/tests/data/iris.csv")
        pg_tools.export_df(df=iris, table_name=table_name)
        results = pg_tools.execute_sql("SELECT COUNT(relname) " +
                                       "FROM pg_class WHERE relname='" +
                                       table_name + "'")
        self.assertEqual(1, results[0][0][0])

    def test_import_table(self):
        table_name = "iris_unittest"
        iris = pg_tools.import_table(table_name)
        size_table = pg_tools.execute_sql("SELECT COUNT(*) "
                                          "FROM " + table_name)
        size_df = len(iris[0])
        self.assertEqual(size_df, size_table[0][0][0])

    def test_drop_table(self):
        table_name = "iris_unittest"
        drop = pg_tools.execute_sql("DROP TABLE " + table_name + "")
        results = pg_tools.execute_sql("SELECT COUNT(relname) "
                                       "FROM pg_class WHERE relname='"
                                       "" + table_name + "'")
        self.assertEqual(0, results[0][0][0])

if __name__ == '__main__':
    unittest.main()
