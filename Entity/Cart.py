class Cart(): 
    def __init__(self, id, customer_id, restaurant_id, status, order_time):
        self.id = id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.status = status
        self.order_time = order_time
        