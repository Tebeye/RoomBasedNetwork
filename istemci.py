import socket
import argparse

# Sunucu ayarları
HOST = '127.0.0.1'
PORT = 12345

# Komut satırı argümanlarını işleme
parser = argparse.ArgumentParser(description='İstemci için UUID belirleme.')
parser.add_argument('-uuid', type=str, help='Sunucu tarafından kullanılacak UUID')
args = parser.parse_args()

# Sunucuya bağlanma
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Oda kimliği ve oturum kimliğini sunucudan al
room_id = ""
session_id = ""

if args.uuid:
    room_id = args.uuid.split(',')
else:
    # Sunucudan oda kimliği ve oturum kimliğini al
    response = client_socket.recv(1024).decode('utf-8')
    room_id, session_id = response.split(',')
    print(f"Oda kimligim: {room_id}, Oturum kimligim: {session_id}")

while True:
    message = input()
    client_socket.send(message.encode('utf-8'))

client_socket.close()
