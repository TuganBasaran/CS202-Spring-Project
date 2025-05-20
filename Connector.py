import mysql.connector as mysql_connector

class Connector(): 
    def __init__(self, user, password, database):
        self.user = user 
        self.password = password 
        self.database = database 
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self): 
        self.connection = mysql_connector.connect(host= 'localhost',
                                          port= 3306,
                                          user= self.user,
                                          password= self.password,
                                          database= self.database)
            
        self.cursor = self.connection.cursor()
        
    def execute_query(self, query):
        self.cursor.execute(query)
        if query.strip().lower().startswith("select"):
            return self.cursor.fetchall()
        else:
            self.connection.commit()
        return None
        
    def commit(self):
        """Commit changes to the database"""
        if self.connection:
            self.connection.commit()
            
    def close(self):
        """Close cursor and connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None


    def get_last_insert_id(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID()")
        return cursor.fetchone()[0]