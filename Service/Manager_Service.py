from Entity.User.Restaurant_Manager import Restaurant_Manager
from Entity.Keyword import Keyword
from Entity.Restaurant import Restaurant
class Manager_Service(): 
    def __init__(self, connection):
        self.connection = connection 
        self.manager = None

    def login(self, user_name, password): 
        query = f"SELECT user_id FROM User U JOIN Restaurant_Manager M ON M.manager_id = U.user_id WHERE user_name= '{user_name}' and password= '{password}'"
        result = self.connection.execute_query(query)
        if result is not None: 
            id = result[0][0]
            self.manager = Restaurant_Manager(id, user_name, password)
            return result
        return 0
    
    def get_all_restaurants_by_manager(self): 
        query= "SELECT * FROM Restaurant Where manager_id= {}".format(self.manager.user_id)
        result = self.connection.execute_query(query)
        restaurants = []

        for row in result: 
            restaurant = Restaurant(row[0], row[1], row[2], row[3], row[4])
            restaurants.append(restaurant)

        return restaurants
    
    def create_keyword(self, keyword):
        manager_id = self.manager.user_id
        query = "INSERT INTO Keyword (keyword, manager_id) VALUES ('{}', {})".format(keyword, manager_id)
        result = self.connection.execute_query(query)
        return result 

    def set_keyword(self, restaurant_name, keyword):
        # 1. Keyword var mı kontrol et, yoksa ekle
        query_keyword = "SELECT keyword_id FROM Keyword WHERE keyword = '{}'".format(keyword)
        result_keyword = self.connection.execute_query(query_keyword)
        if result_keyword and len(result_keyword) > 0:
            keyword_id = result_keyword[0][0]
        else:
            insert_keyword = "INSERT INTO Keyword (keyword, manager_id) VALUES ('{}', {})".format(keyword, self.manager.user_id)
            self.connection.execute_query(insert_keyword)
            # Yeni eklenen keyword_id'yi al
            result_keyword = self.connection.execute_query(query_keyword)
            keyword_id = result_keyword[0][0]

        # 2. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return "Restaurant not found"
        restaurant_id = result_restaurant[0][0]

        # 3. Restaurant_Keyword ilişkisini ekle (varsa hata verme)
        insert_relation = "INSERT IGNORE INTO Restaurant_Keyword (keyword_id, restaurant_id) VALUES ({}, {})".format(keyword_id, restaurant_id)
        self.connection.execute_query(insert_relation)
        return "Keyword set successfully"