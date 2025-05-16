from Entity.User.Restaurant_Manager import Restaurant_Manager
from Entity.Keyword import Keyword
from Entity.Restaurant import Restaurant
from Entity.Menu_Item import Menu_Item
from Entity.Address import Address

# CREATE TABLE IF NOT EXISTS Restaurant (
#     restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
#     restaurant_name VARCHAR(64) NOT NULL,
#     cuisine_type ENUM('Indian', 'Asian', 'European', 'American', 'African', 'Turkish'),
#     manager_id INT NOT NULL,
#     address_id INT NOT NULL,
#     FOREIGN KEY (address_id) REFERENCES Address(address_id),
#     FOREIGN KEY (manager_id) REFERENCES User(user_id)
# );


# CREATE TABLE IF NOT EXISTS Address (
#     address_id INT PRIMARY KEY AUTO_INCREMENT,
#     user_id INT NOT NULL, -- Restaurant adresi eklerken user_id olarak restaurant manager girilecek
#     address_name VARCHAR(64),
#     address VARCHAR(255) NOT NULL,
#     city VARCHAR(64) NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES User(user_id)
# );
class Manager_Service(): 
    def __init__(self, connection):
        self.connection = connection 
        self.manager = None

    def login(self, user_name, password): 
        try: 
            query = f"SELECT user_id FROM User U JOIN Restaurant_Manager M ON M.manager_id = U.user_id WHERE user_name= '{user_name}' and password= '{password}'"
            result = self.connection.execute_query(query)
            if result is not None: 
                id = result[0][0]
                self.manager = Restaurant_Manager(id, user_name, password)
                return result
            return 0
        except Exception: 
            print(-1)

    def get_all_restaurants_by_manager(self): 
        query= "SELECT * FROM Restaurant R JOIN Address A ON R.address_id = A.address_id Where manager_id= {}".format(self.manager.user_id)
        result = self.connection.execute_query(query)
        restaurants = []

        for row in result: 
            # 4'ten sonra address
            address = Address(row[5], row[6], row[7], row[8], row[9])
            restaurant = Restaurant(row[0], row[1], row[2], self.manager.user_name, address)
            restaurants.append(restaurant)

        return restaurants
    
    def get_a_restaurant(self, restaurant_id): 
        query= "SELECT * FROM Restaurant R JOIN Address A ON R.address_id = A.address_id WHERE R.restaurant_id= {}".format(restaurant_id)

        result = self.connection.execute_query(query)
         
        if result is not None: 
            for row in result: 
                address = Address(row[5], row[6], row[7], row[8], row[9])
                restaurant = Restaurant(row[0], row[1], row[2], self.manager.user_name, address)

            return restaurant 
        
        else: 
            return -1 
        
    def get_restaurant_menu_items(self, restaurant_id): 
        query= "Select M.id, M.name, M.image, M.description, M.price, R.restaurant_id FROM Restaurant R JOIN Menu_Item M ON R.restaurant_id = M.restaurant_id WHERE R.restaurant_id = {}".format(restaurant_id)

        result = self.connection.execute_query(query)
        menu_items = []
        if (len(result) > 0 and result is not None): 
            for row in result:
                menu_item = Menu_Item(row[0], row[1], row[2], row[3], row[4], row[5])
                menu_items.append(menu_item)
            
            return menu_items
        
        return -1    
    
    
    #TODO CREATE KEYWORD - SET KEYWORD
    
    def create_menu_item(self, name, image, description, price, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. Menu item ekle
        insert_menu_item = "INSERT INTO Menu_Item (item_name, item_image, item_description, item_price, restaurant_id) VALUES ('{}', '{}', '{}', {}, {})".format(name, image, description, price, restaurant_id)
        self.connection.execute_query(insert_menu_item)
        return 1
    
    def get_all_keywords(self):
        query = "SELECT * FROM Keyword WHERE manager_id = {}".format(self.manager.user_id)
        result = self.connection.execute_query(query)
        keywords = []

        for row in result: 
            keyword = Keyword(row[0], row[1], row[2])
            keywords.append(keyword)

        return keywords
    
    
    def create_discount(self, discount_rate, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. Discount ekle
        insert_discount = "INSERT INTO Discount (discount_rate, restaurant_id) VALUES ({}, {})".format(discount_rate, restaurant_id)
        self.connection.execute_query(insert_discount)
        return 1
    
    def get_all_discounts(self, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. Discountları al
        query_discounts = "SELECT * FROM Discount WHERE restaurant_id = {}".format(restaurant_id)
        result_discounts = self.connection.execute_query(query_discounts)
        discounts = []

        for row in result_discounts: 
            discount = row[1]
            discounts.append(discount)

        return discounts
    
    def get_all_orders(self, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. Cart'ı al
        query_orders = "SELECT * FROM Cart WHERE restaurant_id = {}".format(restaurant_id)
        result_orders = self.connection.execute_query(query_orders)
        orders = []

        for row in result_orders: 
            order = row[1]
            orders.append(order)

        return orders
    
    def accept_order(self, id):
        # 1. Cart'ı kabul et
        update_order = "UPDATE Cart SET status = 'Accepted' WHERE id = {}".format(id)
        self.connection.execute_query(update_order)
        return 1
    
    def show_latest_ten_ratings(self, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. Ratingleri al
        query_ratings = "SELECT * FROM Rating WHERE restaurant_id = {} ORDER BY rating_date DESC LIMIT 10".format(restaurant_id)
        result_ratings = self.connection.execute_query(query_ratings)
        ratings = []

        for row in result_ratings: 
            rating = row[1]
            ratings.append(rating)

        return ratings
    
    def get_total_revenue(self, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. Toplam geliri al
        query_revenue = "SELECT SUM(total_price) FROM Cart WHERE restaurant_id = {}".format(restaurant_id)
        result_revenue = self.connection.execute_query(query_revenue)
        if result_revenue and len(result_revenue) > 0:
            return result_revenue[0][0]
        return 0
    
    def get_number_of_orders(self, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. Toplam sipariş sayısını al
        query_orders = "SELECT COUNT(*) FROM Cart WHERE restaurant_id = {}".format(restaurant_id)
        result_orders = self.connection.execute_query(query_orders)
        if result_orders and len(result_orders) > 0:
            return result_orders[0][0]
        return 0
    
    def get_all_restaurants(self):
        query = "SELECT * FROM Restaurant"
        result = self.connection.execute_query(query)
        restaurants = []

        for row in result: 
            restaurant = Restaurant(row[0], row[1], row[2], row[3], row[4])
            restaurants.append(restaurant)

        return restaurants
    
    def get_the_most_ordering_customer(self, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. En çok sipariş veren müşteriyi al
        query_customer = "SELECT customer_id FROM Cart WHERE restaurant_id = {} GROUP BY customer_id ORDER BY COUNT(*) DESC LIMIT 1".format(restaurant_id)
        result_customer = self.connection.execute_query(query_customer)
        if result_customer and len(result_customer) > 0:
            return result_customer[0][0]
        return 0
    
    def get_the_customer_with_highest_cart_value(self, restaurant_name):
        # total_price Cart tablosunda yok, bu yüzden fonksiyon implement edilmedi.
        raise NotImplementedError("total_price Cart tablosunda yok")
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. En yüksek sepet değerine sahip müşteriyi al
        query_customer = "SELECT customer_id FROM Cart WHERE restaurant_id = {} GROUP BY customer_id ORDER BY SUM(total_price) DESC LIMIT 1".format(restaurant_id)
        result_customer = self.connection.execute_query(query_customer)
        if result_customer and len(result_customer) > 0:
            return result_customer[0][0]
        return 0
