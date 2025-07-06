import sys
from flask import Flask, jsonify, request, redirect, render_template_string, session
import sqlite3
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from dotenv import load_dotenv
from pydantic import BaseModel

app = Flask(__name__)
load_dotenv()
# for sqli thing
app.secret_key = os.getenv("JWT_SECRET_KEY")
# for crack pin thing
secret_pin = os.getenv("SECRET_PIN")
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

# Secure session cookie settings
app.config['SESSION_COOKIE_HTTPONLY'] = True  # JS can't access the cookie
app.config['SESSION_COOKIE_SECURE'] = True   # Set to True in HTTPS-only (prod) environment
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Helps prevent CSRF

# Rate limit: 10 requests/min per IP
# limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# for sqli thing
def init_db():
    db_path = "ctf.db"
    if os.path.exists(db_path):
        os.remove(db_path)  # clean slate
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'ctf-USER')")
    conn.commit()
    conn.close()
    print("Database initialized.")

# for sqli thing
@app.route('/', methods=['GET', 'POST'])
# @limiter.limit("10 per minute")
def vulnerable_login():
    # if request.method == 'GET':
    #     return render_template_string(login_form_html)

    username = request.form.get('username', '')
    password = request.form.get('password', '')

    conn = sqlite3.connect("ctf.db")
    c = conn.cursor()

    # Intentionally vulnerable query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Executing:", query)

    try:
        c.execute(query)
        result = c.fetchone()
    except Exception as e:
        conn.close()
        return f"<b>SQL Error:</b> {str(e)}"

    conn.close()
    if result:
        session['authenticated'] = True
        print("User authenticated! Session set.")
        return redirect("/flag")

    return "Login failed"

# for sqli thing
@app.route('/flag')
def flag():
    print("Session:", session)
    if not session.get('authenticated'):
        return redirect("/")
    return '''
    <h1>🎉 Congratulations!</h1>
    <p>Here is your flag:</p>
    <code>CTF{sql_injection_login_bypassed}</code>
    '''

# for crack pin thing
class PINInput(BaseModel):
    pin : str
    
@app.route("/check-pin", methods=["OPTIONS"])
def check_pin_options():
    return '', 204

# for crack pin thing
@app.route("/check-pin", methods=["POST"])
def check_pin():
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json", "status": "error"}), 400

    try:
        data = request.get_json()
        pin = data.get("pin")
    except Exception:
        return jsonify({"message": "Invalid JSON", "status": "error"}), 400

    if not pin:
        return jsonify({"message": "No pin provided", "status": "error"}), 400

    if pin == secret_pin:
        return jsonify({"message": "Correct pin", "status": "success", "flag": "CTF{pin_bruteforced_successfully}"}), 200
    else:
        return jsonify({"message": "Incorrect pin", "status": "failure"}), 401


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "init-db":
        init_db()
    else:
        app.run(host="0.0.0.0", port=5000)
