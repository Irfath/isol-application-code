from flask import Flask
import os
import mysql.connector

app = Flask(__name__)

# Database connectionS
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@app.route('/')
def hello():
    version = "1.0.0"
    hostname = os.getenv('HOSTNAME', 'unknown')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  
        cursor.execute("SELECT username, userid FROM user LIMIT 1")
        user_data = cursor.fetchone() 
        cursor.close()
        conn.close()

        if user_data:
            username = user_data['username']
            userid = user_data['userid']
            user_info = f"Username: {username}<br>User ID: {userid}"
        else:
            user_info = "No user data found."

    except mysql.connector.Error as err:
        user_info = f"Error: {err}"

    return f"Hello, world Irfath ISOL!<br>Version: {version}<br>Hostname: {hostname}<br>{user_info}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
