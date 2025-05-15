from flask import Flask, render_template, url_for
import mysql.connector
app = Flask(__name__)

init_cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="test123"
)
init_cursor = init_cnx.cursor()
init_cursor.execute("CREATE DATABASE IF NOT EXISTS cs202")
init_cursor.close()
init_cnx.close()

# ✅ Connect to the database
cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="test123",
    database="cs202"  # ✅ Make sure the DB is selected here
)
cursor = cnx.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS cs202")
@app.route('/')
def index():
    cursor.execute("SELECT restaurant_name FROM Restaurant Where cuisine_type='Indian' ")
    restaurant_names = [row[0] for row in cursor.fetchall()]
    return render_template("index.html", restaurants=restaurant_names)

if __name__ == '__main__':
    app.run(debug=True)