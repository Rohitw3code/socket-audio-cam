import socket
import pickle
import struct
import numpy as np
import cv2


# Use ngrok TCP address
NGROK_HOST = "0.tcp.in.ngrok.io"  # Ngrok hostname
NGROK_PORT = 11532  # Ngrok forwarded port


print(f"Starting server on {HOST}:{PORT}...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(5)

conn, addr = sock.accept()
print(f"Connection established from {addr}")

data_buffer = b""
payload_size = struct.calcsize("Q")

try:
    while True:
        while len(data_buffer) < payload_size:
            packet = conn.recv(16384)  # Increased buffer size for faster reception
            if not packet:
                break
            data_buffer += packet
        
        packed_size = data_buffer[:payload_size]
        data_buffer = data_buffer[payload_size:]
        frame_size = struct.unpack("Q", packed_size)[0]
        
        while len(data_buffer) < frame_size:
            data_buffer += conn.recv(16384)  # Increased buffer size for faster frame retrieval
        
        frame_data = data_buffer[:frame_size]
        data_buffer = data_buffer[frame_size:]
        
        compressed_frame = pickle.loads(frame_data)
        frame = cv2.imdecode(compressed_frame, cv2.IMREAD_COLOR)  # Decompress frame
        
        cv2.imshow("Live Stream", frame)  # Display frame using OpenCV
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except Exception as e:
    print(f"Error: {e}")
finally:
    print("Closing connection...")
    conn.close()
    sock.close()
    cv2.destroyAllWindows()
    print("Server stopped.")