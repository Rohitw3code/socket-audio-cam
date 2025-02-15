import socket
import cv2
import pickle
import struct

# Ngrok TCP Address
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 5000  # Use the same port as the sender

print(f"🔗 Starting server on {HOST}:{PORT}...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

conn, addr = sock.accept()
print(f"✅ Connection established from {addr}")

data_buffer = b""
payload_size = struct.calcsize("Q")

try:
    while True:
        while len(data_buffer) < payload_size:
            packet = conn.recv(4096)  # Receive data in chunks
            if not packet:
                break
            data_buffer += packet
        
        packed_size = data_buffer[:payload_size]
        data_buffer = data_buffer[payload_size:]
        frame_size = struct.unpack("Q", packed_size)[0]
        
        while len(data_buffer) < frame_size:
            data_buffer += conn.recv(4096)
        
        frame_data = data_buffer[:frame_size]
        data_buffer = data_buffer[frame_size:]
        
        frame = pickle.loads(frame_data)
        cv2.imshow("Live Stream", frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except Exception as e:
    print(f"⚠️ Error: {e}")
finally:
    print("🔻 Closing connection...")
    conn.close()
    sock.close()
    cv2.destroyAllWindows()
    print("✅ Server stopped.")
