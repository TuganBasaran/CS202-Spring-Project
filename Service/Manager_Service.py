from Entity.User.Restaurant_Manager import Restaurant_Manager
from Entity.Keyword import Keyword
from Entity.Restaurant import Restaurant
from Entity.Menu_Item import Menu_Item
from Entity.Address import Address
from Entity.Rating import Rating

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
    
    def get_restaurant_ratings(self, restaurant_id):
        query = """
        SELECT 
            r.id, r.rating, r.comment, c.id, u.user_name, r.restaurant_id, r.created_at,
            GROUP_CONCAT(m.name SEPARATOR ', ')
        FROM 
            Rating r
        JOIN 
            Cart c ON r.cart_id = c.id
        JOIN 
            User u ON c.customer_id = u.user_id
        JOIN 
            Contains cmi ON c.id = cmi.cart_id
        JOIN 
            Menu_Item m ON cmi.menu_item_id = m.id
        WHERE 
            r.restaurant_id = {}
        GROUP BY r.id
        ORDER BY r.created_at DESC
        LIMIT 10
    """.format(restaurant_id)
        results = self.connection.execute_query(query)
        ratings = []
        average_rating= 0 
        if results is not None and len(results) > 0: 
            for row in results: 
                # Burada row[7] sipariş edilen yemeklerin listesini içeriyor
                rating = Rating(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                ratings.append(rating)
                average_rating+= rating.rating
            average_rating = average_rating / len(ratings)
            return ratings, average_rating
        else: 
            return [], 0 # -1 yerine boş liste döndürmek daha uygun
            # for row in result: 
                # rating= Rating(row[0], row[1], row[2],)

    def get_restaurant_keywords(self, restaurant_id): 
        query = """
        SELECT k.keyword_id, k.keyword, k.manager_id
        FROM Keyword k
        JOIN Restaurant_Keyword rk ON k.keyword_id = rk.keyword_id
        WHERE rk.restaurant_id = {}
        """.format(restaurant_id)
        
        result = self.connection.execute_query(query)
        keywords = []
        
        if result is not None and len(result) > 0:
            for row in result:
                # row[0] = keyword_id, row[1] = keyword, row[2] = manager_id
                keyword = Keyword(row[0], row[1], row[2])
                keywords.append(keyword)
            return keywords
        else:
            return []  # Eğer keyword bulunamazsa boş liste döndür
    
    def create_keyword(self, keyword_text):
        """Create a new keyword and return its ID"""
        # Check if keyword already exists for this manager
        check_query = """
        SELECT keyword_id FROM Keyword 
        WHERE keyword= {} AND manager_id= {}
        """.format(keyword_text, self.manager.user_id)
        result = self.connection.execute_query(check_query)
        
        if result and len(result) > 0:
            # Keyword already exists, return existing ID
            return result[0][0]
        
        # Create new keyword
        insert_query = """
        INSERT INTO Keyword (keyword, manager_id) 
        VALUES ({}, {})
        """.format(keyword_text, self.manager.user_id)
        self.connection.execute_query(insert_query)
        
        # Get the ID of the inserted keyword
        get_id_query = "SELECT LAST_INSERT_ID()"
        result = self.connection.execute_query(get_id_query)
        return result[0][0]
    
    def add_keyword_to_restaurant(self, restaurant_id, keyword_id=None, keyword_text=None):
        """Add a keyword to a restaurant using either keyword_id or keyword_text"""
        # If keyword_text is provided, create or get the keyword first
        if keyword_id is None and keyword_text:
            keyword_id = self.create_keyword(keyword_text)
        
        # Check if the restaurant already has this keyword
        check_query = """
        SELECT * FROM Restaurant_Keyword 
        WHERE restaurant_id = {} AND keyword_id = {}
        """.format(restaurant_id, keyword_id)
        result = self.connection.execute_query(check_query)
        
        if not result or len(result) == 0:
            # Add the keyword to the restaurant
            insert_query = """
            INSERT INTO Restaurant_Keyword (restaurant_id, keyword_id) 
            VALUES ({}, {})
            """.format(restaurant_id, keyword_id)
            self.connection.execute_query(insert_query)
            return True
        return False  # Keyword already assigned to this restaurant
    
    def remove_keyword_from_restaurant(self, restaurant_id, keyword_id):
        """Remove a keyword from a restaurant"""
        delete_query = """
        DELETE FROM Restaurant_Keyword 
        WHERE restaurant_id = %s AND keyword_id = %s
        """
        self.connection.execute_query(delete_query, restaurant_id, keyword_id)
        return True
    
    def get_manager_keywords(self):
        """Get all keywords created by this manager"""
        query = """
        SELECT keyword_id, keyword, manager_id
        FROM Keyword
        WHERE manager_id = {}
        """.format(self.manager.user_id)
        result = self.connection.execute_query(query)
        keywords = []
        
        if result and len(result) > 0:
            for row in result:
                keyword = Keyword(row[0], row[1], row[2])
                keywords.append(keyword)
        return keywords
    
    def create_menu_item(self, name, image, description, price, restaurant_id):
        """Create a new menu item for a restaurant"""
        # Add quotes around string values for SQL
        quoted_name = f"'{name}'"
        quoted_image = f"'{image}'"
        quoted_description = f"'{description}'"
        
        # Create the insert query
        insert_query = """
        INSERT INTO Menu_Item (name, image, description, price, restaurant_id) 
        VALUES ({}, {}, {}, {}, {})
        """.format(quoted_name, quoted_image, quoted_description, price, restaurant_id)
        
        # Execute the query
        self.connection.execute_query(insert_query)
        
        # Get the ID of the inserted menu item
        get_id_query = "SELECT LAST_INSERT_ID()"
        result = self.connection.execute_query(get_id_query)
        return result[0][0]  # Return the new menu item ID
    
    def delete_menu_item(self, menu_item_id, restaurant_id):
        """Delete a menu item from a restaurant's menu"""
        # First verify that this menu item belongs to the restaurant
        # (security check to prevent deletion of other restaurants' items)
        check_query = """
        SELECT id FROM Menu_Item 
        WHERE id = {} AND restaurant_id = {}
        """.format(menu_item_id, restaurant_id)
        
        result = self.connection.execute_query(check_query)
        
        if result and len(result) > 0:
            # Delete the menu item
            delete_query = """
            DELETE FROM Menu_Item 
            WHERE id = {}
            """.format(menu_item_id)
            
            self.connection.execute_query(delete_query)
            return True
        return False  # Menu item not found or doesn't belong to this restaurant