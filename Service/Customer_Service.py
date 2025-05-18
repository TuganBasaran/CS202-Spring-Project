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
                id = result[0][0]  # first row, first column = user_id
                self.user = Customer(id, username, password)
                return result
            return 0
        except Exception as e:
            print("Login failed")
            print(e)

    def get_ratings(self, customer_id):
        # Çıktı düzenlenmeli
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
            query = f"""
                INSERT INTO Rating (cart_id, rating, comment, customer_id, restaurant_id)
                VALUES ({cart_id}, {rating}, '{comment}', {customer_id}, {restaurant_id})
            """
            self.connection.execute_query(query)
            print("Created rating")
            return True
        except Exception as e:
            print("Error while creating rating:", e)
            return e

    def select_by_id(self, id):
        query = f'SELECT * FROM User WHERE user_id= {id}'
        result = self.connection.execute_query(query)
        return result


