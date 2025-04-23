# noinspection SqlCurrentSchemaInspectionForFile

SHOW DATABASES;

CREATE DATABASE IF NOT EXISTS CS202;

USE CS202;

SHOW TABLES;

CREATE TABLE IF NOT EXISTS User (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(64) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL,
    registration_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Customer (
    customer_id INT NOT NULL  REFERENCES User(user_id),
    PRIMARY KEY(customer_id)
);


CREATE TABLE IF NOT EXISTS Restaurant_Manager (
    manager_id INT NOT NULL REFERENCES User(user_id)
);

CREATE TABLE IF NOT EXISTS Address(
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT REFERENCES Restaurant(restaurant_id),
    address_name VARCHAR(64) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    user_id INT REFERENCES User(user_id)
);

CREATE TABLE IF NOT EXISTS Restaurant (
    restaurant_id INT PRIMARY KEY,
    restaurant_name VARCHAR(64),
    cuisine_type ENUM('Indian', 'Asian', 'European', 'American', 'African', 'Turkish'),
    manager_id INT REFERENCES Restaurant_Manager(manager_id),
    address_id INT REFERENCES Address(address_id)
);

CREATE TABLE IF NOT EXISTS Menu_Item (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    image VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    discount DOUBLE,
    restaurant_id INT REFERENCES Restaurant(restaurant_id)
);

CREATE TABLE IF NOT EXISTS `order` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT REFERENCES Restaurant(restaurant_id),
    customer_id INT REFERENCES Customer(customer_id)
);

CREATE TABLE IF NOT EXISTS Phone_Number (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    user_id INT REFERENCES User(user_id),
    restaurant_id INT REFERENCES  Restaurant(restaurant_id)
);

CREATE TABLE IF NOT EXISTS Rating(
    id INT PRIMARY KEY AUTO_INCREMENT,
    rating INT CHECK (rating >= 0 AND rating <= 5) NOT NULL,
    comment VARCHAR(255),
    order_id INT REFERENCES `order`(id),
    restaurant_id INT REFERENCES Restaurant(restaurant_id),
    customer_id INT REFERENCES Customer(customer_id)
    );
