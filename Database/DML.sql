-- USERS
INSERT INTO User (user_id, user_name, password) VALUES
(1, 'ozgur.aydin', 'pass123'),
(2, 'melis.kaya', 'meliskaya456'),
(3, 'emre.ozan', 'ozanemre789'),
(10, 'customer1', 'cust1pass'),
(11, 'customer2', 'cust2pass'),
(12, 'customer3', 'cust3pass'),
(13, 'customer4', 'cust4pass'),
(14, 'customer5', 'cust5pass');

-- RESTAURANT MANAGER
INSERT INTO Restaurant_Manager (manager_id) VALUES
(1),
(2),
(3);

-- CUSTOMER
INSERT INTO Customer (customer_id) VALUES
(10),
(11),
(12),
(13),
(14);

-- ADDRESS
INSERT INTO Address (address_id, user_id, address_name, address, city) VALUES
(1, 1, 'Main Branch', 'Atasehir Mah. No:10', 'Istanbul'),
(2, 2, 'Spice Hub', 'Kadikoy Mah. No:25', 'Istanbul'),
(3, 3, 'Burger Spot', 'Bornova Cad. No:15', 'Izmir'),
(4, 1, 'Mamma Mia HQ', 'Bakirkoy Sok. No:5', 'Istanbul'),
(5, 2, 'Wok Kitchen', 'Cankaya Sk. No:8', 'Ankara'),
(12, 10, 'home12', 'çekmeköy', 'Istanbul');


-- PHONE NUMBER
INSERT INTO Phone_Number (id, user_id, phone_number) VALUES
(1, 1, '+905001112233'),
(2, 2, '+905002223344'),
(3, 3, '+905003334455'),
(4, 10, '+905004445566'),
(5, 11, '+905005556677'),
(6, 12, '+905006667788'),
(7, 13, '+905007778899'),
(8, 14, '+905008889900');

-- RESTAURANT
INSERT INTO Restaurant (restaurant_id, restaurant_name, cuisine_type, manager_id, address_id) VALUES
(1, 'Sofra Anadolu', 'Turkish', 1, 1),
(2, 'Spice Route', 'Indian', 2, 2),
(3, 'Burger District', 'American', 3, 3),
(4, 'Mamma Mia', 'European', 1, 4),
(5, 'Wok Wok', 'Asian', 2, 5);

-- KEYWORDS (Önce manager_id OLMAYANLAR)
INSERT INTO Keyword (keyword_id, keyword) VALUES
(1, 'fast'),
(2, 'home-made'),
(3, 'grill'),
(4, 'vegan'),
(5, 'dessert');

-- KEYWORDS (manager_id OLANLAR)
INSERT INTO Keyword (keyword_id, keyword, manager_id) VALUES
(6, 'organic', 1),
(7, 'family', 2),
(8, 'quick', 3),
(9, 'budget', 1),
(10, 'luxury', 2);

-- RESTAURANT_KEYWORD
INSERT INTO Restaurant_Keyword (keyword_id, restaurant_id) VALUES
(1, 1),
(3, 2),
(5, 3),
(2, 4),
(4, 5),
(6, 1),
(7, 2),
(8, 3),
(9, 4),
(10, 5);

-- MENU ITEM
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

-- DISCOUNT
INSERT INTO Discount (id, discount_rate, start_date, end_date) VALUES
(1, 10.0, '2024-05-01', '2024-05-15'),
(2, 15.5, '2024-06-01', '2024-06-20'),
(3, 20.0, '2024-07-10', '2024-07-25'),
(4, 5.0, '2024-08-01', '2024-08-10'),
(5, 12.0, '2024-09-01', '2024-09-15');

-- HAS_DISCOUNT
INSERT INTO Has_Discount (menu_item_id, discount_id) VALUES
(1, 1),
(3, 2),
(5, 3),
(7, 4),
(9, 5);

-- CART
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

-- CONTAINS (id KALDIRILDI, sadece cart_id, menu_item_id, quantity)
INSERT INTO Contains (cart_id, menu_item_id, quantity) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 3, 2),
(2, 4, 1),
(3, 5, 1),
(3, 6, 2),
(4, 7, 1),
(4, 8, 2),
(5, 9, 1),
(5, 10, 1),
(6, 2, 2),
(6, 1, 1),
(7, 5, 1),
(7, 6, 1),
(8, 13, 2),
(8, 14, 1),
(9, 7, 2),
(9, 9, 1),
(10, 10, 2),
(10, 11, 1),
(11, 13, 2),
(11, 14, 1),
(12, 1, 1),
(12, 3, 1),
(13, 5, 2),
(13, 8, 1),
(14, 9, 1),
(14, 11, 2),
(15, 6, 2),
(15, 7, 1);

-- RATING
-- DDL'de: id (AI), rating, comment, cart_id, customer_id, restaurant_id, created_at

-- Örnek: Restaurant 1 - Sofra Anadolu (Turkish cuisine)
INSERT INTO Rating (rating, comment, cart_id, customer_id, restaurant_id, created_at) VALUES
(5, 'Exceptional Turkish cuisine! The lamb kebabs were perfectly seasoned.', 1, 10, 1, '2024-03-10 14:25:10'),
(4, 'Great authentic flavors, though service was a bit slow.', 6, 12, 1, '2024-03-30 18:12:33'),
(5, 'Best baklava I''ve ever had outside of Istanbul!', 12, 11, 1, '2024-04-12 20:45:22'),
(3, 'Good food but portion sizes were smaller than expected.', 1, 10, 1, '2024-03-15 12:30:45'),
(5, 'The mezze platter was outstanding - fresh and flavorful.', 6, 12, 1, '2024-04-01 19:55:18'),
(4, 'Lovely atmosphere and very tasty traditional dishes.', 12, 11, 1, '2024-04-13 13:20:07'),
(5, 'Their pide bread is absolutely incredible!', 1, 10, 1, '2024-03-20 21:10:33'),
(4, 'Delicious food and friendly staff, will definitely return.', 6, 12, 1, '2024-04-02 17:40:12'),
(3, 'Food was good but arrived lukewarm.', 12, 11, 1, '2024-04-14 18:05:39'),
(5, 'The Turkish tea and desserts were exceptional - truly authentic!', 1, 10, 1, '2024-03-25 16:50:28');

-- Restaurant 2 - Spice Route (Indian cuisine)
INSERT INTO Rating (rating, comment, cart_id, customer_id, restaurant_id, created_at) VALUES
(5, 'The butter chicken had perfect spice balance and rich flavor.', 3, 11, 2, '2024-03-19 19:15:22'),
(4, 'Excellent naan bread and flavorful curries.', 7, 13, 2, '2024-04-02 20:35:41'),
(5, 'Most authentic Indian food I''ve found in the city!', 15, 14, 2, '2024-04-16 18:22:17'),
(3, 'Good flavors but too spicy for my preference.', 3, 11, 2, '2024-03-22 13:40:55'),
(4, 'Great vegetarian options with authentic tastes.', 7, 13, 2, '2024-04-03 19:10:33'),
(5, 'The tandoori dishes were cooked to perfection.', 15, 14, 2, '2024-04-17 20:45:29'),
(2, 'Delivery was very late and food was cold on arrival.', 3, 11, 2, '2024-03-25 21:05:18'),
(4, 'Generous portions and excellent value for money.', 7, 13, 2, '2024-04-05 12:30:22'),
(5, 'Their biryani is simply outstanding!', 15, 14, 2, '2024-04-18 17:55:43'),
(3, 'Tasty food but some items were missing from our order.', 3, 11, 2, '2024-03-28 18:20:11');

-- Restaurant 3 - Burger District (American cuisine)
INSERT INTO Rating (rating, comment, cart_id, customer_id, restaurant_id, created_at) VALUES
(5, 'Juiciest burgers in town! The beef was cooked perfectly.', 2, 10, 3, '2024-03-16 18:22:31'),
(4, 'Great burgers but fries were slightly soggy.', 9, 14, 3, '2024-04-07 19:10:24'),
(5, 'The bacon cheeseburger was simply incredible!', 13, 12, 3, '2024-04-13 21:30:19'),
(3, 'Decent burgers but nothing particularly special.', 2, 10, 3, '2024-03-18 14:25:47'),
(5, 'Best milkshakes ever - perfect with their delicious burgers!', 9, 14, 3, '2024-04-08 17:45:33'),
(4, 'Quality ingredients and generous portions.', 13, 12, 3, '2024-04-14 18:55:16'),
(5, 'Their special sauce makes all the difference - amazing!', 2, 10, 3, '2024-03-22 20:15:29'),
(2, 'Long wait time and incorrect order.', 9, 14, 3, '2024-04-09 21:40:52'),
(4, 'Consistent quality every time I order.', 13, 12, 3, '2024-04-15 13:25:43'),
(3, 'Good taste but my burger was overcooked.', 2, 10, 3, '2024-03-25 15:35:19');

-- Restaurant 4 - Mamma Mia (European cuisine)
INSERT INTO Rating (rating, comment, cart_id, customer_id, restaurant_id, created_at) VALUES
(5, 'The pasta was perfectly al dente with amazing flavor!', 5, 12, 4, '2024-03-26 19:05:22'),
(4, 'Excellent risotto and great wine selection.', 10, 14, 4, '2024-04-09 20:15:43'),
(5, 'Their wood-fired pizza is the best in town!', 14, 13, 4, '2024-04-14 18:45:31'),
(3, 'Good food but portions could be more generous.', 5, 12, 4, '2024-03-27 14:30:19'),
(5, 'The tiramisu was absolutely heavenly!', 10, 14, 4, '2024-04-10 19:22:55'),
(4, 'Lovely ambiance and authentic Italian flavors.', 14, 13, 4, '2024-04-15 21:10:27'),
(5, 'Their seafood pasta had the freshest ingredients.', 5, 12, 4, '2024-03-29 18:40:33'),
(2, 'Food arrived cold and presentation was messy.', 10, 14, 4, '2024-04-11 17:50:42'),
(4, 'The gnocchi was soft and pillowy with delicious sauce.', 14, 13, 4, '2024-04-16 20:35:18'),
(5, 'Best Italian food experience outside of Italy!', 5, 12, 4, '2024-03-30 15:25:51');

-- Restaurant 5 - Wok Wok (Asian cuisine)
INSERT INTO Rating (rating, comment, cart_id, customer_id, restaurant_id, created_at) VALUES
(5, 'The pad thai was bursting with authentic flavors!', 4, 11, 5, '2024-03-23 20:10:25'),
(4, 'Excellent dim sum selection - everything tasted fresh.', 8, 13, 5, '2024-04-05 18:30:47'),
(5, 'The ramen broth was incredibly rich and flavorful.', 11, 10, 5, '2024-04-11 21:15:33'),
(3, 'Good food but some dishes were too salty.', 4, 11, 5, '2024-03-24 15:45:19'),
(5, 'Their sushi was extremely fresh and expertly prepared.', 8, 13, 5, '2024-04-06 19:55:22'),
(4, 'The Korean fried chicken had perfect crispiness.', 11, 10, 5, '2024-04-12 17:20:41'),
(5, 'Amazing variety of dishes from across Asia.', 4, 11, 5, '2024-03-26 20:35:37'),
(2, 'Very long delivery time and food arrived cold.', 8, 13, 5, '2024-04-07 21:40:55'),
(4, 'The dumplings were juicy and full of flavor.', 11, 10, 5, '2024-04-13 14:15:29'),
(5, 'Their Malaysian curry was rich and perfectly spiced!', 4, 11, 5, '2024-03-28 18:50:12');

-- Ekstra test dataları (id otomatik artan olduğundan gerek yok, ama istersen aşağıdaki gibi devam edebilirsin):
-- Örnek: 
-- INSERT INTO Rating (rating, comment, cart_id, customer_id, restaurant_id, created_at) VALUES
-- (5, 'Excellent taste and fast delivery!', 1, 10, 1, '2024-03-10 14:30:00');