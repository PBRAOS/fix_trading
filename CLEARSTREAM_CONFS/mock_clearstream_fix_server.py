import socket
import threading

def handle_client(conn, addr):
    print(f"📡 Connection from {addr}")
    try:
        data = conn.recv(4096)
        if data:
            print(f"📨 Received: {data.decode(errors='ignore')}")
            # Simulate a basic ExecutionReport response
            response = (
                "8=FIX.4.2"  # BeginString
                "35=8"       # MsgType = ExecutionReport
                "150=0"      # ExecType = New
                "39=0"       # OrdStatus = New
                "37=ORDERID123"  # OrderID
                "17=EXECID123"   # ExecID
                "11=CLORDID123"  # ClOrdID
                "54=1"           # Side = Buy
                "55=FAKE123"     # Symbol
                "151=0"          # LeavesQty
                "14=100"         # CumQty
                "6=100.00"       # AvgPx
                "10=000"         # Checksum
            )
            conn.sendall(response.encode())
    finally:
        conn.close()

def run_mock_fix_server(host="0.0.0.0", port=9899):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"✅ Mock Clearstream FIX Server listening on {host}:{port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    run_mock_fix_server()
