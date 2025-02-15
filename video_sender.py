import socket
import cv2
import pickle
import struct

# Ngrok TCP Address
HOST = "0.tcp.in.ngrok.io"  # Replace with your Ngrok-assigned host
PORT = 17859  # Replace with your Ngrok-assigned external port

print(f"Connecting to {HOST}:{PORT}...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    print("Connected! Streaming live video...")

    cap = cv2.VideoCapture(0)  # Open the webcam
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(" Failed to capture frame.")
            break

        # Serialize frame
        data = pickle.dumps(frame)
        size = struct.pack("Q", len(data))  # Pack size as unsigned long long (8 bytes)
        
        try:
            sock.sendall(size + data)
        except socket.error as e:
            print(f"Socket error: {e}")
            break

except (ConnectionRefusedError, socket.error) as e:
    print(f"Connection failed: {e}")
except KeyboardInterrupt:
    print("\n Stopping video stream...")
finally:
    print(" Closing connection...")
    if 'cap' in locals() and cap.isOpened():
        cap.release()
    sock.close()
    print(" Connection closed.")
