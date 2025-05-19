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
- [How to Run the Project](#how-to-run-the-project)
- [How to Implement the Customer Side (Step by Step)](#how-to-implement-the-customer-side-step-by-step)
- [Example Customer Features](#example-customer-features)
- [Tips for Beginners](#tips-for-beginners)

---

## Introduction

This project is a full-stack restaurant management and food ordering system. It is designed for both restaurant managers and customers. The manager side is fully implemented; this guide will help you understand the codebase and teach you how to implement the customer side, even if you are new to Python and Flask.

---

## Project Overview

- **Managers** can:
  - Add/manage restaurants, menu items, and discounts
  - View and process orders
  - See analytics (sales, top customers, etc.)
- **Customers** (to be implemented) will be able to:
  - Browse restaurants and menus
  - Place orders and view order history
  - Rate restaurants

---

## Technology Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML, CSS, Jinja2 (Flask's template engine)
- **Database:** MySQL

---

## Project Structure

```
CS202-Spring-Project/
├── app.py                  # Main Flask app (routes, startup)
├── Connector.py            # Database connection helper
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
├── Database/DML.sql        # Example data
└── requirements.txt        # Python dependencies
```

---

## Database Design

- **User**: All users (managers and customers)
- **Restaurant_Manager**: Managers (inherits from User)
- **Customer**: Customers (inherits from User)
- **Restaurant**: Restaurant info
- **Menu_Item**: Menu items for each restaurant
- **Cart**: Orders (one per customer per order)
- **Contains**: Items in each cart
- **Discount**: Discount campaigns
- **Has_Discount**: Which menu items have which discounts
- **Rating**: Customer feedback
- **Keyword**: Tags for restaurants
- **Restaurant_Keyword**: Which restaurant has which tags
- **Address**: Address info

---

## Backend: Entity Classes

These are Python classes that represent database tables. They are found in the `Entity/` folder.

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

- **Tip:** All entity classes are simple containers for data. You can add more attributes if you need them for the customer side.

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

Service classes contain the business logic. They use the entity classes and database connection to perform operations.

### Example: `Manager_Service.py`

- Handles all manager operations (add menu item, process orders, analytics, etc.)
- Example method:

```python
def get_restaurant_menu_items_with_discounts(self, restaurant_id):
    # Returns a list of Menu_Item objects, with discount info if available
```

### Example: `Customer_Service.py` (for you to implement)

- Handles all customer operations (browse, order, rate, etc.)
- **Tip:** Use the entity classes for all data objects.
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

## How to Run the Project

1. **Install Python 3** (if not already installed)
2. **Install MySQL** and create the database using `Database/DDL.sql` and fill with `Database/DML.sql`
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Start the app:**
   ```sh
   python app.py
   ```
5. **Open your browser:** Go to [http://localhost:5000](http://localhost:5000)

---

## How to Implement the Customer Side (Step by Step)

### 1. Understand the Entity Classes

- All data you need (restaurants, menu items, carts, etc.) are represented as Python classes in `Entity/`.
- Example: To show a restaurant's menu, use the `Menu_Item` class.

### 2. Create a Customer Service Class

- In `Service/Customer_Service.py`, create a `Customer_Service` class.
- Use the database connection to fetch data and return entity objects.
- Example methods:
  - `get_all_restaurants()` → returns list of `Restaurant` objects
  - `get_restaurant_menu(restaurant_id)` → returns list of `Menu_Item` objects
  - `add_to_cart(cart_id, menu_item_id, quantity)` → adds item to cart
  - `submit_order(cart_id)` → finalizes the order

### 3. Add Customer Routes to `app.py`

- Add Flask routes for customer pages:
  - `/customer/restaurants` → show all restaurants
  - `/customer/restaurant/<id>` → show menu and allow ordering
  - `/customer/cart` → show and update cart
  - `/customer/orders` → show order history
  - `/customer/add_rating/<restaurant_id>/<cart_id>` → rate a restaurant

### 4. Create Customer HTML Templates

- Copy and adapt manager templates for the customer side.
- Example: `templates/customer/restaurants.html`, `templates/customer/cart.html`, etc.
- Use Jinja2 to loop over data and show it in the browser.

### 5. Use Entity Classes in Your Service

- When fetching data from the database, always create and return entity objects (e.g., `Restaurant`, `Menu_Item`, `Cart`).
- If you need to store a set of items (e.g., for a cart), you can use Python's `set` type.

### 6. Test Your Features

- Use the browser to test all customer features you add.
- Print debug info in your Flask routes if needed.

---

## Example Customer Features

- **Browse Restaurants:** List all restaurants with filters (cuisine, city)
- **View Menu:** Show menu items, prices, and discounts
- **Add to Cart:** Add menu items to a cart (order)
- **Checkout:** Submit the cart as an order
- **Order History:** Show all previous orders
- **Rate Restaurant:** After an order, allow the customer to rate and comment

---

## Tips for Beginners

- **Entity classes** are just Python classes for holding data. You can add more attributes if you need them.
- **Service classes** do the work: they talk to the database and return entity objects.
- **HTML templates** use curly braces (`{{ }}`) to show data from Python.
- **If you get stuck:**
  - Print debug info in your Python code
  - Check the Flask and Jinja2 documentation
  - Look at the manager side for working examples

---

## Adım Adım: Bir Service Methodu, Route ve Template Nasıl Çalışır?

Bu bölümde, bir örnek üzerinden **Manager_Service** içindeki bir methodun nasıl çalıştığını, bu methodun `app.py`'da nasıl kullanıldığını ve HTML template'te nasıl gösterildiğini adım adım açıklayacağız. Aynı mantıkla customer tarafını da kolayca geliştirebilirsiniz.

### 1. Entity Katmanı (Model)

Örneğin bir menü öğesi (Menu_Item) için:

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

- **Amaç:** Veritabanındaki Menu_Item tablosunun Python karşılığıdır. Tüm menü öğesi verileri bu class ile tutulur.

### 2. Service Katmanı (İş Mantığı)

Örneğin, bir restoranın menü öğelerini ve indirimlerini getiren method:

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

- **Amaç:**
  - SQL ile veritabanından menü öğelerini ve varsa indirim bilgilerini çeker.
  - Her satır için bir `Menu_Item` nesnesi oluşturur.
  - İndirim varsa, ilgili alanları doldurur.
  - Sonuç olarak bir `Menu_Item` listesi döner.

### 3. Route (app.py)

Bu methodu bir web sayfasında göstermek için bir Flask route'u tanımlanır:

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
        return "Restoran bulunamadı", 404
```

- **Amaç:**
  - URL'den restaurant_id alır.
  - Service katmanından menü ve restoran bilgilerini çeker.
  - Sonucu HTML template'e yollar.

### 4. Template (HTML)

Son olarak, bu veriler HTML'de gösterilir:

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

- **Amaç:**
  - Python'dan gelen menü listesini döngüyle ekrana basar.
  - Eğer indirim varsa hem orijinal hem indirimli fiyatı gösterir.

---

## Kendi Customer Service ve Sayfalarını Yazarken

1. **Entity**: Her veri için bir class kullan (ör: Restaurant, Menu_Item, Cart).
2. **Service**: Veritabanı işlemlerini yapan methodlar yaz. Her method bir veya birden fazla entity döndürsün.
3. **Route**: Flask'ta bir route tanımla, service methodunu çağır, sonucu template'e gönder.
4. **Template**: HTML dosyanda Python'dan gelen verileri Jinja2 ile göster.

### Örnek: Customer Menü Görüntüleme

- **Entity:** Menu_Item
- **Service:** get_restaurant_menu(restaurant_id)
- **Route:** /customer/restaurant/<id>
- **Template:** customer/restaurant_detail.html

Her adımda, entity class'larını kullanarak veriyi taşımak ve template'te göstermek en iyi pratiktir.

---

## Sıkça Sorulan Sorular

- **Bir service methodu neden entity döndürmeli?**
  - Çünkü template'te ve diğer methodlarda kolayca kullanılabilir, kod okunur ve bakımı kolay olur.
- **Birden fazla tabloyu birleştirirken ne yapmalıyım?**
  - SQL JOIN kullan, sonucu entity'ye aktar.
- **Template'te neden set veya liste kullanmalıyım?**
  - Çünkü birden fazla veri göstermek için döngüye ihtiyacın olur.

---

Bu örnekleri ve açıklamaları takip ederek, projenin customer tarafını da kolayca geliştirebilirsin. Her adımda mevcut manager kodlarını referans alabilirsin.
