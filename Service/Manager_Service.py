class Manager_Service(): 
    def __init__(self, connection):
        self.connection = connection 


    def login(self, user_name, password): 
        query = f"SELECT user_id FROM User U JOIN Restaurant_Manager M ON M.manager_id = U.user_id WHERE user_name= '{user_name}' and password= '{password}'"
        result = self.connection.execute_query(query)
        if result is not None: 
            return result
        return 0 
    
    
