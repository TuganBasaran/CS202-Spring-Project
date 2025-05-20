from flask import Flask, render_template, url_for, request, redirect, session, flash
from datetime import datetime, timedelta
from Entity.User.Customer import Customer
from Service.Customer_Service import Customer_Service
from Service.Manager_Service import Manager_Service
from Connector import Connector
from Entity.Restaurant import Restaurant

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Session için gerekli anahtar

user = 'root'
connector = Connector(user, password, database)
manager_service = Manager_Service(connector)
customer_service = Customer_Service(connector)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    
    if role == 'manager': 
        login_success = manager_service.login(user_name=username, password=password)
        
        if login_success:
            # Fetch all restaurants for the manager
            restaurants = manager_service.get_all_restaurants_by_manager()
            
            # Get total statistics across all restaurants
            total_revenue = manager_service.get_manager_total_revenue()
            total_orders = manager_service.get_manager_total_orders()
            
            # Get per-restaurant statistics
            for restaurant in restaurants:
                restaurant.revenue = manager_service.get_restaurant_revenue(restaurant.restaurant_id)
                restaurant.order_count = manager_service.get_restaurant_order_count(restaurant.restaurant_id)
            
            return render_template("manager/manager_dashboard.html",
                                  restaurants=restaurants,
                                  username=manager_service.manager.user_name,
                                  total_revenue=total_revenue,
                                  total_orders=total_orders)
        else:
            return render_template("index.html", error="Invalid credentials")
            # Assume 'customer_service' is already created from Customer_Service(connection)

    else:
        login_success = customer_service.login(username=username, password=password)

        if login_success:
            session['user_id'] = customer_service.user.user_id
            local_restaurants = customer_service.get_restaurants_sorted_by_rating()
            addresses = customer_service.view_address(customer_service.user.user_id)
            phones = customer_service.view_phone_number(customer_service.user.user_id)

            return render_template("Customer/customer_menu.html",
                                   restaurants=local_restaurants,
                                   username=customer_service.user.user_name,
                                   addresses=addresses,
                                   phones=phones)

        else:
            return render_template("index.html", error="Invalid credentials")


@app.route('/manager/restaurant/<int:restaurant_id>')
def manager_restaurant_page(restaurant_id):
    if manager_service.manager is None: 
        return render_template("index.html", error= "Manager not set!")

    result = manager_service.get_a_restaurant(restaurant_id)
    
    if result != -1 and result is not None:
        # Eğer result bir liste ise ilk elemanı al, değilse direkt gönder
        if isinstance(result, list) and len(result) > 0:
            restaurant = result[0]
        else:
            restaurant = result
            
        # Use the method with discount information instead
        menu_items = manager_service.get_restaurant_menu_items_with_discounts(restaurant_id)
        
        ratings, average_rating = manager_service.get_restaurant_ratings(restaurant_id)
        label = None
        if len(ratings) < 10: 
            average_rating = 0
            label = 'New'
        keywords = manager_service.get_restaurant_keywords(restaurant_id)
        return render_template('manager/restaurant_page.html',
                              restaurant=restaurant, 
                              menu_item_list=menu_items, 
                              ratings=ratings, 
                              keywords=keywords, 
                              average_rating=average_rating, 
                              label=label)
    else:
        return "Restoran bulunamadı", 404

@app.route('/customer/restaurant/<int:restaurant_id>')
def customer_restaurant_page(restaurant_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    restaurant = customer_service.get_restaurant(restaurant_id)
    if not restaurant:
        return "Restaurant not found", 404

    menu_items = customer_service.get_restaurant_menu_items(restaurant_id)
    ratings, avg_rating = customer_service.get_restaurant_ratings(restaurant_id)

    return render_template("Customer/restaurant_view.html",
                           restaurant=restaurant,
                           menu_items=menu_items,
                           ratings=ratings,
                           average_rating=avg_rating)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

from flask import Flask, render_template, url_for, request, redirect, session

@app.route('/customer/add_address', methods=['GET'])
def add_address_form():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('Customer/add_address.html')

@app.route('/customer/add_address', methods=['POST'])
def add_address():
    address_name = request.form.get('address_name')
    address = request.form.get('address')
    city = request.form.get('city')

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    if not address or not city:
        return "Address and city are required.", 400

    success = customer_service.add_address(user_id, address_name, address, city)
    if success:
        return redirect(url_for('customer_menu'))
    return "Failed to add address."

@app.route('/customer/add_phone', methods=['GET'])
def add_phone_form():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('Customer/add_phone.html')

@app.route('/customer/add_phone', methods=['POST'])
def add_phone():
    phone_number = request.form.get('phone_number')
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    if not phone_number:
        return "Phone number is required.", 400

    success = customer_service.add_phone_number(user_id, phone_number)
    if success:
        return redirect(url_for('customer_menu'))
    return "Failed to add phone number."


@app.route('/restaurant/<int:restaurant_id>/keywords', methods=['GET'])
def restaurant_keywords(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
        
    restaurant = manager_service.get_a_restaurant(restaurant_id)
    keywords = manager_service.get_restaurant_keywords(restaurant_id)
    all_manager_keywords = manager_service.get_manager_keywords()
    
    return render_template('manager/restaurant_keywords.html', 
                          restaurant=restaurant, 
                          keywords=keywords, 
                          all_keywords=all_manager_keywords)

@app.route('/restaurant/<int:restaurant_id>/add_keyword', methods=['POST'])
def add_keyword(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
    
    action = request.form.get('action')
    
    if action == 'existing':
        keyword_id = request.form.get('keyword_id')
        if keyword_id:
            manager_service.add_keyword_to_restaurant(restaurant_id, keyword_id=int(keyword_id))
    else:  # new keyword
        keyword_text = request.form.get('keyword_text')
        if keyword_text:
            # Add quotes around the keyword text for SQL
            quoted_keyword = f"'{keyword_text}'"
            manager_service.add_keyword_to_restaurant(restaurant_id, keyword_text=quoted_keyword)
    
    return redirect(url_for('restaurant_keywords', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/remove_keyword/<int:keyword_id>', methods=['POST'])
def remove_keyword(restaurant_id, keyword_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
    
    # Pass as tuple for parameterized query
    manager_service.remove_keyword_from_restaurant(restaurant_id, keyword_id)
    return redirect(url_for('restaurant_keywords', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/add_menu_item', methods=['GET'])
def add_menu_item_form(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
        
    restaurant = manager_service.get_a_restaurant(restaurant_id)
    return render_template('manager/add_menu_item.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/add_menu_item', methods=['POST'])
def add_menu_item(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    image = request.form.get('image')
    description = request.form.get('description')
    price = request.form.get('price')
    
    # Validate inputs
    if not name or not price:
        return "Name and price are required", 400
    
    # Set default values if needed
    if not image:
        image = 'default_food.jpg'
    
    # Create menu item
    menu_item_id = manager_service.create_menu_item(
        name=name,
        image=image,
        description=description,
        price=price,
        restaurant_id=restaurant_id
    )
    
    # Redirect back to restaurant page
    return redirect(url_for('manager_restaurant_page', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/delete_menu_item/<int:menu_item_id>', methods=['POST'])
def delete_menu_item(restaurant_id, menu_item_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
    
    # Delete the menu item
    success = manager_service.delete_menu_item(menu_item_id, restaurant_id)
    
    if success:
        # You could add a flash message here if you want to show a success message
        pass
    
    # Redirect back to the restaurant page
    return redirect(url_for('manager_restaurant_page', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/discounts', methods=['GET'])
def restaurant_discounts(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
        
    restaurant = manager_service.get_a_restaurant(restaurant_id)
    menu_items = manager_service.get_restaurant_menu_items_with_discounts(restaurant_id)
    discounts = manager_service.get_restaurant_discounts(restaurant_id)
    
    return render_template('manager/discounts.html', 
                          restaurant=restaurant,
                          menu_items=menu_items,
                          discounts=discounts)

@app.route('/restaurant/<int:restaurant_id>/add_discount', methods=['GET'])
def add_discount_form(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
        
    restaurant = manager_service.get_a_restaurant(restaurant_id)
    menu_items = manager_service.get_restaurant_menu_items_with_discounts(restaurant_id)
    
    return render_template('manager/add_discount.html', 
                          restaurant=restaurant,
                          menu_items=menu_items)

@app.route('/restaurant/<int:restaurant_id>/add_discount', methods=['POST'])
def add_discount(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
    
    discount_rate = request.form.get('discount_rate')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    menu_item_ids = request.form.getlist('menu_item_ids')
    
    # Validate inputs
    if not discount_rate or not start_date or not end_date or not menu_item_ids:
        return "All fields are required", 400
    
    # Create the discount
    discount_id = manager_service.create_discount(
        discount_rate=discount_rate,
        start_date=start_date,
        end_date=end_date
    )
    
    # Apply the discount to selected menu items
    for menu_item_id in menu_item_ids:
        manager_service.apply_discount_to_menu_item(int(menu_item_id), discount_id)
    
    # Redirect back to the discounts page
    return redirect(url_for('restaurant_discounts', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/remove_discount/<int:menu_item_id>/<int:discount_id>', methods=['POST'])
def remove_discount(restaurant_id, menu_item_id, discount_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
    
    manager_service.remove_discount_from_menu_item(menu_item_id, discount_id)
    
    # Redirect back to the discounts page
    return redirect(url_for('restaurant_discounts', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/orders')
def restaurant_orders(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
        
    restaurant = manager_service.get_a_restaurant(restaurant_id)
    
    # Default to showing all orders
    order_filter = request.args.get('filter', 'all')
    
    if order_filter == 'pending':
        orders = manager_service.get_restaurant_pending_orders(restaurant_id)
        title = "Pending Orders"
    else:
        orders = manager_service.get_restaurant_all_orders(restaurant_id)
        title = "All Orders"
    
    return render_template('manager/orders.html',
                          restaurant=restaurant,
                          orders=orders,
                          filter=order_filter,
                          title=title)

@app.route('/restaurant/<int:restaurant_id>/accept_order/<int:order_id>', methods=['POST'])
def accept_order(restaurant_id, order_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
    
    success = manager_service.update_order_status(order_id, 'accepted', restaurant_id)
    
    if success:
        # You could add a flash message here if you want
        pass
    
    return redirect(url_for('restaurant_orders', restaurant_id=restaurant_id, filter='pending'))

@app.route('/restaurant/<int:restaurant_id>/deliver_order/<int:order_id>', methods=['POST'])
def deliver_order(restaurant_id, order_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
    
    success = manager_service.update_order_status(order_id, 'delivered', restaurant_id)
    
    if success:
        # You could add a flash message here if you want
        pass
    
    return redirect(url_for('restaurant_orders', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu_stats')
def menu_item_stats(restaurant_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))
        
    restaurant = manager_service.get_a_restaurant(restaurant_id)
    
    # Default to 30 days, but allow query parameter to change
    days = request.args.get('days', 30, type=int)
    
    menu_stats_raw = manager_service.get_menu_item_sales_stats(restaurant_id, days)
    # menu_stats_raw is a list of (Menu_Item, total_quantity, total_revenue)
    menu_stats = []
    total_quantity = 0
    total_revenue = 0
    for menu_item, quantity, revenue in menu_stats_raw:
        menu_stats.append({
            'id': menu_item.id,
            'name': menu_item.name,
            'image': menu_item.image,
            'description': menu_item.description,
            'price': menu_item.price,
            'total_quantity': quantity,
            'total_revenue': revenue
        })
        total_quantity += quantity
        total_revenue += revenue

    # Get the customer with most orders
    top_customer_tuple = manager_service.get_customer_most_orders(restaurant_id, days)
    if top_customer_tuple:
        top_customer, order_count = top_customer_tuple
        top_customer_dict = {
            'user_id': top_customer.user_id,
            'user_name': top_customer.user_name,
            'order_count': order_count
        }
    else:
        top_customer_dict = None

    # Get the customer with highest-value cart
    top_cart_tuple = manager_service.get_customer_highest_value_cart(restaurant_id, days)
    if top_cart_tuple:
        cart, customer = top_cart_tuple
        top_cart_customer_dict = {
            'user_id': customer.user_id,
            'user_name': customer.user_name,
            'total_value': round(getattr(cart, 'total_value', None), 2),
            'order_time': getattr(cart, 'order_time', None),
            'cart_items': getattr(cart, 'cart_items', None)
        }
    else:
        top_cart_customer_dict = None

    return render_template('manager/menu_stats.html',
                          restaurant=restaurant,
                          menu_stats=menu_stats,
                          days=days,
                          total_quantity=total_quantity,
                          total_revenue=total_revenue,
                          top_customer=top_customer_dict,
                          top_cart_customer=top_cart_customer_dict)

@app.route('/customer/menu', methods=['GET'])
def customer_menu():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    if not customer_service.user or customer_service.user.user_id != user_id:
        # You were only setting a placeholder user here
        user_result = customer_service.select_by_id(user_id)
        username = user_result[0][1] if user_result else "Unknown"
        customer_service.user = Customer(user_id, username, "placeholder")

    restaurants = customer_service.get_restaurants_sorted_by_rating()
    addresses = customer_service.view_address(user_id)
    phone_numbers = customer_service.view_phone_number(user_id)

    return render_template(
        "Customer/customer_menu.html",
        restaurants=restaurants,
        username=customer_service.user.user_name,
        addresses=addresses,
        phones=phone_numbers
    )

@app.route('/customer/orders')
def customer_orders():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    orders = customer_service.get_customer_orders(user_id)
    return render_template('Customer/customer_orders.html', orders=orders, now=datetime.now())

@app.route('/customer/review/<int:cart_id>', methods=['GET'])
def review_order_form(cart_id):
    return render_template('Customer/review_form.html', cart_id=cart_id)


@app.route('/customer/review/<int:cart_id>', methods=['POST'])
def submit_review(cart_id):
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')
    user_id = session.get('user_id')

    cart_info = customer_service.get_cart_details_by_id(cart_id)
    if not cart_info:
        return "Invalid cart", 400

    restaurant_id = cart_info['restaurant_id']

    success = customer_service.create_rating(cart_id, rating, comment, user_id, restaurant_id)
    if success:
        return redirect(url_for('customer_orders'))
    return "Review failed", 500



@app.route('/restaurant/<int:restaurant_id>/edit_menu_item/<int:menu_item_id>', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_item_id):
    if manager_service.manager is None:
        return redirect(url_for('index'))

    if request.method == 'GET':
        menu_item = manager_service.get_menu_item(menu_item_id)
        restaurant = manager_service.get_a_restaurant(restaurant_id)
        return render_template('manager/edit_menu_item.html',
                               menu_item=menu_item,
                               restaurant=restaurant)

    # POST: update item
    name = request.form.get('name')
    image = request.form.get('image')
    description = request.form.get('description')
    price = request.form.get('price')

    success = manager_service.update_menu_item(menu_item_id, name, image, description, price)
    if success:
        return redirect(url_for('manager_restaurant_page', restaurant_id=restaurant_id))
    else:
        return "Failed to update item", 500

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    menu_item_id = request.form.get('menu_item_id')
    restaurant_id = request.form.get('restaurant_id')

    success = customer_service.add_to_cart(user_id, menu_item_id, restaurant_id)
    if success:
        flash('Item added to cart successfully!')
        return redirect(url_for('customer_restaurant_page', restaurant_id=restaurant_id))
    else:
        flash('Failed to add item to cart.')
        return redirect(url_for('customer_restaurant_page', restaurant_id=restaurant_id))

@app.route('/cart/view')
def view_cart():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    cart, items = customer_service.get_open_cart_details(user_id)
    if not cart:
        return render_template("Customer/view_cart.html", empty=True)

    return render_template("Customer/view_cart.html", cart=cart, items=items)

@app.route('/cart/send', methods=['POST'])
def send_cart():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    cart_id = request.form.get('cart_id')
    if not cart_id:
        return "Missing cart ID", 400

    success = customer_service.submit_cart(cart_id)
    if success:
        return redirect(url_for('customer_menu'))  # or show confirmation
    else:
        return "Failed to submit cart", 500




if __name__ == '__main__':
    app.run(debug=True)