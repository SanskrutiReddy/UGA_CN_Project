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

def encrypt_audio(audio):
    return cipher_suite.encrypt(audio)

def decrypt_audio(encrypted_audio):
    return cipher_suite.decrypt(encrypted_audio)

if __name__ == "__main__":
    isDestinationReacheable(receiver_ip)
    print(f'Your IP address is : {local_ip}')
    print(f'Target IP address is : {receiver_ip}')
    print('Audio is being encrypted..')