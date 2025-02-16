import socket
import cv2
import pickle
import struct
import pyaudio
import numpy as np

# Replace with your ngrok TCP forwarding address
HOST = '0.0.0.0'  # Bind to all interfaces (local server)
PORT = 5000  # Must match ngrok forwarding port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected to {addr}")

# Audio setup (Matching the sender settings)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050  # Must match sender

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

data_buffer = b""

while True:
    # Receive video frame size
    while len(data_buffer) < struct.calcsize("Q"):
        data_buffer += conn.recv(4096)
    
    msg_size = struct.unpack("Q", data_buffer[:struct.calcsize("Q")])[0]
    data_buffer = data_buffer[struct.calcsize("Q"):]

    while len(data_buffer) < msg_size:
        data_buffer += conn.recv(4096)

    frame_data = data_buffer[:msg_size]
    data_buffer = data_buffer[msg_size:]

    # Decode JPEG frame
    frame = pickle.loads(frame_data)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow("Receiver", frame)

    # Receive and play audio
    while len(data_buffer) < struct.calcsize("Q"):
        data_buffer += conn.recv(4096)
    
    audio_size = struct.unpack("Q", data_buffer[:struct.calcsize("Q")])[0]
    data_buffer = data_buffer[struct.calcsize("Q"):]

    while len(data_buffer) < audio_size:
        data_buffer += conn.recv(4096)

    audio_data = data_buffer[:audio_size]
    data_buffer = data_buffer[audio_size:]

    stream.write(audio_data)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
audio.terminate()
conn.close()
server_socket.close()
