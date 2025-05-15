from Connector import Connector
from Service.Customer_Service import Customer_Service

connector = Connector('root', 'Wthrw_<>1215@', 'cs202')
customer_service = Customer_Service(connector)
result = customer_service.select_by_id(id=1)

print(result)

a = customer_service.browse_menu(restaurant_id=1)
print(a)