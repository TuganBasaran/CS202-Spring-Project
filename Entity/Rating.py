class Rating(): 
    def __init__(self, id, rating, comment, cart_id, customer, restaurant, created_at, menu_items):
        self.id = id 
        self.rating = rating
        self.comment = comment
        self.cart_id = cart_id
        self.customer = customer
        self.restaurant = restaurant
        self.created_at = created_at
        self.menu_items = menu_items

    def __repr__(self):
        return (f"Rating(id={self.id}, rating={self.rating}, comment='{self.comment}', "
                f"cart_id={self.cart_id}, customer='{self.customer}', "
                f"restaurant={self.restaurant}, created_at='{self.created_at}')")

    def __str__(self):
        return (f"Rating: {self.rating} - '{self.comment}' by {self.customer} "
                f"on {self.created_at}")
