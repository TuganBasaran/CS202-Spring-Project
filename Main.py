from Connector import Connector
from Service.Customer_Service import Customer_Service
from Service.Manager_Service import Manager_Service

connector = Connector('root', 'password', 'CS202')
customer_service = Customer_Service(connector)

print(customer_service.get_addresses())