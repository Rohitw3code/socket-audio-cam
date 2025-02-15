import cv2
import socket
import pickle
import struct

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = ''  # Replace with receiver's IP address
port = 9999

client_socket.connect((host_ip, port))
print("Connected to receiver.")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Serialize frame
    data = pickle.dumps(frame)
    message_size = struct.pack("Q", len(data))  # Pack message size

    # Send frame size first, then frame data
    client_socket.sendall(message_size + data)

    # Show the sender's feed (optional)
    cv2.imshow("Sending...", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
client_socket.close()
cv2.destroyAllWindows()
