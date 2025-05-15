class Customer_Service(): 
    def __init__(self, connection):
        self.connection = connection 

    def select_by_id(self, id): 
        query = f'SELECT * FROM User WHERE user_id= {id}'
        result = self.connection.execute_query(query)
        return result 
    
    def search_restaurants(self, name): 
        query = "SELECT * FROM Restaurant WHERE restaurant_name = '{}'".format(name)
        result = self.connection.execute_query(query)
        return result 