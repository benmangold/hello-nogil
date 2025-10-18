#!/usr/bin/env python3
"""
Simple multithreaded web server demonstrating Python 3.14 free-threading (no GIL).
Run with: python -X gil=0 server.py
"""

import socket
import threading
import time
import sys
from datetime import datetime


def handle_client(conn, addr):
    """Handle a single client connection in its own thread."""
    try:
        # Read the HTTP request
        request = conn.recv(1024).decode('utf-8')

        # Simulate some CPU-intensive work that benefits from true parallelism
        # With GIL disabled, multiple threads can actually run this in parallel
        result = 0
        for i in range(1000000):
            result += i

        # Get current thread info
        thread_name = threading.current_thread().name
        thread_id = threading.get_ident()

        # Build HTTP response
        response_body = f"""<!DOCTYPE html>
<html>
<head>
    <title>Free-Threaded Python Server</title>
    <style>
        body {{ font-family: monospace; padding: 20px; }}
        .info {{ background: #f0f0f0; padding: 10px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>Hello from Python 3.14 (GIL Disabled)! 🚀</h1>
    <div class="info">
        <strong>Connection Info:</strong><br>
        Client: {addr[0]}:{addr[1]}<br>
        Thread: {thread_name}<br>
        Thread ID: {thread_id}<br>
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        Computation Result: {result}
    </div>
    <p>This request was handled by a true parallel thread!</p>
    <p>Active threads: {threading.active_count()}</p>
</body>
</html>"""

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{response_body}"
        )

        conn.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()


def run_server(host='0.0.0.0', port=8000):
    """Run the multithreaded web server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"🚀 Free-threaded server running on http://{host}:{port}")
    
    if hasattr(sys, '_is_gil_enabled'):
        gil_status = sys._is_gil_enabled()
        if gil_status:
            print("The GIL is currently ENABLED.")
        else:
            print("The GIL is currently DISABLED.")
    else:
        print("sys._is_gil_enabled() is not available in this Python version.")
        print("The GIL is likely enabled by default in older versions.")   
        print(f"   Press Ctrl+C to stop\n")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"📥 Connection from {addr[0]}:{addr[1]} - spawning thread")

            # Create a new thread for each request
            # With GIL disabled, these threads can truly run in parallel!
            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
    finally:
        server_socket.close()


if __name__ == '__main__':
    run_server()