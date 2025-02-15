import socket
import pickle
import struct
import numpy as np
import cv2

# Ngrok TCP Address
HOST = "0.tcp.in.ngrok.io"  # Replace with your Ngrok-assigned host
PORT = 17859  # Replace with your Ngrok-assigned external port

print(f"Connecting to {HOST}:{PORT}...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    print("Connected! Streaming live video...")
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 30])  # Further compression
        data = pickle.dumps(compressed_frame, protocol=pickle.HIGHEST_PROTOCOL)  # Optimize serialization
        size = struct.pack("Q", len(data))  # Pack size as unsigned long long (8 bytes)
        
        try:
            sock.sendall(size + data)
        except socket.error as e:
            print(f"Socket error: {e}")
            break

except (ConnectionRefusedError, socket.error) as e:
    print(f"Connection failed: {e}")
except KeyboardInterrupt:
    print("Stopping video stream...")
finally:
    print("Closing connection...")
    cap.release()
    sock.close()
    print("Connection closed.")
