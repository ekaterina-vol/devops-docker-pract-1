from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import psycopg2
from datetime import datetime

NAME = os.environ.get("NAME", "World")
DB_HOST = os.environ.get("DB_HOST", "postgres-service")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "appdb")
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASS = os.environ.get("DB_PASS", "apppassword")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            visited_at TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_visit():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visits (visited_at) VALUES (%s)", (datetime.now(),))
    conn.commit()
    cur.close()
    conn.close()

def get_visits():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT visited_at FROM visits ORDER BY visited_at DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            add_visit()
            visits = get_visits()
            rows_html = "".join(
                f"<li>{row[0].strftime('%Y-%m-%d %H:%M:%S')}</li>" for row in visits
            )
            html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Hello App</title></head>
<body style="font-family:sans-serif; text-align:center; margin-top:100px;">
  <h1>Hello, {NAME}!</h1>
  <h3>Последние визиты:</h3>
  <ul style="list-style:none;">{rows_html}</ul>
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print("Initializing DB...")
    init_db()
    print(f"Server started on port 8080, NAME={NAME}")
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()