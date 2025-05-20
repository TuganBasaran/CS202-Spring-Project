from Connector import Connector
from Service.Customer_Service import Customer_Service
from Service.Manager_Service import Manager_Service

connector = Connector('root', 'test123', 'cs202')
customer_service = Customer_Service(connector)
