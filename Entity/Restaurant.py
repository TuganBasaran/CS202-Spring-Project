class Restaurant(): 
    def __init__(self, restaurant_id, restaurant_name, cuisine_type, manager_id, address_id):
        self.restaurant_id = restaurant_id
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type 
        self.manager_id = manager_id
        self.address_id = address_id 

    def __repr__(self):
        return f"Restaurant(id={self.restaurant_id}, name={self.restaurant_name}, cuisine_type={self.cuisine_type}, manager_id= {self.manager_id}, address_id= {self.address_id})"