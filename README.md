# SQL Injection Login Challenge (Flag on Bypass)

This version of the challenge rewards participants with a flag **only if they bypass the login**.

## 👨‍💻 Challenge Details

- User table only: `admin / ctf-USER`
- SQL Injection needed to bypass login
- Successful login redirects to `/flag`
- `/flag` displays the challenge flag

## 🔐 Security

- SQLite DB is read-only after setup
- Flask-limiter limits brute force attempts
- Flask-CORS limits frontend domains
- Runs as non-root in Docker

## ▶️ Run It

```bash
docker build -t sqli-login-bypass .
docker run -p 5000:5000 sqli-login-bypass
