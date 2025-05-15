from Entity.User.Restaurant_Manager import Restaurant_Manager
from Entity.Keyword import Keyword
from Entity.Restaurant import Restaurant
from Entity.Menu_Item import Menu_Item
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
            return 0
        restaurant_id = result_restaurant[0][0]

        # 3. Restaurant_Keyword ilişkisini ekle (varsa hata verme)
        insert_relation = "INSERT INTO Restaurant_Keyword (keyword_id, restaurant_id) VALUES ({}, {})".format(keyword_id, restaurant_id)
        self.connection.execute_query(insert_relation)
        return 1
    
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
    
    def get_all_menu_items(self, restaurant_name):
        # 1. Restaurant id'yi bul
        query_restaurant = "SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '{}'".format(restaurant_name)
        result_restaurant = self.connection.execute_query(query_restaurant)
        if not result_restaurant or len(result_restaurant) == 0:
            return 0
        restaurant_id = result_restaurant[0][0]

        # 2. Menu itemleri al
        query_menu_items = "SELECT * FROM Menu_Item WHERE restaurant_id = {}".format(restaurant_id)
        result_menu_items = self.connection.execute_query(query_menu_items)
        menu_items = []

        for row in result_menu_items: 
            menu_item = Menu_Item(row[0], row[1], row[2], row[3], row[4])
            menu_items.append(menu_item)

        return menu_items
    
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
        # total_price Cart tablosunda yok, bu yüzden fonksiyon implement edilmedi.
        raise NotImplementedError("total_price Cart tablosunda yok")
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
