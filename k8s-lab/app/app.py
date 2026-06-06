from http.server import HTTPServer, BaseHTTPRequestHandler
import os

NAME = os.environ.get("NAME", "World")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Hello App</title></head>
<body style="font-family:sans-serif; text-align:center; margin-top:100px;">
  <h1>Hello, {NAME}!</h1>
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print(f"Server started on port 8080, NAME={NAME}")
    server.serve_forever()