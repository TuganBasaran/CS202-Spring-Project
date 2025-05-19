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

    def add_address(self, address_name, address, city):
        user_id = self.user.user_id
        try:
            query = (f"INSERT INTO Address (user_id, address_name, address, city)"
                     f"VALUES ({user_id}, '{address_name}', '{address}', '{city}')")
            self.connection.execute_query(query)
            print("Added address")
            return True
        except Exception as e:
            print("Error while adding address:", e)
            return e

    def add_phone_number(self, phone_number):
        user_id = self.user.user_id
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



    def select_by_id(self, id):
        query = f'SELECT * FROM User WHERE user_id= {id}'
        result = self.connection.execute_query(query)
        return result