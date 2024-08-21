from flask import Flask, render_template, jsonify
import os
import mysql.connector

app = Flask(__name__)

# Database connection
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@app.route('/')
def index():
    version = "2.0.4"
    hostname = os.getenv('HOSTNAME', 'unknown')
    return render_template('index.html', version=version, hostname=hostname)

@app.route('/get_user_data')
def get_user_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, userid FROM user LIMIT 1")
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            return jsonify(user_data)
        else:
            return jsonify({"error": "No user data found."})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
