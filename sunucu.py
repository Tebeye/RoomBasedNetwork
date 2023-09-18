import socket
import argparse
import uuid
import threading
# Komut satırı argümanlarını işleme
parser = argparse.ArgumentParser(description='Sunucu için UUID belirleme.')
parser.add_argument('-uuid', type=str, help='Sunucu tarafından kullanılacak UUID')
args = parser.parse_args()

# Sunucu ayarları
HOST = '127.0.0.1'
PORT = 12345

# Bağlantı noktalarını saklamak için bir sözlük
ports = {}
# İstemcileri saklamak için bir sözlük
clients = {}

# Ortak UUID'ler ve bunların bağlantı noktalarını saklamak için bir sözlük
common_uuids = {}

def handle_client(client_socket, room_id):
    while True:
        try:
            data = client_socket.recv(1024)
            for aaa in clients:
                print(f"Clients: {clients[aaa]}")
            if not data:
                print(f"Istemci {room_id} ayrildi.")
                del clients[room_id]
                del ports[client_socket]
                break
            print(f"Mesaj alindi odasi {room_id}: {data.decode('utf-8')}")

            # Ortak UUID'ye sahip istemcilere mesajı ilet
            if room_id in common_uuids:
                for other_room_id, other_client_socket in clients.items():
                    if other_room_id != room_id:
                        try:
                            other_client_socket['socket'].send(data)
                        except Exception as e:
                            print(f"Hata: {str(e)}")
                            del clients[other_room_id]
        except Exception as e:
            print(f"Hata: {str(e)}")
            del clients[room_id]
            del ports[client_socket]
            break

# Sunucu başlatma ve istemci bağlantılarını kabul etme
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Sunucu {HOST}:{PORT} dinleniyor...")

    while True:
        client_socket, addr = server.accept()
        print(f"Yeni istemci baglandi: {addr} ({ports.get(client_socket)})")
        
        # İstemci tarafından sağlanan UUID veya sunucu tarafından otomatik olarak oluşturulan UUID
        if args.uuid:
            room_id = args.uuid
        else:
            room_id = str(uuid.uuid4())
        
        # İstemcinin bağlandığı bağlantı noktasını al
        _, client_port = addr
        # Bağlantı noktasına ait oda kimliğini güncelle
        ports[client_socket] = room_id
        
        # Ortak UUID'ler listesine ekle (eğer istemci argüman olarak -uuid verirse)
        if args.uuid and args.uuid in common_uuids:
            common_uuids[args.uuid].append(room_id)
        else:
            common_uuids[room_id] = [room_id]
        
        clients[room_id] = {
            "socket": client_socket,
            "room_id": room_id
        }
        
        # İstemciye oda kimliğini gönder
        client_socket.send(f"Oda kimliginiz: {room_id}".encode())
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket, room_id))
        client_handler.start()


if __name__ == "__main__":
        # İstemci tarafından verilen UUID'yi al
    parser = argparse.ArgumentParser(description='Sunucu için UUID belirleme.')
    parser.add_argument('-uuid', type=str, help='Sunucu tarafından kullanılacak UUID')
    args = parser.parse_args()

    if args.uuid:
        common_uuids[args.uuid] = [args.uuid]  # Verilen UUID'yi ortak UUID listesine ekle
    else:
        args.uuid = str(uuid.uuid4())  # Eğer istemci argüman olarak UUID vermediyse, otomatik olarak oluştur

    main()
