# CS202 Restaurant Management System

## Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [Backend: Entity Classes](#backend-entity-classes)
- [Backend: Service Classes](#backend-service-classes)
- [Frontend: HTML Templates](#frontend-html-templates)
- [Running the Project](#running-the-project)
- [How to Develop the Customer Side (Step by Step)](#how-to-develop-the-customer-side-step-by-step)
- [Example Customer Features](#example-customer-features)
- [Tips for Beginners](#tips-for-beginners)

---

## Introduction

This project is a comprehensive restaurant management and food ordering system for restaurant managers and customers. The manager side is fully implemented; this guide will help you understand the codebase and learn how to develop the customer side, even if you are new to Python and Flask.

---

## Project Overview

- **Managers:**
  - Can add and manage restaurants, menus, and discounts
  - Can view and process orders
  - Can view analytics (sales, top customers, etc.)
- **Customers** (to be implemented):
  - Can browse restaurants and menus
  - Can place orders and view order history
  - Can rate restaurants

---

## Technology Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML, CSS, Jinja2 (Flask's template engine)
- **Database:** MySQL

---

## Project Structure

```
CS202-Spring-Project/
├── app.py                  # Main Flask application (routes, initialization)
├── Connector.py            # Database connection helper class
├── Entity/                 # Data model classes (Python)
│   ├── Address.py
│   ├── Cart.py
│   ├── Discount.py
│   ├── Keyword.py
│   ├── Menu_Item.py
│   ├── Rating.py
│   ├── Restaurant.py
│   └── User/
│       ├── Customer.py
│       ├── Restaurant_Manager.py
│       └── User.py
├── Service/                # Business logic classes
│   ├── Customer_Service.py
│   └── Manager_Service.py
├── templates/              # HTML templates (Jinja2)
│   ├── index.html
│   └── manager/
│       ├── add_discount.html
│       ├── add_menu_item.html
│       ├── discounts.html
│       ├── manager_dashboard.html
│       ├── menu_stats.html
│       ├── orders.html
│       ├── restaurant_keywords.html
│       └── restaurant_page.html
├── Database/DDL.sql        # Database schema
├── Database/DML.sql        # Sample data
└── requirements.txt        # Python dependencies
```

---

## Database Design

- **User**: All users (managers and customers)
- **Restaurant_Manager**: Managers (derived from User)
- **Customer**: Customers (derived from User)
- **Restaurant**: Restaurant information
- **Menu_Item**: Menu items for each restaurant
- **Cart**: Orders (one order per customer)
- **Contains**: Items in each cart
- **Discount**: Discount campaigns
- **Has_Discount**: Which menu has which discount
- **Rating**: Customer feedback
- **Keyword**: Restaurant tags
- **Restaurant_Keyword**: Which restaurant has which tag
- **Address**: Address information

---

## Backend: Entity Classes

These are Python classes that represent database tables. They are located in the `Entity/` folder.

### Example: `Menu_Item.py`

```python
class Menu_Item():
    def __init__(self, id, name, image, description, price, restaurant_id):
        self.id = id
        self.name = name
        self.image = image
        self.description = description
        self.price = price
        self.restaurant_id = restaurant_id
        self.has_discount = False
        self.discount_rate = 0
        self.original_price = price
```

- **Tip:** All entity classes are simple containers for data. You can add more properties if needed for the customer side.

### Example: `Cart.py`

```python
class Cart:
    def __init__(self, id, customer_id, restaurant_id, status, order_time):
        self.id = id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.status = status
        self.order_time = order_time
        self.customer_name = None
        self.items = None
        self.total_price = None
```

---

## Backend: Service Classes

Service classes contain business logic. They use entity classes and database connections to perform operations.

### Example: `Manager_Service.py`

- Manages all manager operations (adding menu items, processing orders, analytics, etc.).
- Example method:

```python
def get_restaurant_menu_items_with_discounts(self, restaurant_id):
    # Returns a list of menu items for a restaurant with relevant discount information
```

### Example: `Customer_Service.py` (for your implementation)

- Manages all customer operations (browsing, ordering, rating, etc.).
- **Tip:** Use entity classes for all data objects.
- Example method:

```python
def get_all_restaurants(self):
    # Returns a list of Restaurant objects
```

---

## Frontend: HTML Templates

Templates are in the `templates/` folder. They use Jinja2 syntax (curly braces) to insert data from Python.

### Example: `manager/restaurant_page.html`

```html
<ul>
  {% for menu in menu_item_list %}
  <li>
    <img src="{{ menu.image }}" alt="{{ menu.name }}" />
    <strong>{{ menu.name }}</strong>
    {% if menu.has_discount %}
    <span style="text-decoration: line-through; color: #999"
      >{{ menu.original_price }} TL</span
    >
    <span style="color: #e74c3c; font-weight: bold">{{ menu.price }} TL</span>
    {% else %}
    <span>{{ menu.price }} TL</span>
    {% endif %}
    <br />
    {{ menu.description }}
  </li>
  {% endfor %}
</ul>
```

- **Tip:** You can copy and adapt these templates for the customer side.

---

## Running the Project

1. **Install Python 3** (if you haven't already)
2. **Install MySQL** and create the database with `Database/DDL.sql` and populate it with `Database/DML.sql`
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Start the application:**
   ```sh
   python app.py
   ```
5. **Open your browser:** Go to [http://localhost:5000](http://localhost:5000)

---

## How to Develop the Customer Side (Step by Step)

### 1. Understand the Entity Classes

- All the data you need (restaurants, menu items, carts, etc.) is represented as Python classes in `Entity/`.
- Example: Use the `Menu_Item` class to display a restaurant's menu.

### 2. Create a Customer Service Class

- Create a `Customer_Service` class in `Service/Customer_Service.py`.
- Fetch data using the database connection and return them as entity objects.
- Example methods:
  - `get_all_restaurants()` → returns a list of `Restaurant` objects
  - `get_restaurant_menu(restaurant_id)` → returns a list of `Menu_Item` objects
  - `add_to_cart(cart_id, menu_item_id, quantity)` → adds an item to the cart
  - `submit_order(cart_id)` → completes the order

### 3. Add Customer Routes to `app.py`

- Add Flask routes for customer pages:
  - `/customer/restaurants` → show all restaurants
  - `/customer/restaurant/<id>` → show menu and allow ordering
  - `/customer/cart` → show and update cart
  - `/customer/orders` → show order history
  - `/customer/add_rating/<restaurant_id>/<cart_id>` → rate a restaurant

### 4. Create Customer HTML Templates

- Copy the manager templates and adapt them for the customer side.
- Example: `templates/customer/restaurants.html`, `templates/customer/cart.html`, etc.
- Use Jinja2 to loop through data and display it in the browser.

### 5. Use Entity Classes in Your Service

- Always create and return entity objects (e.g., `Restaurant`, `Menu_Item`, `Cart`) when fetching data from the database.
- If you need to store a collection of items (e.g., for a cart), you can use Python's `set` type.

### 6. Test Your Features

- Use the browser to test all the customer features you add.
- Print debugging information in your Flask routes if needed.

---

## Example Customer Features

- **Browse Restaurants:** List all restaurants with filters like cuisine, city
- **View Menu:** Show menu items, prices, and discounts
- **Add to Cart:** Add menu items to a cart (order)
- **Checkout:** Submit the cart as an order
- **Order History:** Show all previous orders
- **Rate Restaurant:** After an order, allow the customer to rate and comment on the restaurant

---

## Tips for Beginners

- **Entity classes** are just Python classes to hold data. You can add more properties if needed.
- **Service classes** do the work: they talk to the database and return entity objects.
- **HTML templates** use curly braces (`{{ }}`) to display data from Python.
- **When you're stuck:**
  - Print debugging information in your Python code
  - Look at Flask and Jinja2 documentation
  - Look at the manager side for working examples

---

## Step by Step: How a Service Method, Route, and Template Work

In this section, we will explain step by step how a method in **Manager_Service** works, how this method is used in `app.py`, and how it is displayed in the HTML template. You can easily develop the customer side with the same logic.

### 1. Entity Layer (Model)

For example, for a menu item (Menu_Item):

```python
# Entity/Menu_Item.py
default
class Menu_Item():
    def __init__(self, id, name, image, description, price, restaurant_id):
        self.id = id
        self.name = name
        self.image = image
        self.description = description
        self.price = price
        self.restaurant_id = restaurant_id
        self.has_discount = False
        self.discount_rate = 0
        self.original_price = price
```

- **Purpose:** This is the Python equivalent of the Menu_Item table in the database. All menu item data is stored with this class.

### 2. Service Layer (Business Logic)

For example, the method that fetches menu items and discounts for a restaurant:

```python
# Service/Manager_Service.py
def get_restaurant_menu_items_with_discounts(self, restaurant_id):
    """Get all menu items for a restaurant with discount information if available"""
    query = """
    SELECT
        M.id, M.name, M.image, M.description, M.price, M.restaurant_id,
        D.id, D.discount_rate, D.start_date, D.end_date
    FROM
        Menu_Item M
    LEFT JOIN
        Has_Discount HD ON M.id = HD.menu_item_id
    LEFT JOIN
        Discount D ON HD.discount_id = D.id
            AND CURDATE() BETWEEN D.start_date AND D.end_date
    WHERE
        M.restaurant_id = {}
    """.format(restaurant_id)

    result = self.connection.execute_query(query)
    menu_items = []
    if result and len(result) > 0:
        for row in result:
            menu_item = Menu_Item(row[0], row[1], row[2], row[3], row[4], row[5])
            if row[6] is not None:
                menu_item.has_discount = True
                menu_item.discount_rate = row[7]
                menu_item.original_price = menu_item.price
                menu_item.price = round(menu_item.price * (1 - row[7]/100), 2)
            menu_items.append(menu_item)
    return menu_items
```

- **Purpose:**
  - Fetches menu items and discount information (if any) from the database using SQL.
  - Creates a `Menu_Item` object for each row.
  - If there is a discount, it fills the relevant fields.
  - Returns a list of `Menu_Item` objects.

### 3. Route (app.py)

A Flask route is defined to display this method on a web page:

```python
# app.py
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_page(restaurant_id):
    if manager_service.manager is None:
        return render_template("index.html", error="Manager not set!")
    result = manager_service.get_a_restaurant(restaurant_id)
    if result != -1 and result is not None:
        restaurant = result[0] if isinstance(result, list) and len(result) > 0 else result
        menu_items = manager_service.get_restaurant_menu_items_with_discounts(restaurant_id)
        return render_template('manager/restaurant_page.html',
                              restaurant=restaurant,
                              menu_item_list=menu_items)
    else:
        return "Restaurant not found", 404
```

- **Purpose:**
  - Gets the restaurant_id from the URL.
  - Fetches menu and restaurant information from the Service layer.
  - Passes the result to the HTML template.

### 4. Template (HTML)

Finally, this data is displayed in HTML:

```html
<!-- templates/manager/restaurant_page.html -->
<ul>
  {% for menu in menu_item_list %}
  <li>
    <img src="{{ menu.image }}" alt="{{ menu.name }}" />
    <strong>{{ menu.name }}</strong>
    {% if menu.has_discount %}
    <span style="text-decoration: line-through; color: #999"
      >{{ menu.original_price }} TL</span
    >
    <span style="color: #e74c3c; font-weight: bold">{{ menu.price }} TL</span>
    {% else %}
    <span>{{ menu.price }} TL</span>
    {% endif %}
    <br />
    {{ menu.description }}
  </li>
  {% endfor %}
</ul>
```

- **Purpose:**
  - Loops through and displays the menu list from Python.
  - If there is a discount, it shows both the original and discounted price.

---

## Step-by-Step Example: From Database to Webpage (Entity → Service → Route → Template)

This section provides a **detailed, beginner-friendly walkthrough** of how data flows from the database to the web page in this project. We use the example of listing menu items (with discounts) for a restaurant on the manager side. The same logic applies to the customer side!

### 1. Database Connection: The `Connector` Class

All database operations go through the `Connector` class (`Connector.py`). This class:

- Connects to the MySQL database.
- Runs SQL queries.
- Returns results to the Service classes.

**Example:**

```python
# Connector.py
class Connector():
    def execute_query(self, query):
        self.cursor.execute(query)
        if query.strip().lower().startswith("select"):
            return self.cursor.fetchall()
        else:
            self.connection.commit()
        return None
```

- **Usage:** The Service class creates a `Connector` object and uses it to fetch data.

### 2. Data Model: The `Entity` Classes

Entity classes (in the `Entity/` folder) represent tables in the database. For example, `Menu_Item` holds all the data for a menu item.

**Example:**

```python
# Entity/Menu_Item.py
class Menu_Item():
    def __init__(self, id, name, image, description, price, restaurant_id):
        self.id = id
        self.name = name
        self.image = image
        self.description = description
        self.price = price
        self.restaurant_id = restaurant_id
        self.has_discount = False
        self.discount_rate = 0
        self.original_price = price
```

- **Tip:** Always use Entity classes to pass data between Service, Route, and Template.

### 3. Business Logic: The Service Method

Service classes (like `Manager_Service.py`) contain methods that:

- Use the `Connector` to run SQL queries.
- Create Entity objects from the results.
- Return lists of Entity objects.

**Example:**

```python
# Service/Manager_Service.py
def get_restaurant_menu_items_with_discounts(self, restaurant_id):
    query = """
    SELECT
        M.id, M.name, M.image, M.description, M.price, M.restaurant_id,
        D.id, D.discount_rate, D.start_date, D.end_date
    FROM
        Menu_Item M
    LEFT JOIN
        Has_Discount HD ON M.id = HD.menu_item_id
    LEFT JOIN
        Discount D ON HD.discount_id = D.id
            AND CURDATE() BETWEEN D.start_date AND D.end_date
    WHERE
        M.restaurant_id = {}
    """.format(restaurant_id)
    result = self.connection.execute_query(query)
    menu_items = []
    for row in result:
        menu_item = Menu_Item(row[0], row[1], row[2], row[3], row[4], row[5])
        if row[6] is not None:
            menu_item.has_discount = True
            menu_item.discount_rate = row[7]
            menu_item.original_price = menu_item.price
            menu_item.price = round(menu_item.price * (1 - row[7]/100), 2)
        menu_items.append(menu_item)
    return menu_items
```

- **Key Points:**
  - The method uses the `Connector` to get data from the database.
  - It creates a `Menu_Item` object for each row.
  - If there is a discount, it updates the object.
  - Returns a list of `Menu_Item` objects.

### 4. Flask Route: Connecting Service to Web

The Flask route (in `app.py`) calls the Service method and passes the data to the template.

**Example:**

```python
# app.py
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_page(restaurant_id):
    if manager_service.manager is None:
        return render_template("index.html", error="Manager not set!")
    restaurant = manager_service.get_a_restaurant(restaurant_id)
    menu_items = manager_service.get_restaurant_menu_items_with_discounts(restaurant_id)
    return render_template('manager/restaurant_page.html',
                          restaurant=restaurant,
                          menu_item_list=menu_items)
```

- **Key Points:**
  - The route gets the `restaurant_id` from the URL.
  - Calls the Service method to get menu items (as Entity objects).
  - Passes the list to the template as `menu_item_list`.

### 5. HTML Template: Displaying Data

The template (in `templates/manager/restaurant_page.html`) uses Jinja2 to loop over the data and display it.

**Example:**

```html
<ul>
  {% for menu in menu_item_list %}
  <li>
    <img src="{{ menu.image }}" alt="{{ menu.name }}" />
    <strong>{{ menu.name }}</strong>
    {% if menu.has_discount %}
    <span style="text-decoration: line-through; color: #999"
      >{{ menu.original_price }} TL</span
    >
    <span style="color: #e74c3c; font-weight: bold">{{ menu.price }} TL</span>
    {% else %}
    <span>{{ menu.price }} TL</span>
    {% endif %}
    <br />
    {{ menu.description }}
  </li>
  {% endfor %}
</ul>
```

- **Key Points:**
  - Loops over `menu_item_list` (a list of `Menu_Item` objects).
  - Shows the name, image, price, and discount info.

---

### Summary Table: How Everything Connects

| Layer     | File/Folder                            | Example Symbol/Class                     | Role/Responsibility                    |
| --------- | -------------------------------------- | ---------------------------------------- | -------------------------------------- |
| Database  | MySQL                                  | Menu_Item table                          | Stores the data                        |
| Connector | Connector.py                           | Connector                                | Runs SQL, returns results              |
| Entity    | Entity/Menu_Item.py                    | Menu_Item                                | Holds data as Python objects           |
| Service   | Service/Manager_Service.py             | get_restaurant_menu_items_with_discounts | Fetches data, returns Entity objects   |
| Route     | app.py                                 | restaurant_page                          | Calls Service, passes data to template |
| Template  | templates/manager/restaurant_page.html | menu_item_list                           | Displays data using Jinja2             |

---

### How to Apply This to the Customer Side

- Create similar Service methods in `Customer_Service.py` (use Entity classes!).
- Add routes in `app.py` for customer pages.
- Pass Entity objects to your templates.
- Use Jinja2 to display the data.

**If you follow this pattern, you can build any feature!**

---

## Notes and Tips

- Service methods should always return Entities, so they can be easily used in templates and other methods.
- Run SQL queries with the Connector class and transfer the results to Entities.
- Call the Service method in the Route and send the result to the template.
- Display data with loops in the template using Jinja2.
- You can easily write the customer side by examining examples from the manager side.
