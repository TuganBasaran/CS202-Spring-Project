class Phone_Number(): 
    def __init__(self, id, user_id, phone_number):
        self.id = id 
        self.user_id = user_id 
        self.phone_number = phone_number

    def __repr__(self):
        return f"Phone_Number(id={self.id}, user_id={self.user_id}, phone_number='{self.phone_number}')"

    def __str__(self):
        return f"Phone Number: {self.phone_number} (User ID: {self.user_id})"