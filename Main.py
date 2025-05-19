from Connector import Connector
from Service.Customer_Service import Customer_Service
from Service.Manager_Service import Manager_Service

connector = Connector('root', 'test123', 'CS202')
customer_service = Customer_Service(connector)
manager_service = Manager_Service(connector)

login_boolean = manager_service.login(user_name= 'ozgur.aydin', password= 'pass123')
result = manager_service.get_restaurant_keywords(1)


for row in result:
    print(row)