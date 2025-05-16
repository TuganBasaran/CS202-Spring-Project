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
    result = manager_service.get_a_restaurant(restaurant_id)

    if result != -1 and result is not None:
        # Eğer result bir liste ise ilk elemanı al, değilse direkt gönder
        if isinstance(result, list) and len(result) > 0:
            restaurant = result[0]
        else:
            restaurant = result
        # Menü itemlarını al
        menu_items = manager_service.get_restaurant_menu_items(restaurant_id)
        return render_template('manager/restaurant_page.html', restaurant=restaurant, menu_item_list=menu_items)
    else:
        return "Restoran bulunamadı", 404

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)