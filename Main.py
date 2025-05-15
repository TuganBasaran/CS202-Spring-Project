from Connector import Connector
from Service.Customer_Service import Customer_Service
from Service.Manager_Service import Manager_Service

connector = Connector('root', 'password', 'CS202')
customer_service = Customer_Service(connector)
manager_service = Manager_Service(connector)

login_boolean = manager_service.login(user_name= 'ozgur.aydin', password= 'pass123')
result = manager_service.get_all_restaurants_by_manager()
keyword = manager_service.create_keyword(keyword='sustainable')

print(keyword)