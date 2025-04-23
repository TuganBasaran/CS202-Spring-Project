CREATE TABLE PhoneNumber (
                             phone_id INT PRIMARY KEY,
                             phone_name VARCHAR(50),
                             phone_number VARCHAR(20)
);

CREATE TABLE User (
                      user_id INT PRIMARY KEY,
                      username VARCHAR(50),
                      password VARCHAR(100),
                      phone_id INT,
                      FOREIGN KEY (phone_id) REFERENCES PhoneNumber(phone_id)
);

CREATE TABLE Address (
                         address_id INT PRIMARY KEY,
                         address_name VARCHAR(100),
                         address_description TEXT,
                         city VARCHAR(50),
                         user_id INT,
                         FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Customer (
                          user_id INT PRIMARY KEY,
                          registration_date DATE,
                          FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE RestaurantManager (
                                   user_id INT PRIMARY KEY,
                                   FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Restaurant (
                            restaurant_id INT PRIMARY KEY,
                            restaurant_name VARCHAR(100),
                            cuisine_type VARCHAR(50),
                            menu TEXT,
                            manager_id INT,
                            FOREIGN KEY (manager_id) REFERENCES RestaurantManager(user_id)
);

CREATE TABLE MenuItem (
                          menu_item_id INT PRIMARY KEY,
                          restaurant_id INT,
                          menu_item_name VARCHAR(100),
                          image VARCHAR(255),
                          price DECIMAL(10,2),
                          description TEXT,
                          discount DECIMAL(5,2),
                          FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

CREATE TABLE `Order` (
                         order_id INT PRIMARY KEY,
                         status VARCHAR(50),
                         order_time DATETIME,
                         customer_id INT,
                         FOREIGN KEY (customer_id) REFERENCES Customer(user_id)
);

CREATE TABLE Contains (
                          order_id INT,
                          menu_item_id INT,
                          quantity INT,
                          PRIMARY KEY (order_id, menu_item_id),
                          FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
                          FOREIGN KEY (menu_item_id) REFERENCES MenuItem(menu_item_id)
);

CREATE TABLE Ratings (
                         rating_id INT PRIMARY KEY,
                         rating INT CHECK (rating >= 1 AND rating <= 5),
                         comment TEXT,
                         order_id INT UNIQUE,
                         FOREIGN KEY (order_id) REFERENCES `Order`(order_id)
);

CREATE TABLE Keyword (
                         keyword_id INT PRIMARY KEY,
                         keyword_name VARCHAR(50)
);

CREATE TABLE Restaurant_Keyword (
                                    restaurant_id INT,
                                    keyword_id INT,
                                    PRIMARY KEY (restaurant_id, keyword_id),
                                    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
                                    FOREIGN KEY (keyword_id) REFERENCES Keyword(keyword_id)
);