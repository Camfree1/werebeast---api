from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {
            "status": "server is working"
        }

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
        except:
            data = {}

        response = {
            "success": True,
            "message": "route working",
            "received": data
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), handler)
    print("Server running on port", port)
    server.serve_forever()
