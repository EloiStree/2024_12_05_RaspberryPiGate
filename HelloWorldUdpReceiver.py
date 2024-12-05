
print("Hello World SSH Raspberry pi 3")


import socket
import netifaces

def get_ip_addresses():
    ip_addresses = []
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for address in addresses[netifaces.AF_INET]:
                ip_addresses.append(address['addr'])
    return ip_addresses

def listen_udp(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    print(f"Listening for UDP messages on port {port}...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received message from {addr}: {data.decode()}")

if __name__ == "__main__":
    print("IP addresses of the computer:")
    for ip in get_ip_addresses():
        print(ip)
    
    listen_udp(7000)