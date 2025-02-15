import socket
import pyaudio

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Ngrok TCP Address
HOST = "0.tcp.in.ngrok.io"  # Replace with your Ngrok-assigned host
PORT = 14231  # Replace with your Ngrok-assigned external port

print(f"🔗 Connecting to {HOST}:{PORT}...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    print("✅ Connected! Streaming live audio...")

    # Initialize Audio Stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            sock.sendall(data)
        except OSError as e:
            print(f"⚠️ Audio error: {e}")
            break
except (ConnectionRefusedError, socket.error) as e:
    print(f"❌ Connection failed: {e}")
except KeyboardInterrupt:
    print("\n🛑 Stopping audio stream...")
finally:
    print("🔻 Closing connection...")
    if 'stream' in locals() and stream.is_active():
        stream.stop_stream()
        stream.close()
    if 'audio' in locals():
        audio.terminate()
    sock.close()
    print("✅ Connection closed.")
