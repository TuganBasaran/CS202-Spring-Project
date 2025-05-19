class Restaurant(): 
    def __init__(self, restaurant_id, restaurant_name, cuisine_type, manager, address):
        self.restaurant_id = restaurant_id
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type 
        self.manager = manager
        self.address = address
        

    def __repr__(self):
        return f"Restaurant(id={self.restaurant_id}, name={self.restaurant_name}, cuisine_type={self.cuisine_type}, manager= {self.manager}, address= {self.address}"