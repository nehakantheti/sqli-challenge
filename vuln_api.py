from flask import Flask, request, redirect, render_template_string, session
import sqlite3
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("JWT_SECRET_KEY")  # Replace in prod
CORS(app, origins=["*"])

# Secure session cookie settings
app.config['SESSION_COOKIE_HTTPONLY'] = True  # JS can't access the cookie
app.config['SESSION_COOKIE_SECURE'] = True   # Set to True in HTTPS-only (prod) environment
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Helps prevent CSRF

# Rate limit: 10 requests/min per IP
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

def init_db():
    conn = sqlite3.connect("ctf.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'ctf-USER')")
    conn.commit()
    conn.close()
    os.chmod("ctf.db", 0o444)  # Make the DB read-only after setup

# login_form_html = '''
# <!DOCTYPE html>
# <html>
# <head>
#     <title>CTF Login Challenge</title>
#     <style>
#         body {
#             font-family: 'Segoe UI', sans-serif;
#             background-color: #f4f6f8;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             height: 100vh;
#         }

#         .login-box {
#             background-color: white;
#             padding: 40px 30px;
#             border-radius: 12px;
#             box-shadow: 0 0 15px rgba(0,0,0,0.1);
#             width: 300px;
#             text-align: center;
#         }

#         .login-box h2 {
#             margin-bottom: 20px;
#             color: #2d3748;
#         }

#         input[type="text"] {
#             width: 100%;
#             padding: 10px;
#             margin: 10px 0 20px;
#             border: 1px solid #ccc;
#             border-radius: 6px;
#             font-size: 14px;
#         }

#         button {
#             background-color: #3182ce;
#             color: white;
#             padding: 10px 20px;
#             border: none;
#             border-radius: 6px;
#             font-size: 15px;
#             cursor: pointer;
#             transition: background-color 0.2s;
#         }

#         button:hover {
#             background-color: #2b6cb0;
#         }
#     </style>
# </head>
# <body>
#     <div class="login-box">
#         <h2> CTF Login</h2>
#         <form method="POST" action="/">
#             <input type="text" name="username" placeholder="Username" required>
#             <input type="text" name="password" placeholder="Password" required>
#             <button type="submit">Login</button>
#         </form>
#     </div>
# </body>
# </html>
# '''

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
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

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
