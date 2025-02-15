import socket
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000  # Must match the port used in ngrok

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print("Waiting for connection...")

conn, addr = sock.accept()
print(f"Connected by {addr}")

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

print("Receiving live audio...")

try:
    while True:
        data = conn.recv(CHUNK * 2)  # Read data from the sender
        if not data:
            break
        stream.write(data)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    conn.close()
    sock.close()