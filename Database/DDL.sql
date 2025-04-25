CREATE DATABASE IF NOT EXISTS CS202;
USE CS202;

-- USERS (hem müşteri hem restoran yöneticisi olabilir)
CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(64) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL
);

-- CUSTOMER
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    FOREIGN KEY (customer_id) REFERENCES User(user_id)
);

CREATE TABLE Restaurant_Manager (
     manager_id INT PRIMARY KEY,
    FOREIGN KEY (manager_id) REFERENCES User(user_id)
);



-- RESTAURANT
CREATE TABLE Restaurant (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_name VARCHAR(64) NOT NULL,
    cuisine_type ENUM('Indian', 'Asian', 'European', 'American', 'African', 'Turkish'),
    manager_id INT NOT NULL,
    address_id INT NOT NULL,
    FOREIGN KEY (address_id) REFERENCES Address(address_id),
    FOREIGN KEY (manager_id) REFERENCES User(user_id)
);

-- ADDRESS (bir kullanıcı birden fazla adres sahibi olabilir)
CREATE TABLE Address (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL, -- Restaurant adresi eklerken user_id olarak restaurant manager girilecek
    address_name VARCHAR(64),
    address VARCHAR(255) NOT NULL,
    city VARCHAR(64) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- PHONE NUMBER
CREATE TABLE Phone_Number (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    phone_number CHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- MENU ITEM
CREATE TABLE Menu_Item (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    image VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    price FLOAT NOT NULL,
    restaurant_id INT NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

-- OPTIONAL DISCOUNT TABLE
CREATE TABLE Discount (
    id INT PRIMARY KEY AUTO_INCREMENT,
    menu_item_id INT NOT NULL,
    discount_rate DOUBLE NOT NULL,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (menu_item_id) REFERENCES Menu_Item(id)
);

CREATE TABLE Keyword(
    keyword_id INT PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(20)
);

-- KEYWORDS FOR RESTAURANTS
CREATE TABLE Restaurant_Keyword (
    keyword_id INT,
    restaurant_id INT,
    PRIMARY KEY (keyword_id, restaurant_id),
    FOREIGN KEY (keyword_id) REFERENCES Keyword(keyword_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

-- CART (ORDER)
CREATE TABLE Cart (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    status ENUM('waiting','accepted') NOT NULL,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

-- CART ITEM
CREATE TABLE Contains (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES Cart(id),
    FOREIGN KEY (menu_item_id) REFERENCES Menu_Item(id)
);

-- RATINGS
CREATE TABLE Rating (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rating INT CHECK (rating >= 1 AND rating <= 5) NOT NULL,
    comment VARCHAR(255),
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    cart_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    FOREIGN KEY (cart_id) REFERENCES Cart(id)
);