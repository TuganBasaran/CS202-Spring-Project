from Connector import Connector
from Service.Customer_Service import Customer_Service

connector = Connector('root', 'test123', 'cs202')
customer_service = Customer_Service(connector)

result1 = customer_service.select_by_id(id="3")
result = customer_service.login(username='customer1',password='cust1pass')
result2 = customer_service.get_ratings(customer_id="14")
res1 = customer_service.create_rating(cart_id="5", rating="5", comment="Excelent", customer_id="14", restaurant_id="5")
print(res1)
print(result1)
print(result)
print(result2)