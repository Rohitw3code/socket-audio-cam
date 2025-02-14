import socket
import pyaudio

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Server details
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

# Initialize audio playback
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True,
                    frames_per_buffer=CHUNK)

print("Receiving live audio...")

try:
    while True:
        data, addr = sock.recvfrom(CHUNK * 2)  # 2 bytes per frame
        stream.write(data)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
