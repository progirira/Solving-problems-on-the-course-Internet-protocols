import re
import socket
import argparse
import sys
from multiprocessing import Process


pattern_ip = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")


def tcp_scanner(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.05)
        try:
            sock.connect((host, port))
        except:
            pass
        else:
            print("TCP: порт {} открыт".format(port))


def udp_scanner(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.sendto(b"", (host, port))
            sock.settimeout(1)
            sock.recvfrom(1024)
            print("UDP: порт {} открыт".format(port))
        except socket.timeout:
            print("UDP: порт {} открыт".format(port))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP and UDP scanner")
    parser.add_argument('-i', "--ip", help="ip", required=True)
    parser.add_argument("-s", "--start", help="Beginning of range",
                        type=int, required=True)
    parser.add_argument("-e", "--end", help="Ending of range", type=int,
                        required=True)
    args = parser.parse_args()
    if not re.search(pattern_ip, args.ip):
        print("Некорректный ip адрес")
        sys.exit()
    for i in range(args.start, args.end):
        proc_tcp = Process(target=tcp_scanner, args=(args.ip, i))
        proc_udp = Process(target=udp_scanner, args=(args.ip, i))
        proc_tcp.start()
        proc_udp.start()
