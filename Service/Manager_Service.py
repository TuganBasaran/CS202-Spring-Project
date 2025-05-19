from Entity.User.Restaurant_Manager import Restaurant_Manager
from Entity.Keyword import Keyword
from Entity.Restaurant import Restaurant
from Entity.Menu_Item import Menu_Item
from Entity.Address import Address
from Entity.Rating import Rating
from Entity.Discount import Discount
from Entity.Cart import Cart

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
        
    
    
    def get_restaurant_menu_items_with_discounts(self, restaurant_id):
        """Get all menu items for a restaurant with discount information if available"""
        # Get menu items with any active discounts
        query = """
        SELECT 
            M.id, M.name, M.image, M.description, M.price, M.restaurant_id,
            D.id, D.discount_rate, D.start_date, D.end_date
        FROM 
            Menu_Item M
        LEFT JOIN 
            Has_Discount HD ON M.id = HD.menu_item_id
        LEFT JOIN 
            Discount D ON HD.discount_id = D.id 
                AND CURDATE() BETWEEN D.start_date AND D.end_date
        WHERE 
            M.restaurant_id = {}
        """.format(restaurant_id)

        result = self.connection.execute_query(query)
        menu_items = []
        
        if result and len(result) > 0:
            for row in result:
                # Create the basic menu item
                menu_item = Menu_Item(row[0], row[1], row[2], row[3], row[4], row[5])
                
                # Check if there's an active discount
                if row[6] is not None:
                    discount_id = row[6]
                    discount_rate = row[7]
                    start_date = row[8]
                    end_date = row[9]
                    
                    # Add discount properties to menu item
                    menu_item.has_discount = True
                    menu_item.discount_rate = discount_rate
                    menu_item.original_price = menu_item.price
                    # Calculate discounted price
                    menu_item.price = round(menu_item.price * (1 - discount_rate/100), 2)
                    
                    # Add these missing properties
                    menu_item.discount_id = discount_id  # Add this line
                    menu_item.end_date = end_date        # Add this line for date in template
                else:
                    menu_item.has_discount = False
                    menu_item.discount_rate = 0
            
                menu_items.append(menu_item)
            return menu_items
        else:
            return []  # No menu items found
    
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
    
    def get_restaurant_discounts(self, restaurant_id):
        """Get all discounts for a restaurant's menu items"""
        query = """
        SELECT DISTINCT d.id, d.discount_rate, d.start_date, d.end_date
        FROM Discount d
        JOIN Has_Discount hd ON d.id = hd.discount_id
        JOIN Menu_Item m ON hd.menu_item_id = m.id
        WHERE m.restaurant_id = {}
        """.format(restaurant_id)
        
        result = self.connection.execute_query(query)
        discounts = []
        
        if result and len(result) > 0:
            for row in result:
                discount = Discount(row[0], row[1], row[2], row[3])
                discounts.append(discount)
        return discounts

    def create_discount(self, discount_rate, start_date, end_date):
        """Create a new discount and return its ID"""
        # Add quotes around date values for SQL
        quoted_start_date = f"'{start_date}'"
        quoted_end_date = f"'{end_date}'"
        
        # Create the insert query
        insert_query = """
        INSERT INTO Discount (discount_rate, start_date, end_date) 
        VALUES ({}, {}, {})
        """.format(discount_rate, quoted_start_date, quoted_end_date)
        
        # Execute the query
        self.connection.execute_query(insert_query)
        
        # Get the ID of the inserted discount
        get_id_query = "SELECT LAST_INSERT_ID()"
        result = self.connection.execute_query(get_id_query)
        return result[0][0]  # Return the new discount ID

    def apply_discount_to_menu_item(self, menu_item_id, discount_id):
        """Apply a discount to a menu item"""
        # Check if this discount is already applied to this menu item
        check_query = """
        SELECT * FROM Has_Discount 
        WHERE menu_item_id = {} AND discount_id = {}
        """.format(menu_item_id, discount_id)
        
        result = self.connection.execute_query(check_query)
        
        if not result or len(result) == 0:
            # Apply the discount to the menu item
            insert_query = """
            INSERT INTO Has_Discount (menu_item_id, discount_id) 
            VALUES ({}, {})
            """.format(menu_item_id, discount_id)
            self.connection.execute_query(insert_query)
            return True
        return False  # Discount already applied to this menu item

    def remove_discount_from_menu_item(self, menu_item_id, discount_id):
        """Remove a discount from a menu item"""
        delete_query = """
        DELETE FROM Has_Discount 
        WHERE menu_item_id = {} AND discount_id = {}
        """.format(menu_item_id, discount_id)
        self.connection.execute_query(delete_query)
        return True
    
    def get_restaurant_pending_orders(self, restaurant_id):
        """Get all pending orders for a restaurant"""
        query = """
        SELECT 
            c.id, c.customer_id, c.restaurant_id, c.status, c.order_time, 
            u.user_name, 
            GROUP_CONCAT(CONCAT(m.name, ' (', con.quantity, ')') SEPARATOR ', ') as items,
            SUM(m.price * con.quantity) as total_price
        FROM 
            Cart c
        JOIN 
            User u ON c.customer_id = u.user_id
        JOIN 
            Contains con ON c.id = con.cart_id
        JOIN 
            Menu_Item m ON con.menu_item_id = m.id
        WHERE 
            c.restaurant_id = {} AND c.status = 'waiting'
        GROUP BY 
            c.id
        ORDER BY 
            c.order_time DESC
        """.format(restaurant_id)
        
        result = self.connection.execute_query(query)
        orders = []
        
        if result and len(result) > 0:
            for row in result:
                order = Cart(row[0], row[1], row[2], row[3], row[4])
                order.customer_name = row[5]
                order.items = row[6]
                order.total_price = row[7]
                orders.append(order)
            return orders
        else:
            return []

    def update_order_status(self, order_id, status, restaurant_id):
        """Update the status of an order"""
        # First verify that this order belongs to the restaurant
        check_query = """
        SELECT id FROM Cart 
        WHERE id = {} AND restaurant_id = {}
        """.format(order_id, restaurant_id)
        
        result = self.connection.execute_query(check_query)
        
        if result and len(result) > 0:
            # Update the order status
            update_query = """
            UPDATE Cart 
            SET status = '{}'
            WHERE id = {}
            """.format(status, order_id)
            
            self.connection.execute_query(update_query)
            return True
        return False  # Order not found or doesn't belong to this restaurant

    def get_restaurant_all_orders(self, restaurant_id):
        """Get all orders for a restaurant with their statuses"""
        query = """
        SELECT 
            c.id, c.customer_id, c.restaurant_id, c.status, c.order_time, 
            u.user_name, 
            GROUP_CONCAT(CONCAT(m.name, ' (', con.quantity, ')') SEPARATOR ', ') as items,
            SUM(m.price * con.quantity) as total_price
        FROM 
            Cart c
        JOIN 
            User u ON c.customer_id = u.user_id
        JOIN 
            Contains con ON c.id = con.cart_id
        JOIN 
            Menu_Item m ON con.menu_item_id = m.id
        WHERE 
            c.restaurant_id = {}
        GROUP BY 
            c.id
        ORDER BY 
            c.order_time DESC
        """.format(restaurant_id)
        
        result = self.connection.execute_query(query)
        orders = []
        
        if result and len(result) > 0:
            for row in result:
                order = Cart(row[0], row[1], row[2], row[3], row[4])
                order.customer_name = row[5]
                order.items = row[6]
                order.total_price = row[7]
                orders.append(order)
            return orders
        else:
            return []
    
    def get_manager_total_revenue(self):
        """Calculate total revenue from all restaurants managed by this manager"""
        query = """
        SELECT SUM(m.price * con.quantity) as total_revenue
        FROM Cart c
        JOIN Contains con ON c.id = con.cart_id
        JOIN Menu_Item m ON con.menu_item_id = m.id
        JOIN Restaurant r ON c.restaurant_id = r.restaurant_id
        WHERE r.manager_id = {} AND c.status IN ('delivered', 'accepted')
        """.format(self.manager.user_id)
        
        result = self.connection.execute_query(query)
        if result and result[0][0] is not None:
            return round(result[0][0], 2)
        return 0.0  # No revenue yet

    def get_manager_total_orders(self):
        """Count total orders from all restaurants managed by this manager"""
        query = """
        SELECT COUNT(DISTINCT c.id) as total_orders
        FROM Cart c
        JOIN Restaurant r ON c.restaurant_id = r.restaurant_id
        WHERE r.manager_id = {}
        """.format(self.manager.user_id)
        
        result = self.connection.execute_query(query)
        if result:
            return result[0][0]
        return 0  # No orders yet
    
    def get_restaurant_revenue(self, restaurant_id):
        """Calculate total revenue for a specific restaurant"""
        query = """
        SELECT SUM(m.price * con.quantity) as total_revenue
        FROM Cart c
        JOIN Contains con ON c.id = con.cart_id
        JOIN Menu_Item m ON con.menu_item_id = m.id
        WHERE c.restaurant_id = {} AND c.status IN ('delivered', 'accepted')
        """.format(restaurant_id)
        
        result = self.connection.execute_query(query)
        if result and result[0][0] is not None:
            return round(result[0][0], 2)
        return 0.0  # No revenue yet

    def get_restaurant_order_count(self, restaurant_id):
        """Count total orders for a specific restaurant"""
        query = """
        SELECT COUNT(DISTINCT c.id) as total_orders
        FROM Cart c
        WHERE c.restaurant_id = {}
        """.format(restaurant_id)
        
        result = self.connection.execute_query(query)
        if result:
            return result[0][0]
        return 0  # No orders yet
    
    def get_menu_item_sales_stats(self, restaurant_id, days=30):
        """Get total quantity sold and revenue per menu item for the past month"""
        query = """
        SELECT 
            m.id, m.name, m.image, m.price,
            SUM(con.quantity) as total_quantity,
            SUM(m.price * con.quantity) as total_revenue
        FROM 
            Menu_Item m
        JOIN 
            Contains con ON m.id = con.menu_item_id
        JOIN 
            Cart c ON con.cart_id = c.id
        WHERE 
            m.restaurant_id = {}
        /* Include all status types instead of filtering */
        /* AND c.order_time >= DATE_SUB(CURDATE(), INTERVAL {} DAY) */
        GROUP BY 
            m.id
        ORDER BY 
            total_revenue DESC
        """.format(restaurant_id, days)
        
        result = self.connection.execute_query(query)
        menu_item_stats = []
        
        if result and len(result) > 0:
            for row in result:
                item_stat = {
                    'id': row[0],
                    'name': row[1],
                    'image': row[2],
                    'price': row[3],
                    'total_quantity': row[4],
                    'total_revenue': round(row[5], 2)
                }
                menu_item_stats.append(item_stat)
    
        return menu_item_stats
    
    def get_customer_most_orders(self, restaurant_id, days=30):
        """Get the customer who placed the most orders in the specified time period"""
        query = """
        SELECT 
            u.user_id, u.user_name,
            COUNT(DISTINCT c.id) as order_count
        FROM 
            Cart c
        JOIN 
            User u ON c.customer_id = u.user_id
        WHERE 
            c.restaurant_id = {}
            /* Remove date filtering */
        GROUP BY 
            c.customer_id
        ORDER BY 
            order_count DESC
        LIMIT 1
        """.format(restaurant_id)
        
        result = self.connection.execute_query(query)
        
        if result and len(result) > 0:
            return {
                'user_id': result[0][0],
                'user_name': result[0][1],
                'order_count': result[0][2]
            }
        
        return None  # No customers with orders in this period

    def get_customer_highest_value_cart(self, restaurant_id, days=30):
        """Get the customer with the highest-value cart in the specified time period"""
        query = """
        SELECT 
            c.id as cart_id,
            u.user_id, u.user_name,
            SUM(m.price * con.quantity) as total_value,
            c.order_time,
            GROUP_CONCAT(CONCAT(m.name, ' (', con.quantity, ')') SEPARATOR ', ') as cart_items
        FROM 
            Cart c
        JOIN 
            User u ON c.customer_id = u.user_id
        JOIN 
            Contains con ON c.id = con.cart_id
        JOIN 
            Menu_Item m ON con.menu_item_id = m.id
        WHERE 
            c.restaurant_id = {}
        GROUP BY 
            c.id
        ORDER BY 
            total_value DESC
        LIMIT 1
        """.format(restaurant_id)
    
        result = self.connection.execute_query(query)
        
        if result and len(result) > 0:
            return {
                'cart_id': result[0][0],
                'user_id': result[0][1],
                'user_name': result[0][2],
                'total_value': result[0][3],
                'order_time': result[0][4],
                'cart_items': result[0][5]  # Changed from 'items' to 'cart_items'
            }
        
        return None  # No carts in this period