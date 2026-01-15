import pygame
import time
import socket

ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
IP_ADDR = "192.168.37.1"
PORT = 8080

def play_song(file_path):
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f"Playing: {file_path}")
        ServerSocket.sendto("ON".encode(), (IP_ADDR, PORT))
        # Keep the script running while the music plays
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except pygame.error as e:
        print(f"Error playing music: {e}")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    finally:
        # Optional: stop the mixer when done
        pygame.mixer.music.stop()
        ServerSocket.sendto("OFF".encode(), (IP_ADDR, PORT))

# Replace 'path/to/your/song.mp3' with the actual path to your song file
play_song('song.mp3')
