import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    sock.sendto("D".encode(), ("192.168.137.69", 4210))
    print("Packet sent")
    time.sleep(2)