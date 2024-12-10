## This code allows to received IID message from UDP package and ban/kick user
# if they send more than 16 bytes package or too much data per period of time.

# This server is in thrust mode. If user say it is index 7, it is index 7.
# When on Shared Server index should be linked to a user registerer in a database.

# Warning: In this model, one IP is one user.


import socket
import struct
import threading
from datetime import datetime
import time


SERVER_PORT_IN_LISTENER = 7000

# Constants
BAN_THRESHOLD = 10 * 1024 * 1024  # 10 MB in bytes

# Shared resources
ip_byte_count = {}
banned_ips = set()
kick_ips= set()
allow_ips= set()
ip_to_index_registered= {}
ip_to_index_guest= {}

ip_to_index_registered["81.240.94.97"]=42
int_guest_index = -1


lock = threading.Lock()

float_kick_countdown_time =10
# Current DateTime in python
current_time = datetime.now()
date_last_unkick_time = datetime.now()

# Relay on the local machine
local_port = [7001]

# Relay on the remote machine
remote_ipv4_port = ["81.240.94.97:7000"]



def broadcast_valide_iid(int_index, int_value, ulong_date):
    
    data = struct.pack('<iiQ', int_index, int_value, ulong_date)
    
    for port in local_port:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(data, ("127.0.0.1", port))
        udp_socket.close()
        
    for ip_port in remote_ipv4_port:
        ip, port = ip_port.split(":")
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(data, (ip, int(port)))
        udp_socket.close()
   
def received_index_integer_date(int_index: int, int_value: int, ulong_date: int):
    
    int_index = int(int_index)
    int_value = int(int_value)
    ulong_date = int(ulong_date)
    float_date = float(ulong_date)
    broadcast_valide_iid(int_index, int_value, int(ulong_date))
    print(f"Received integer: {int_value} at index {int_index} long {ulong_date} with date {datetime.fromtimestamp(float_date/100)}")




def date_ulong():
    return int(datetime.now().timestamp()*10000)


def ban(ip):
    print(f"---BAN---> {ip}")
    banned_ips.add(ip)

def kick(ip):
    print(f"---KICK---> {ip}")
    kick_ips.add(ip)
    

def udp_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", SERVER_PORT_IN_LISTENER))
    print("UDP server is listening on port 7000...")
    while True:
        data, addr = udp_socket.recvfrom(1024)  # Receive data
        
        source_ip = addr[0]
        byte_count = len(data)
        with lock:
            # Check if IP is banned
            if source_ip in banned_ips:
                print(f"---BANNED---> {source_ip}")
                continue
            if source_ip in kick_ips:
                print(f"---KICKED---> {source_ip}")
                continue
            
            int_user_index = 0
            if source_ip not in ip_to_index_registered:
                if source_ip not in ip_to_index_guest:
                    print("NEW GUEST: ", source_ip)
                    ip_to_index_guest.add(source_ip)
                    ip_to_index_guest[source_ip] = int_guest_index
                    int_guest_index -= 1
                else:
                    int_user_index = ip_to_index_guest[source_ip]
            else:
                int_user_index = ip_to_index_registered[source_ip]
                
            print(f"User index: {int_user_index} ({source_ip} |  {byte_count} bytes)")
            
            if byte_count > 16:
                # User of integer server are not suppose to send moer that 16 bytes IID lenght
                kick_ips.add(source_ip)  
                print(f"IP {source_ip} has been kick (over 16 bytes package).")
             
            int_value =0
            int_index =0
                
            if byte_count ==4:
                int_value = struct.unpack('<i', data)
                received_index_integer_date(0,int_value, date_ulong())
            
            elif byte_count == 8:
                int_index,int_value = struct.unpack('<ii', data)
                received_index_integer_date(int_index,int_value, date_ulong())
            
            elif byte_count == 12:
                int_value, ulong_date = struct.unpack('<iQ', data)
                received_index_integer_date(0,int_value,ulong_date)
            elif byte_count == 16:
                int_index,int_value, ulong_date = struct.unpack('<iiQ', data)
                received_index_integer_date(int_index,int_value, ulong_date)
            elif byte_count == 11 or byte_count == 10:
                ## 00 88 99 77 66 
                ## 0088997766
                ## 0088997766\n
                
                string_text = data.decode('utf-8').strip()
                try:
                    int_value = int(string_text)
                except ValueError:
                    kick(source_ip)
                    continue
                received_index_integer_date(0,int_value, date_ulong())
                print(f"Integer as ASCII/UTF8 \\n :{int_value} ({string_text}) ")
            else:
                kick(source_ip)  
            # Update the byte count for this IP
            if source_ip not in ip_byte_count:
                ip_byte_count[source_ip] = 0
            ip_byte_count[source_ip] += byte_count

            # Check if the IP exceeds the threshold
            if ip_byte_count[source_ip] > BAN_THRESHOLD:
                ban(source_ip)
                print(f"IP {source_ip} has been banned (over {BAN_THRESHOLD} bytes).")
                continue


        # Process the packet
        print(f"Received {byte_count} bytes from {source_ip}. Total: {ip_byte_count[source_ip]} bytes")
        
        
# Initialize variables
int_tick = 0
int_unban_tick = 360
int_unkick_tick = 1
banned_ips = set()
kick_ips = set()
ip_byte_count = {}
def manage_banned_ips():
    global int_tick
    print("Ban/Kick tick check started")
    while True:
        time.sleep(10)  # Wait for 10 seconds
        int_tick += 1
        
        # Unban logic
        if int_tick % int_unban_tick == 0:
            with lock:  # Ensure thread safety
                print(">>>>>>>>>> Unban all and reset byte count <<<<<<<<") 
                print("Total banned IPs:", len(banned_ips))
                print("Total bytes consumed:", sum(ip_byte_count.values()))
                
                ip_byte_count.clear()  # Reset byte count
                banned_ips.clear()  # Clear banned IPs
        
        # Unkick logic
        if int_tick % int_unkick_tick == 0:
            with lock:  # Ensure thread safety
                print(">>>>>>>>>> Unkick all <<<<<<<<") 
                print("Total kicked IPs:", len(kick_ips))
                kick_ips.clear()  # Clear kicked IPs


# Start the server and admin thread
server_thread = threading.Thread(target=udp_server, daemon=True)
admin_thread = threading.Thread(target=manage_banned_ips, daemon=True)

server_thread.start()
admin_thread.start()

# Keep the main thread alive
server_thread.join()
admin_thread.join()
