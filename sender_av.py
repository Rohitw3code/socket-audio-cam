import socket
import cv2
import pickle
import struct
import pyaudio

# Use your ngrok TCP forwarding address
NGROK_HOST = "0.tcp.in.ngrok.io"  # Replace with your ngrok hostname
NGROK_PORT = 11532  # Replace with your ngrok port

# Connect to ngrok TCP host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((NGROK_HOST, NGROK_PORT))

# Video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Audio capture (Lower Sample Rate for Compression)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050  # Lower sample rate for bandwidth efficiency

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print(f"Streaming to {NGROK_HOST}:{NGROK_PORT}")

while True:
    # Capture video frame
    ret, frame = cap.read()
    if not ret:
        break

    # Compress frame using JPEG encoding (80% quality)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, protocol=pickle.HIGHEST_PROTOCOL)

    # Pack frame size
    message_size = struct.pack("Q", len(data))

    # Capture and send audio
    audio_data = stream.read(CHUNK, exception_on_overflow=False)
    audio_size = struct.pack("Q", len(audio_data))

    # Send frame and audio
    client_socket.sendall(message_size + data + audio_size + audio_data)

cap.release()
stream.stop_stream()
stream.close()
audio.terminate()
client_socket.close()
