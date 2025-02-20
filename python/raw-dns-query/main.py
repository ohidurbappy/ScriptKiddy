import socket

def build_dns_query(domain):
    """Constructs a raw DNS query for the given domain."""
    # Generate a unique Transaction ID (16-bit)
    transaction_id = b"\xaa\xbb"

    # Flags: Standard Query (0x0100)
    flags = b"\x01\x00"

    # Questions: 1
    qdcount = b"\x00\x01"

    # Answer RRs, Authority RRs, Additional RRs: 0
    ancount = b"\x00\x00"
    nscount = b"\x00\x00"
    arcount = b"\x00\x00"

    # Header section
    header = transaction_id + flags + qdcount + ancount + nscount + arcount

    # Encode domain name in DNS format (e.g., "example.com" → "\x07example\x03com\x00")
    qname = b"".join(len(part).to_bytes(1, "big") + part.encode() for part in domain.split(".")) + b"\x00"

    # QTYPE: A (Host Address) (0x0001), QCLASS: IN (Internet) (0x0001)
    qtype = b"\x00\x01"
    qclass = b"\x00\x01"

    # Final query
    return header + qname + qtype + qclass

def parse_dns_response(response):
    """Parses a raw DNS response and extracts the IP addresses."""
    header = response[:12]  # First 12 bytes are the DNS header
    qname_end = response[12:].index(b"\x00") + 13  # Locate end of QNAME
    answer_section = response[qname_end + 4:]  # Skip QTYPE and QCLASS

    ip_addresses = []
    while answer_section:
        if len(answer_section) < 16:
            break

        # Extract the response fields
        ip_part = answer_section[-4:]  # Last 4 bytes should be the IPv4 address
        ip_address = ".".join(str(b) for b in ip_part)
        ip_addresses.append(ip_address)

        answer_section = answer_section[:-16]  # Move to the next answer (if any)

    return ip_addresses if ip_addresses else "No IP found"

def dns_query_udp(domain, dns_server="8.8.8.8", port=53):
    """Sends a raw DNS query over UDP and parses the response."""
    query = build_dns_query(domain)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)  # Set a timeout

    try:
        # Send query to the DNS server
        sock.sendto(query, (dns_server, port))

        # Receive response
        response, _ = sock.recvfrom(512)  # DNS responses are usually < 512 bytes
    except socket.timeout:
        return "Timeout: No response from server"
    finally:
        sock.close()

    return parse_dns_response(response)

# Example usage
print(dns_query_udp("example.com"))
