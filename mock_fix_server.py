import socket
import threading

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received from FIX client: {data.decode(errors='ignore')}")
            conn.sendall(b'8=FIX.4.2|9=12|35=8|10=128|'.replace(b'|', b'\x01'))
    finally:
        conn.close()

def start_server(host='0.0.0.0', port=5001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Mock FIX Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
