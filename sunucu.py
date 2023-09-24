import socket
import argparse
import uuid
import threading
import Game
import Client

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
def handle_client(client_socket, room_id, session_id):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"Istemci {room_id} ayrildi.")
                del clients[room_id][session_id]
                if not clients[room_id]:
                    del clients[room_id]
                break
            print(f"Mesaj alindi odasi {room_id}, oturum {session_id}: {data.decode('utf-8')}")

            # Ortak UUID'ye sahip istemcilere mesajı ilet
            if room_id in clients:
                for other_session_id, other_client_socket in clients[room_id].items():
                    if other_session_id != session_id:
                        try:
                            other_client_socket.send(data)
                        except Exception as e:
                            print(f"Hata: {str(e)}")
                            # Hata durumunda bağlantıları temizle
                            del clients[room_id][other_session_id]
                            if not clients[room_id]:
                                del clients[room_id]
        except Exception as e:
            print(f"Hata: {str(e)}")
            del clients[room_id][session_id]
            if not clients[room_id]:
                del clients[room_id]
            break

# Sunucu başlatma ve istemci bağlantılarını kabul etme
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Sunucu {HOST}:{PORT} dinleniyor...")

    while True:
        client_socket, addr = server.accept()
        print(f"Yeni istemci baglandi: {addr}")
        
        # İstemci tarafından sağlanan UUID veya sunucu tarafından otomatik olarak oluşturulan UUID
        if args.uuid:
            room_id = args.uuid
    
        else:
            room_id = str(uuid.uuid4())
        
        # İstemcinin bağlandığı bağlantı noktasını al
        _, client_port = addr
        # Benzersiz bir oturum kimliği (session_id) oluştur
        session_id = str(uuid.uuid4())
        
        # Oda kimliği altında oturumları sakla
        if room_id not in clients:
            clients[room_id] = {}
        
        clients[room_id][session_id] = client_socket
        
        # İstemciye oda kimliği ve oturum kimliğini gönder
        client_socket.send(f"Oda kimliginiz: {room_id}, Oturum kimliginiz: {session_id}".encode())
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket, room_id, session_id))
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
