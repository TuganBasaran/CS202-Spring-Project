INSERT INTO User (user_id, user_name, password) VALUES
(1, 'ozgur.aydin', 'pass123'),
(2, 'melis.kaya', 'meliskaya456'),
(3, 'emre.ozan', 'ozanemre789'),
(10, 'customer1', 'cust1pass'),
(11, 'customer2', 'cust2pass'),
(12, 'customer3', 'cust3pass'),
(13, 'customer4', 'cust4pass'),
(14, 'customer5', 'cust5pass');

INSERT INTO Restaurant_Manager (manager_id) VALUES
(1),
(2),
(3);

INSERT INTO Customer (customer_id) VALUES
(10),
(11),
(12),
(13),
(14);

INSERT INTO Address (address_id, user_id, address_name, address, city) VALUES
(1, 1, 'Main Branch', 'Atasehir Mah. No:10', 'Istanbul'),
(2, 2, 'Spice Hub', 'Kadikoy Mah. No:25', 'Istanbul'),
(3, 3, 'Burger Spot', 'Bornova Cad. No:15', 'Izmir'),
(4, 1, 'Mamma Mia HQ', 'Bakirkoy Sok. No:5', 'Istanbul'),
(5, 2, 'Wok Kitchen', 'Cankaya Sk. No:8', 'Ankara');

INSERT INTO Phone_Number (id, user_id, phone_number) VALUES
(1, 1, '+905001112233'),
(2, 2, '+905002223344'),
(3, 3, '+905003334455'),
(4, 10, '+905004445566'),
(5, 11, '+905005556677'),
(6, 12, '+905006667788'),
(7, 13, '+905007778899'),
(8, 14, '+905008889900');

INSERT INTO Restaurant (restaurant_id, restaurant_name, cuisine_type, manager_id, address_id) VALUES
(1, 'Sofra Anadolu', 'Turkish', 1, 1),
(2, 'Spice Route', 'Indian', 2, 2),
(3, 'Burger District', 'American', 3, 3),
(4, 'Mamma Mia', 'European', 1, 4),
(5, 'Wok Wok', 'Asian', 2, 5);

INSERT INTO Keyword (keyword_id, keyword) VALUES
(1, 'fast'),
(2, 'home-made'),
(3, 'grill'),
(4, 'vegan'),
(5, 'dessert');

INSERT INTO Restaurant_Keyword (keyword_id, restaurant_id) VALUES
(1, 1),
(3, 2),
(5, 3),
(2, 4),
(4, 5);

INSERT INTO Menu_Item (id, name, image, description, price, restaurant_id) VALUES
(1, 'Grilled Chicken Shawarma', 'image1.jpg', 'Tender chicken breast wrapped in spices and grilled to perfection.', 107.86, 1),
(2, 'Spaghetti Carbonara', 'image2.jpg', 'Classic Italian pasta with pancetta, egg, and parmesan.', 91.16, 1),
(3, 'Sushi Platter', 'image3.jpg', 'Assorted nigiri and rolls served with soy sauce and wasabi.', 141.35, 1),
(4, 'Falafel Wrap', 'image4.jpg', 'Crispy chickpea balls wrapped with tahini and fresh vegetables.', 69.40, 2),
(5, 'Beef Burger', 'image5.jpg', 'Juicy beef patty with cheddar, lettuce, tomato, and house sauce.', 167.51, 2),
(6, 'Pad Thai', 'image6.jpg', 'Stir-fried rice noodles with shrimp, tofu, and peanuts.', 115.20, 2),
(7, 'Margherita Pizza', 'image7.jpg', 'Wood-fired pizza with fresh mozzarella and basil.', 98.75, 3),
(8, 'Butter Chicken', 'image8.jpg', 'Creamy tomato-based curry with tender chicken pieces.', 134.00, 3),
(9, 'Veggie Burrito', 'image9.jpg', 'Tortilla stuffed with beans, rice, salsa, and grilled veggies.', 122.55, 3),
(10, 'BBQ Ribs', 'image10.jpg', 'Slow-cooked pork ribs glazed with BBQ sauce.', 150.00, 4),
(11, 'Greek Salad', 'image11.jpg', 'Fresh cucumbers, olives, feta cheese, and olive oil dressing.', 88.80, 4),
(12, 'Chicken Caesar Wrap', 'image12.jpg', 'Grilled chicken, romaine, parmesan, and Caesar dressing.', 175.00, 4),
(13, 'Tom Yum Soup', 'image13.jpg', 'Spicy Thai soup with shrimp, mushrooms, and lemongrass.', 92.30, 5),
(14, 'Beef Tacos', 'image14.jpg', 'Soft tacos filled with spiced beef, salsa, and sour cream.', 146.50, 5),
(15, 'Chocolate Lava Cake', 'image15.jpg', 'Warm chocolate cake with a gooey center, served with ice cream.', 134.22, 5);

INSERT INTO Cart (id, customer_id, restaurant_id, status, order_time) VALUES
(1, 10, 1, 'waiting', '2024-03-08 12:20:00'),
(2, 10, 3, 'accepted', '2024-03-15 14:55:00'),
(3, 11, 2, 'accepted', '2024-03-18 11:45:00'),
(4, 11, 5, 'waiting', '2024-03-22 19:30:00'),
(5, 12, 4, 'accepted', '2024-03-25 16:40:00'),
(6, 12, 1, 'waiting', '2024-03-29 13:10:00'),
(7, 13, 2, 'accepted', '2024-04-01 17:25:00'),
(8, 13, 5, 'waiting', '2024-04-04 20:15:00'),
(9, 14, 3, 'accepted', '2024-04-06 21:50:00'),
(10, 14, 4, 'waiting', '2024-04-08 22:40:00'),
(11, 10, 5, 'accepted', '2024-04-10 14:05:00'),
(12, 11, 1, 'waiting', '2024-04-11 15:50:00'),
(13, 12, 3, 'accepted', '2024-04-12 18:00:00'),
(14, 13, 4, 'waiting', '2024-04-13 20:30:00'),
(15, 14, 2, 'accepted', '2024-04-14 21:10:00');

INSERT INTO Contains (id, cart_id, menu_item_id, quantity) VALUES
(1, 1, 1, 2),
(2, 1, 2, 1),
(3, 2, 3, 2),
(4, 2, 4, 1),
(5, 3, 5, 1),
(6, 3, 6, 2),
(7, 4, 7, 1),
(8, 4, 8, 2),
(9, 5, 9, 1),
(10, 5, 10, 1),
(11, 6, 2, 2),
(12, 6, 1, 1),
(13, 7, 5, 1),
(14, 7, 6, 1),
(15, 8, 13, 2),
(16, 8, 14, 1),
(17, 9, 7, 2),
(18, 9, 9, 1),
(19, 10, 10, 2),
(20, 10, 11, 1),
(21, 11, 13, 2),
(22, 11, 14, 1),
(23, 12, 1, 1),
(24, 12, 3, 1),
(25, 13, 5, 2),
(26, 13, 8, 1),
(27, 14, 9, 1),
(28, 14, 11, 2),
(29, 15, 6, 2),
(30, 15, 7, 1);


INSERT INTO Rating (id, rating, comment, cart_id, created_at) VALUES
(1, 5, 'Amazing shawarma, will order again!', 2, '2024-03-15 16:55:00'),
(2, 4, 'Fresh sushi, fast delivery.', 3, '2024-03-18 13:45:00'),
(3, 5, 'Excellent service and delicious food.', 5, '2024-03-25 18:50:00'),
(4, 5, 'Great flavors, loved the Pad Thai.', 7, '2024-04-01 19:25:00'),
(5, 3, 'Tacos were a bit dry, but still good.', 9, '2024-04-06 23:00:00'),
(6, 5, 'Best salad I have ever eaten.', 11, '2024-04-10 16:10:00'),
(7, 4, 'Good pizza, but took some time.', 13, '2024-04-12 19:10:00'),
(8, 5, 'Amazing chocolate lava cake!', 15, '2024-04-14 22:30:00');
