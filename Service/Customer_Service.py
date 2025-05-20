from Entity.User import User
from Entity.User.Customer import Customer

class Customer_Service():
    def __init__(self, connection):
        self.connection = connection
        self.user = None

    def login(self, username, password):
        try:
            query = (f"SELECT user_id FROM User U JOIN Customer C ON C.customer_id = "
                     f"U.user_id WHERE user_name = '{username}' AND password = '{password}'")
            result = self.connection.execute_query(query)
            if result and len(result) > 0:
                id = result[0][0]
                self.user = Customer(id, username, password)
                return True
            return False
        except Exception as e:
            print("Login failed")
            print(e)

    def get_ratings(self):
        # Çıktı düzenlenmeli
        customer_id = self.user.user_id
        try:
            query = (f"SELECT R.id, R.rating, R.comment, R.created_at, Res.restaurant_name "
                     f"FROM Rating R "
                     f"JOIN Restaurant Res ON R.restaurant_id = Res.restaurant_id "
                     f"WHERE R.customer_id = {customer_id} "
                     f"ORDER BY R.created_at DESC")
            result = self.connection.execute_query(query)
            return result
        except Exception as e:
            print("Failed to get ratings")
            print(e)
            return None

    def create_rating(self, cart_id, rating, comment, customer_id, restaurant_id):
        #Should the restaurant Id insertion handled here and should we allow multiple ratings
        #Cart and rating can have mismatch info since the restaurant is  manual
        try:
            query = (f" INSERT INTO Rating (cart_id, rating, comment, customer_id, restaurant_id)"
                     f"VALUES ({cart_id}, {rating}, '{comment}', {customer_id}, {restaurant_id})")
            self.connection.execute_query(query)
            print("Created rating")
            return True
        except Exception as e:
            print("Error while creating rating:", e)
            return e

    def view_address(self, user_id):
        try:
            query = f"SELECT address_id, address_name, address, city FROM Address WHERE user_id = {user_id};"
            result = self.connection.execute_query(query)
            return result
        except Exception as e:
            print("Error fetching address:", e)
            return []

    def view_phone_number(self, user_id):
        try:
            query = f"SELECT phone_number FROM Phone_Number WHERE user_id = {user_id};"
            result = self.connection.execute_query(query)
            return result
        except Exception as e:
            print("Error fetching phone number:", e)
            return []

    def delete_address(self, address_id):
        try:
            query = f"DELETE FROM Address WHERE address_id = {address_id}"
            self.connection.execute_query(query)
        except Exception as e:
            print("Error deleting address:", e)

    def update_phone_number(self, phone_id, new_number):
        try:
            query = f"UPDATE Phone_Number SET phone_number = '{new_number}' WHERE id = {phone_id}"
            self.connection.execute_query(query)
        except Exception as e:
            print("Phone update failed:", e)

    def delete_phone_number(self, phone_id):
        try:
            query = f"DELETE FROM Phone_Number WHERE id = {phone_id}"
            self.connection.execute_query(query)
        except Exception as e:
            print("Phone delete failed:", e)

    def add_address(self, user_id, address_name, address, city):
        try:
            query = (f"INSERT INTO Address (user_id, address_name, address, city)"
                     f"VALUES ({user_id}, '{address_name}', '{address}', '{city}')")
            self.connection.execute_query(query)
            print("Added address")
            return True
        except Exception as e:
            print("Error while adding address:", e)


            return e

    def update_address(self, address_id, name, address, city):
        try:
            query = f"""
                UPDATE Address
                SET address_name = '{name}', address = '{address}', city = '{city}'
                WHERE address_id = {address_id}
            """
            self.connection.execute_query(query)
        except Exception as e:
            print("Address update failed:", e)

    def delete_address(self, address_id):
        try:
            query = f"DELETE FROM Address WHERE address_id = {address_id}"
            self.connection.execute_query(query)
        except Exception as e:
            print("Address delete failed:", e)

    def add_phone_number(self, user_id, phone_number):
        try:
            query = (f"INSERT INTO Phone_Number (user_id, phone_number)"
                     f"VALUES ({user_id}, '{phone_number}')")
            self.connection.execute_query(query)
            print("Added Phone Number")
            return True
        except Exception as e:
            print("Error while adding phone number:", e)
            return e

    def get_restaurants_sorted_by_rating(self):
        customer_id = self.user.user_id
        try:
            query = f"""
            SELECT R.restaurant_id, R.restaurant_name, A.city,
                AVG(RT.rating) AS average_rating FROM Customer C
            JOIN Address AC ON C.customer_id = AC.user_id
            JOIN Restaurant R ON R.address_id IN (
            SELECT address_id FROM Address WHERE city = AC.city )
            JOIN Address A ON R.address_id = A.address_id
            LEFT JOIN Rating RT ON R.restaurant_id = RT.restaurant_id
            WHERE C.customer_id = {customer_id}
            GROUP BY  R.restaurant_id, R.restaurant_name, A.city
            ORDER BY average_rating DESC;
            """
            result = self.connection.execute_query(query)
            return result
        except Exception as e:
            print("Failed to get restaurants by rating")
            print(e)
            return None

    def add_to_cart(self, customer_id, menu_item_id, restaurant_id):
        try:
            # 1. Find or create a cart
            cart_query = f"""
                SELECT id FROM Cart 
                WHERE customer_id = {customer_id} 
                  AND restaurant_id = {restaurant_id}
                  AND status = 'not_sent'
            """
            cart_result = self.connection.execute_query(cart_query)

            if cart_result and len(cart_result) > 0:
                cart_id = cart_result[0][0]
            else:
                # Create new cart
                create_cart_query = f"""
                    INSERT INTO Cart (customer_id, restaurant_id, status)
                    VALUES ({customer_id}, {restaurant_id}, 'not_sent')
                """
                self.connection.execute_query(create_cart_query)

                # ✅ Get the last inserted ID from the connection
                cart_id = self.connection.get_last_insert_id()
                if not cart_id:
                    print("Cart creation failed: no cart_id returned.")
                    return False

            # 2. Insert or update item in cart
            insert_item_query = f"""
                INSERT INTO Contains (cart_id, menu_item_id, quantity)
                VALUES ({cart_id}, {menu_item_id}, 1)
                ON DUPLICATE KEY UPDATE quantity = quantity + 1
            """
            self.connection.execute_query(insert_item_query)

            print(f"Item {menu_item_id} added to cart {cart_id}")
            return True

        except Exception as e:
            print("Error in add_to_cart:", e)
            return False

    def get_last_insert_id(self):
        return self.connection.cursor.lastrowid

    def select_by_id(self, id):
        query = f'SELECT * FROM User WHERE user_id= {id}'
        result = self.connection.execute_query(query)
        return result

    def get_restaurant(self, restaurant_id):
        try:
            query = f"""
                SELECT R.restaurant_id, R.restaurant_name, A.city
                FROM Restaurant R
                JOIN Address A ON R.address_id = A.address_id
                WHERE R.restaurant_id = {restaurant_id}
            """
            result = self.connection.execute_query(query)
            if result and len(result) > 0:
                row = result[0]
                return {
                    'restaurant_id': row[0],
                    'restaurant_name': row[1],
                    'city': row[2]
                }
            return None
        except Exception as e:
            print("Error in get_restaurant:", e)
            return None

    def get_restaurant_menu_items(self, restaurant_id):
        try:
            query = f"""
                SELECT id, name, image, description, price
                FROM Menu_Item
                WHERE restaurant_id = {restaurant_id}
            """
            result = self.connection.execute_query(query)
            menu_items = []
            for row in result:
                menu_items.append({
                    'id': row[0],
                    'name': row[1],
                    'image': row[2],
                    'description': row[3],
                    'price': row[4]
                })
            return menu_items
        except Exception as e:
            print("Error in get_restaurant_menu_items:", e)
            return []

    def get_restaurant_ratings(self, restaurant_id):
        try:
            query = f"""
                SELECT rating, comment, created_at
                FROM Rating
                WHERE restaurant_id = {restaurant_id}
                ORDER BY created_at DESC
            """
            result = self.connection.execute_query(query)
            if result:
                ratings = result
                avg_query = f"""
                    SELECT AVG(rating) FROM Rating
                    WHERE restaurant_id = {restaurant_id}
                """
                avg_result = self.connection.execute_query(avg_query)
                average = avg_result[0][0] if avg_result and avg_result[0][0] is not None else None
                return ratings, average
            return [], None
        except Exception as e:
            print("Error fetching ratings:", e)
            return [], None

    def get_open_cart_details(self, customer_id):
        try:
            # Get the open cart
            cart_query = f"""
                SELECT id, restaurant_id FROM Cart
                WHERE customer_id = {customer_id} AND status = 'not_sent'
                ORDER BY order_time DESC
                LIMIT 1
            """
            cart_result = self.connection.execute_query(cart_query)
            if not cart_result:
                return None, []

            cart_id, restaurant_id = cart_result[0]

            # Get restaurant name
            restaurant_query = f"SELECT restaurant_name FROM Restaurant WHERE restaurant_id = {restaurant_id}"
            restaurant_name = self.connection.execute_query(restaurant_query)[0][0]

            # Get cart items
            items_query = f"""
                SELECT M.id, M.name, M.image, M.price, C.quantity
                FROM Contains C
                JOIN Menu_Item M ON C.menu_item_id = M.id
                WHERE C.cart_id = {cart_id}
            """
            item_result = self.connection.execute_query(items_query)
            items = []
            total_price = 0
            for row in item_result:
                item = {
                    'id': row[0],
                    'name': row[1],
                    'image': row[2],
                    'price': row[3],
                    'quantity': row[4],
                    'subtotal': row[3] * row[4]
                }
                total_price += item['subtotal']
                items.append(item)

            return {
                'cart_id': cart_id,
                'restaurant_id': restaurant_id,
                'restaurant_name': restaurant_name,
                'total_price': total_price
            }, items

        except Exception as e:
            print("Error fetching cart:", e)
            return None, []

    def submit_cart(self, cart_id):
        try:
            query = f"""
                UPDATE Cart
                SET status = 'waiting'
                WHERE id = {cart_id} AND status = 'not_sent'
            """
            self.connection.execute_query(query)
            print(f"Cart {cart_id} submitted.")
            return True
        except Exception as e:
            print("Error submitting cart:", e)
            return False

    def search_restaurants(self, customer_id, search_query):
        try:
            query = f"""
                SELECT DISTINCT R.restaurant_id, R.restaurant_name, A.city,
                    COALESCE(AVG(RT.rating), 0) AS average_rating
                FROM Customer C
                JOIN Address AC ON C.customer_id = AC.user_id
                JOIN Restaurant R ON R.address_id IN (
                    SELECT address_id FROM Address WHERE city = AC.city
                )
                JOIN Address A ON R.address_id = A.address_id
                LEFT JOIN Rating RT ON R.restaurant_id = RT.restaurant_id
                LEFT JOIN Restaurant_Keyword RK ON R.restaurant_id = RK.restaurant_id
                LEFT JOIN Keyword K ON RK.keyword_id = K.keyword_id
                WHERE C.customer_id = {customer_id}
                  AND (
                    R.restaurant_name LIKE '%{search_query}%'
                    OR K.keyword LIKE '%{search_query}%'
                  )
                GROUP BY R.restaurant_id, R.restaurant_name, A.city
                ORDER BY average_rating DESC
            """
            return self.connection.execute_query(query)
        except Exception as e:
            print("Error in search_restaurants:", e)
            return []

