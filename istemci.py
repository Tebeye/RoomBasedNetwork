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

# Oda kimliğini sunucuya gönder
room_id = ""

if args.uuid:
    room_id = args.uuid
else:
    # Sunucudan oda kimliği al
    room_id = client_socket.recv(1024).decode('utf-8')

print(f"Oda kimligim: {room_id}")

while True:
    message = input()
    client_socket.send(message.encode('utf-8'))

client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='İstemci için UUID belirleme.')
    parser.add_argument('-uuid', type=str, help='İstemci tarafından kullanılacak UUID')
    args = parser.parse_args()

    # Sunucu tarafından verilen UUID'yi veya otomatik olarak oluşturulan UUID'yi al
    if args.uuid:
        room_id = args.uuid
    else:
        room_id = input("Oda kimliğiniz: ")

    main()