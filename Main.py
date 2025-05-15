from Connector import Connector
from Service.Customer_Service import Customer_Service
from Service.Manager_Service import Manager_Service

connector = Connector('root', 'password', 'CS202')
customer_service = Customer_Service(connector)
manager_service = Manager_Service(connector)

result = manager_service.login(user_name= 'ozgur.aydin', password= 'pass123')

result = customer_service.search_restaurants(name= 'Burger District')

print(result)