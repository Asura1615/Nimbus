import socket
import struct
from enum import Enum
import time
import re
from typing import Dict

server_ip = "0.0.0.0"
server_port = 8080
BUFFER_SIZE = 1024

NO_OF_ESP_IN_NETWORK = 1
ServerSocket = None
isMusicStarted = False
start_time = None
MAX_NO_OF_LED_STRIP_IN_ESP = 5

class LEDSTATE(Enum):
    POWERON = 1
    POWEROFF = 0

class Esp(object):
    
    def __init__(self, node_id:int, no_of_led_strip_in_it:int, ip_address):
        self.node_id = node_id
        self.no_of_led_strip_in_it = no_of_led_strip_in_it
        self.ip_address = ip_address
        self.last_state = 0b00000

    def send_command(self, ledstate:LEDSTATE, led_strip_nos:list):
        if len(led_strip_nos) > self.no_of_led_strip_in_it:
            raise Exception("LED strip out of range")
        fmt = "<B"
        state_to_deploy = self.create_led_state(ledstate, led_strip_nos)
        print(bin(state_to_deploy))
        packet = struct.pack(fmt, state_to_deploy)
        ServerSocket.sendto(packet, self.ip_address)
        self.last_state = state_to_deploy
    
    def create_led_state(self, state:LEDSTATE, led_list:list) -> int:
        led_state = self.last_state
        for led in led_list:
            if state == LEDSTATE.POWERON:
                led_state |= (1 << (led-1))     # turn ON
            elif state == LEDSTATE.POWEROFF:
                led_state &= ~(1 << (led-1))    # turn OFF
        return led_state

Espobj:Dict[int, Esp] = {}

try:
        # AF_INET specifies the IPv4 address family
        # SOCK_DGRAM specifies the User Datagram Protocol (UDP)
        ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        ServerSocket.bind((server_ip, server_port))
        print(f"UDP server up and listening on {server_ip}:{server_port}")
except socket.error as e:
        print(f"Error binding socket: {e}")
        raise

my_pattern = [
[1, LEDSTATE.POWERON, {1: [1,2,3]}],
[11, LEDSTATE.POWERON, {1: [4,5]}],
[15, LEDSTATE.POWEROFF, {1:[4,2,1]}]
]

def get_time():
    return time.time() - start_time

def reset_time():
    global start_time
    start_time = time.time()

def checkformusic(data:bytes):
    global isMusicStarted
    print(data.decode('utf-8'))
    if data.decode('utf-8') == "ON":
        isMusicStarted = True
    else:
        isMusicStarted = False

if __name__ == "__main__":
    print("UDP Control Server")
    print("------------------------------")
    print("Commands:")
    print("<Time> <state>   (example: 12345 3 1)")
    print("  q                     quit")
    print("------------------------------")
    while True:
        client_esp = ServerSocket.recvfrom(255)
        if len(client_esp[0]) == 1:
            node_id = struct.unpack("<B", client_esp[0])[0]
            Espobj[int(node_id)] = Esp(int(node_id), MAX_NO_OF_LED_STRIP_IN_ESP, client_esp[1])
        else:
            checkformusic(client_esp[0])
            break

        print("Connection received")
        
        if NO_OF_ESP_IN_NETWORK == len(Espobj):
            print("All esp are connected now")
            break
    
    curr_command_index = 0
        # if not isMusicStarted:
        #     print("Music not playing all esp are here")
        #     client_music = ServerSocket.recvfrom(255)
        #     print("Got some data")
        #     checkformusic(client_music)
        #     continue

    print("Music started and esp are here")

    if curr_command_index == 0:
            start_time = time.time()

    for command in my_pattern:
            print("Executing command")
            time_to_fire_comm, led_state,led_to_change = command[0], command[1], command[2]
            while True:
                if time_to_fire_comm <= get_time():
                    for esp_index in led_to_change.keys():
                        print(esp_index)
                        print(Espobj)
                        Espobj[esp_index].send_command(led_state, led_to_change[esp_index])
                    break
            curr_command_index +=1
