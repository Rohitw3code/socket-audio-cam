import socket
import pyaudio

# Audio settings
CHUNK = 1024  # Size of each chunk
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Sampling rate

# Server details
HOST = "192.168.188.135"  # Replace with the receiver's IP address
PORT = 5000

# Initialize audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Sending live audio...")

try:
    while True:
        data = stream.read(CHUNK)
        sock.sendto(data, (HOST, PORT))
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
