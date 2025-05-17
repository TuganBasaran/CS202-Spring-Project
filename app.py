from flask import Flask, render_template, url_for, request, redirect, session
from Service.Manager_Service import Manager_Service
from Connector import Connector
from Entity.Restaurant import Restaurant

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Session için gerekli anahtar

user = 'root'
password = 'password'
database = 'CS202'
connector = Connector(user, password, database)
manager_service = Manager_Service(connector)

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
            # Assuming you want to fetch all restaurants for the manager
            restaurants = manager_service.get_all_restaurants_by_manager()
            return render_template("manager/manager_dashboard.html", restaurants=restaurants, username= manager_service.manager.user_name)
        else:
            return render_template("index.html", error="Invalid credentials")
    else:
        # Customer veya diğer roller için de bir response dön
        return render_template("index.html", error="Sadece manager girişi destekleniyor.")

@app.route('/restaurant/<int:restaurant_id>')
def restaurant_page(restaurant_id):
    if manager_service.manager is None: 
        return render_template("index.html", error= "Manager not set!")

    result = manager_service.get_a_restaurant(restaurant_id)
    
    if result != -1 and result is not None:
        # Eğer result bir liste ise ilk elemanı al, değilse direkt gönder
        if isinstance(result, list) and len(result) > 0:
            restaurant = result[0]
        else:
            restaurant = result
        # Menü itemlarını al
        menu_items = manager_service.get_restaurant_menu_items(restaurant_id)
        ratings, average_rating= manager_service.get_restaurant_ratings(restaurant_id)
        label = None
        if len(ratings) < 10: 
            average_rating = 0
            label= 'New'
        keywords = manager_service.get_restaurant_keywords(restaurant_id)
        return render_template('manager/restaurant_page.html', restaurant=restaurant, menu_item_list=menu_items, ratings=ratings, keywords= keywords, average_rating= average_rating, label= label)
    else:
        return "Restoran bulunamadı", 404

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

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
    return redirect(url_for('restaurant_page', restaurant_id=restaurant_id))

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
    return redirect(url_for('restaurant_page', restaurant_id=restaurant_id))

if __name__ == '__main__':
    app.run(debug=True)