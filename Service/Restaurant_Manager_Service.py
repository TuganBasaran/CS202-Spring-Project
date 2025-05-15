class Restaurant_Manager_Service(): 
    def __init__(self, connection):
        self.connection = connection 

    def create_restaurant(self, name, location, cuisine_type):
        query = f'INSERT INTO Restaurant (restaurant_name, location, cuisine_type) VALUES ("{name}", "{location}", "{cuisine_type}")'
        self.connection.execute_query(query)
        self.connection.commit()
        return "Restaurant created successfully."
    
    def update_restaurant(self, restaurant_id, name=None, location=None, cuisine_type=None):
        query = f'UPDATE Restaurant SET '
        if name:
            query += f'restaurant_name = "{name}", '
        if location:
            query += f'location = "{location}", '
        if cuisine_type:
            query += f'cuisine_type = "{cuisine_type}" '
        query = query.rstrip(', ')
        query  += f"Where restaurant_id = {restaurant_id}"
        self.connection.execute_query(query)
        self.connection.commit()
        return "Restaurant updated successfully."
    
    def delete_restaurant(self, restaurant_id):
        query = f'DELETE FROM Restaurant WHERE restaurant_id = {restaurant_id}'
        self.connection.execute_query(query)
        self.connection.commit()
        return "Restaurant deleted successfully."
    
    ##################################################################

    def add_menu_item(self, restaurant_id, item_name, price):
        query = f'INSERT INTO Menu_Item (restaurant_id, item_name, price) VALUES ({restaurant_id}, "{item_name}", {price})'
        self.connection.execute_query(query)
        self.connection.commit()
        return "Menu item added successfully."  
    
    def update_menu_item(self, item_id, item_name=None, price=None):
        query = f'UPDATE Menu_Item SET '
        if item_name:
            query += f'item_name = "{item_name}", '
        if price:
            query += f'price = {price} '
        query = query.rstrip(', ')
        query  += f"Where item_id = {item_id}"
        self.connection.execute_query(query)
        self.connection.commit()
        return "Menu item updated successfully."
    
    def delete_menu_item(self, item_id):
        query = f'DELETE FROM Menu_Item WHERE item_id = {item_id}'
        self.connection.execute_query(query)
        self.connection.commit()
        return "Menu item deleted successfully."
    
    
        ##################################################################

    
    def view_orders(self, restaurant_id):
        query = f'SELECT * FROM Orders WHERE restaurant_id = {restaurant_id}'
        result = self.connection.execute_query(query)
        return result
        
    def define_discount(self, item_id, start_date, end_date, discount_rate):
        query = f'INSERT INTO Discount (item_id, start_date, end_date, discount_rate) VALUES ({item_id}, "{start_date}", "{end_date}", {discount_rate})'
        self.connection.execute_query(query)
        self.connection.commit()
        return "Discount defined successfully."
    
    def update_discount(self, discount_id, start_date=None, end_date=None, discount_rate=None):
        query = f'UPDATE Discount SET '
        if start_date:
            query += f'start_date = "{start_date}", '
        if end_date:
            query += f'end_date = "{end_date}", '
        if discount_rate:
            query += f'discount_rate = {discount_rate} '
        query = query.rstrip(', ')
        query  += f"Where discount_id = {discount_id}"
        self.connection.execute_query(query)
        self.connection.commit()
        return "Discount updated successfully."
    
    def delete_discount(self, discount_id):
        query = f'DELETE FROM Discount WHERE discount_id = {discount_id}'
        self.connection.execute_query(query)
        self.connection.commit()
        return "Discount deleted successfully." 
    

    ##################################################################
    
    def accept_order(self, order_id):
        query = f'UPDATE Orders SET status = "Accepted" WHERE order_id = {order_id}'
        self.connection.execute_query(query)
        self.connection.commit()
        return "Order accepted successfully."

    def reject_order(self, order_id):
        query = f'UPDATE Orders SET status = "Rejected" WHERE order_id = {order_id}'
        self.connection.execute_query(query)
        self.connection.commit()
        return "Order rejected successfully."