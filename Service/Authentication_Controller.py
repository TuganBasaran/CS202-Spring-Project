class Authentication_Controller: 
    def __init__(self, connection):
        self.connection = connection 

    def login(self):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        user_type = self.get_user_type(name, password)
        return user_type

    def is_manager(self, user_id):
        query = "SELECT manager_id FROM Restaurant_Manager WHERE manager_id = %s"
        result = self.connection.execute_query(query, (user_id,))
        return result.fetchone() is not None

    def get_user_type(self, name, password):
        query = "SELECT user_id FROM User WHERE user_name = %s AND password = %s"
        result = self.connection.execute_query(query, (name, password))
        user = result.fetchone()

        if user is None:
            print("Wrong username or password")
            return False

        user_id = user[0]

        if self.is_manager(user_id):
            print("Welcome Manager " + name)
            return "Manager"
        else:
            print("Welcome Customer " + name)
            return "Customer"
        
    def register(self):
        name = input("Enter your username: ")
        password = input("Enter your password: ") 
        phone = input("Enter your phone number: ")
        address = input("Enter your address: ")
        city = input("Enter your city: ")
        address_name = input("Enter address name (e.g. Home, Work): ")

        user_query = "INSERT INTO User (user_name, password) VALUES (%s, %s)"
        self.connection.execute_query(user_query, (name, password))
        self.connection.commit()

        user_id_query = "SELECT user_id FROM User WHERE user_name = %s"
        result = self.connection.execute_query(user_id_query, (name,))
        user = result.fetchone()
        if not user:
            print("User registration failed.")
            return False
        user_id = user[0]

        phone_query = "INSERT INTO Phone_Number (user_id, phone_number) VALUES (%s, %s)"
        self.connection.execute_query(phone_query, (user_id, phone))

        address_query = "INSERT INTO Address (user_id, address_name, address, city) VALUES (%s, %s, %s, %s)"
        self.connection.execute_query(address_query, (user_id, address_name, address, city))

        self.connection.commit()
        print("User registered successfully.")
        return True
    
    def logout_user():
        print("User logged out successfully.")
        return True
       