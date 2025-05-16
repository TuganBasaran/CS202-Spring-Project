from flask import Flask, render_template, url_for, request
from Service.Manager_Service import Manager_Service
from Connector import Connector

app = Flask(__name__)

user = 'root'
password = 'password'
database = 'CS202'
connector = Connector(user, password, database)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    
    if role == 'manager': 
        manager_service = Manager_Service(connector)
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


if __name__ == '__main__':
    app.run(debug=True)