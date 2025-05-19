class  Menu_Item(): 
    def __init__(self, id, name, image, description, price, restaurant_id, discount_rate= 0):
        self.id = id 
        self.name = name 
        self.image = image 
        self.description = description
        self.price = price 
        self.discount_rate= discount_rate
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return f"Menu_Item(id={self.id}, name={self.name}, image={self.image}, description={self.description}, price={self.price}, restaurant_id={self.restaurant_id})"
    
    def __str__(self):
        return f"Menu_Item(id={self.id}, name={self.name}, price={self.price})"