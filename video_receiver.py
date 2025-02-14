import cv2
import socket
import pickle
import struct

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '0.0.0.0'  # Listen on all available interfaces
port = 9999

server_socket.bind((host_ip, port))
server_socket.listen(5)
print("Waiting for connection...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

data = b""
payload_size = struct.calcsize("Q")  # Size of packed message size

while True:
    while len(data) < payload_size:
        packet = conn.recv(4 * 1024)  # Receive in chunks
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]  # Unpack message size

    while len(data) < msg_size:
        data += conn.recv(4 * 1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)  # Deserialize frame
    cv2.imshow("Receiving...", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

conn.close()
cv2.destroyAllWindows()
