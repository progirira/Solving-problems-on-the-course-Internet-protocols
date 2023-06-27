import socket
import struct
import time
import requests


def tracert(host: str, hops: int, timeout: int):
    try:
        target_host = socket.gethostbyname(host)
    except socket.gaierror:
        print("Введено неверное имя хоста")
    print(f"Трассировка до {target_host} ({host}) c максимальным количеством прыжков {hops} :")
    icmp_proto = socket.getprotobyname("icmp")
    try:
        for hop in range(1, hops + 1):
            try:
                icmp_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_RAW, icmp_proto)
            except socket.error as e:
                print(f"Error {e}")
            time_to_live = hop
            id = hop
            if (ping(target_host, icmp_socket, time_to_live, id, timeout)):
                icmp_socket.close()
                break
            icmp_socket.close()
    except KeyboardInterrupt:
        print("\n[END] EXITING TRACE  ")


def get_checksum(header):
    checksum = 0
    overflow = 0
    for i in range(0, len(header), 2):
        word = header[i] + (header[i + 1] << 8)
        checksum = checksum + word
        overflow = checksum >> 16
        while overflow > 0:
            checksum = checksum & 0xFFFF
            checksum = checksum + overflow
            overflow = checksum >> 16
    overflow = checksum >> 16
    while overflow > 0:
        checksum = checksum & 0xFFFF
        checksum = checksum + overflow
        overflow = checksum >> 16
    checksum = ~checksum
    checksum = checksum & 0xFFFF
    return checksum


def ping(target_host: str, icmp_socket: socket, time_to_live: int, id: int, timeout: int):
    try:
        print(f"{time_to_live}\t ", end="")
        checksum = 0
        header = struct.pack(
            "bbHHh", 8, 0, checksum, id, 1)
        checksum = get_checksum(header)
        header = struct.pack("bbHHh", 8,
                             0, checksum, id, 1)
        icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, time_to_live)
        icmp_socket.sendto(header, (target_host, 1))
        icmp_socket.settimeout(timeout)
        recv_packet, addr = icmp_socket.recvfrom(1024)
        hostname = ''
        try:
            host_details = socket.gethostbyaddr(addr[0])
            if len(host_details) > 0:
                hostname = host_details[0]
        except Exception:
            hostname = 'unknown'
        ip_url = "https://api.hackertarget.com/aslookup/?q=" + str(addr[0])
        req = requests.get(ip_url)
        auto_sys = req.text.split(",")
        start_time = time.time()
        ms = int((time.time() - start_time) * 1000.00)
        if len(auto_sys) >= 5:
            print(f'{ms} ms\t{hostname} [{addr[0]}], AS: {auto_sys[1]} , '
                  f'Provider:{auto_sys[3]} ,Country: {auto_sys[4]}')
        else:
            print(f'{ms}ms\t{hostname} [{addr[0]}]')

        if addr[0] == target_host:
            return True
    except socket.timeout:
        # ms = int((time.time() - start_time) * 1000.0)
        print('*\tRequest timed out.')
        return False
    return False


if __name__ == '__main__':
    dest = input("Введите имя хоста назначения: ")
    tracert(dest, 30, 1)
    a = input('нажмите ENTER для выхода')