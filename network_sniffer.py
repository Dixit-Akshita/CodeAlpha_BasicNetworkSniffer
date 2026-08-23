from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
from collections import Counter

# Terminal colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

packet_count = 0
protocol_count = Counter()


def packet_callback(packet):
    global packet_count

    if IP not in packet:
        return

    packet_count += 1

    source_ip = packet[IP].src
    destination_ip = packet[IP].dst
    packet_length = len(packet)

    # Identify protocol and ports
    if TCP in packet:
        protocol = "TCP"
        source_port = packet[TCP].sport
        destination_port = packet[TCP].dport

    elif UDP in packet:
        protocol = "UDP"
        source_port = packet[UDP].sport
        destination_port = packet[UDP].dport

    elif ICMP in packet:
        protocol = "ICMP"
        source_port = "N/A"
        destination_port = "N/A"

    else:
        protocol = "Other"
        source_port = "N/A"
        destination_port = "N/A"

    protocol_count[protocol] += 1

    # Display packet information
    print(f"\n{CYAN}{'=' * 55}{RESET}")
    print(f"{BOLD}{MAGENTA}              PACKET #{packet_count}{RESET}")
    print(f"{CYAN}{'=' * 55}{RESET}")

    print(f"{GREEN}Source IP       :{RESET} {source_ip}")
    print(f"{GREEN}Destination IP  :{RESET} {destination_ip}")
    print(f"{YELLOW}Protocol        :{RESET} {protocol}")
    print(f"{YELLOW}Source Port     :{RESET} {source_port}")
    print(f"{YELLOW}Destination Port:{RESET} {destination_port}")
    print(f"{BLUE}Packet Length   :{RESET} {packet_length} bytes")

    # Payload information
    if Raw in packet:
        payload = packet[Raw].load
        print(f"{BLUE}Payload Length  :{RESET} {len(payload)} bytes")
        print(f"{BLUE}Payload         :{RESET} {payload[:50]}")
    else:
        print(f"{BLUE}Payload         :{RESET} No Raw payload")


def show_summary():
    print(f"\n\n{CYAN}{'=' * 55}{RESET}")
    print(f"{BOLD}{MAGENTA}                 CAPTURE SUMMARY{RESET}")
    print(f"{CYAN}{'=' * 55}{RESET}")

    print(f"{GREEN}Total IP Packets:{RESET} {packet_count}")

    if protocol_count:
        print(f"\n{YELLOW}Protocol Statistics:{RESET}")

        for protocol, count in protocol_count.items():
            print(f"  {protocol}: {count}")


# Program Header
print()
print(f"{CYAN}{'=' * 55}{RESET}")
print(f"{BOLD}{MAGENTA}           🔐 BASIC NETWORK PACKET SNIFFER{RESET}")
print(f"{CYAN}{'=' * 55}{RESET}")
print(f"{GREEN}Capturing network packets...{RESET}")
print(f"{YELLOW}Press Ctrl+C to stop.{RESET}")
print()

try:
    sniff(prn=packet_callback)

except KeyboardInterrupt:
    print(f"\n{YELLOW}Stopping packet capture...{RESET}")

finally:
    show_summary()