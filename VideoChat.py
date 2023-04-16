import multiprocessing
import subprocess
from vidstream import *
from cryptography.fernet import Fernet
import socket
import time
import sys

# Generate a key for Fernet encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Enter your IP address and the receiver's IP address
local_ip = ''
receiver_ip = ''

# Method to check if the destination is reachable
def isDestinationReacheable(ip_address):
    try:
        hostname = ip_address
        result = subprocess.run(["ping", hostname], capture_output=True, text=True)
        if ("Request timed out." or "unreachable") in result.stdout:
            print(f"{ip_address} is not reachable")
            sys.exit()
        else:
            print(f'Destination {ip_address} is reachable')

    except socket.error:
        print(f"{ip_address} is not reachable")
        sys.exit()

# Method to encrypt audio
def encrypt_audio(audio):
    return cipher_suite.encrypt(audio)

def decrypt_audio(encrypted_audio):
    return cipher_suite.decrypt(encrypted_audio)

def start_audio_receiver():
    audio_receiving_port = AudioReceiver(local_ip, 6666)
    audio_receiving_port.start_server()

def start_audio_sender():
    audio_sender_port = AudioSender(receiver_ip, 6666)
    audio_sender_port.audio_thread = True
    audio_sender_port.audio_callback = lambda audio_frames: [encrypt_audio(audio_frame) for audio_frame in audio_frames]
    audio_sender_port.start_stream()

def start_video_receiver():
    receiving = StreamingServer(local_ip, 9999)
    receiving.start_server()

def start_video_sender():
    sending = CameraClient(receiver_ip, 9999)
    time.sleep(5) # Wait for server to start
    sending.start_stream()


def start_audio_receiver_decrypt():
    audio_receiving_port = AudioReceiver(local_ip, 7777)
    audio_receiving_port.audio_thread = True
    audio_receiving_port.audio_callback = lambda audio_frames: [decrypt_audio(audio_frame) for audio_frame in audio_frames]
    audio_receiving_port.start_server()

def start_audio_sender_decrypt():
    audio_sender_port = AudioSender(receiver_ip, 7777)
    audio_sender_port.start_stream()


if __name__ == "__main__":
    isDestinationReacheable(receiver_ip)
    print(f'Your IP address is : {local_ip}')
    print(f'Target IP address is : {receiver_ip}')
    print('Audio is being encrypted..')
    
    audio_receiver_process = multiprocessing.Process(target=start_audio_receiver)
    audio_sender_process = multiprocessing.Process(target=start_audio_sender)
    video_receiver_process = multiprocessing.Process(target=start_video_receiver)
    video_sender_process = multiprocessing.Process(target=start_video_sender)
    audio_receiver_decrypt_process = multiprocessing.Process(target=start_audio_receiver_decrypt)
    audio_sender_decrypt_process = multiprocessing.Process(target=start_audio_sender_decrypt)
    audio_receiver_process.start()
    audio_sender_process.start()
    video_receiver_process.start()
    video_sender_process.start()
    audio_receiver_decrypt_process.start()
    audio_sender_decrypt_process.start()

    while True:
        if input("") != 'STOP':
            print('connected')
            continue
        else:
            break

    audio_receiver_process.terminate()
    audio_sender_process.terminate()
    video_receiver_process.terminate()
    video_sender_process.terminate()
    audio_receiver_decrypt_process.terminate()
    audio_sender_decrypt_process.terminate()
