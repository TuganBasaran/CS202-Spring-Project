class Rating(): 
    def __init__(self, id, rating, comment, cart_id, restaurant_id, created_at):
        self.id = id 
        self.rating = rating
        self.comment = comment
        self.cart_id = cart_id
        self.restaurant_id = restaurant_id
        self.created_at = created_at
        