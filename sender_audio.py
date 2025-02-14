import socket
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

HOST = "0.tcp.in.ngrok.io"  # Ngrok assigned address
PORT = 11107  # Ngrok assigned port

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Sending live audio...")

try:
    while True:
        data = stream.read(CHUNK)
        sock.sendall(data)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
