import unittest
import mysql.connector

class TestStateCreation(unittest.TestCase):

    @unittest.skipIf(HBNB_TYPE_STORAGE != 'db', 'MySQL-specific test')
    def test_create_state(self):
        # Connect to the test database
        connection = mysql.connector.connect(
            host=HBNB_MYSQL_HOST,
            user=HBNB_MYSQL_USER,
            password=HBNB_MYSQL_PWD,
            database=HBNB_MYSQL_DB
        )
        cursor = connection.cursor()

        # Get initial record count
        cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = cursor.fetchone()[0]

        # Execute the create State command
        cursor.execute("INSERT INTO states (name) VALUES (%s)", ("California",))
        connection.commit()

        # Get new record count
        cursor.execute("SELECT COUNT(*) FROM states")
        new_count = cursor.fetchone()[0]

        # Assert the difference is +1
        self.assertEqual(new_count - initial_count, 1)

        cursor.close()
        connection.close()

if __name__ == '__main__':
    unittest.main()

