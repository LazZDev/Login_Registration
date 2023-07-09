import pymysql.cursors

# Define a class to establish a connection and interact with MySQL database


class MySQLConnection:
    def __init__(self, db):
        # Establish a connection to the MySQL database
        connection = pymysql.connect(
            host='localhost',  # Hostname of the MySQL server
            user='root',  # MySQL username
            password='root',  # MySQL password
            db=db,  # Name of the database to connect to
            charset='utf8mb4',  # Character encoding
            cursorclass=pymysql.cursors.DictCursor,  # Cursor class to return results as dictionaries
            autocommit=True  # Automatically commit changes to the database
        )
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                # Format the query with the provided data
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                # Execute the query with the data
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # If the query is an INSERT statement, commit the changes and return the last inserted ID
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # If the query is a SELECT statement, fetch all the results as a list of dictionaries
                    result = cursor.fetchall()
                    return result
                else:
                    # For other types of queries like UPDATE and DELETE, commit the changes and return nothing
                    self.connection.commit()
            except Exception as e:
                # If an exception occurs, print an error message and return False
                print("Something went wrong", e)
                return False
            finally:
                # Close the database connection
                self.connection.close()

# Function to create an instance of MySQLConnection for a given database name


def connectToMySQL(db):
    return MySQLConnection(db)
