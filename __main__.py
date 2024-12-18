import psutil
from voyager import Voyager
from dotenv import load_dotenv
import os
import socket
import struct
import json
from selector import select_option


def to_varint(n):
    """Convert integer to VarInt (used in Minecraft networking)."""
    byte_array = bytearray()
    while (n & ~0x7F) != 0:
        byte_array.append((n & 0x7F) | 0x80)
        n >>= 7
    byte_array.append(n)
    return bytes(byte_array)


def construct_handshake_packet(ip_addr, port_number):
    """Constructs the Handshake packet for the Minecraft server."""
    # Packet ID for Handshake (0x00)
    packet_id = b"\x00"
    # Protocol Version (as of 1.19, protocol version is 759)
    protocol_version = to_varint(759)
    # IP address
    ip_address_bytes = ip_addr.encode("utf-8")
    ip_address_length = to_varint(len(ip_address_bytes))
    # Port number
    port_bytes = struct.pack("!H", port_number)
    # Next state (0x01 for status)
    next_state = b"\x01"

    # Combine all parts into a Handshake packet
    handshake_packet = (
        packet_id +
        protocol_version +
        ip_address_length +
        ip_address_bytes +
        port_bytes +
        next_state
    )

    # Prepend the length of the packet as a VarInt
    handshake_length = to_varint(len(handshake_packet))
    full_handshake_packet = handshake_length + handshake_packet

    return full_handshake_packet

def send_handshake_and_status(sock, handshake_packet):
    """Sends the Handshake packet and Status Request packet to the server."""
    sock.sendall(handshake_packet)
    # Send the Status Request packet (1 byte, 0x00)
    status_request_packet = b"\x01\x00"  # Length of 1 (VarInt) + 0x00 (Packet ID)
    sock.sendall(status_request_packet)


def verify_minecraft_server(ip_addr, port_number):
    sock = None
    try:
        # Connect to the server with a timeout
        sock = socket.create_connection((ip_addr, port_number), timeout=5)

        # Construct the Handshake packet
        full_handshake_packet = construct_handshake_packet(ip_addr, port_number)
        # Send the Handshake packet and Status Request
        send_handshake_and_status(sock, full_handshake_packet)

        # Read the response
        # Read the length of the packet (VarInt)
        to_varint(read_varint(sock))
        # Read the Packet ID (VarInt, not needed further)
        read_varint(sock)
        # Read the JSON Data (as a string)
        json_length = read_varint(sock)  # Length of the JSON string
        response = sock.recv(json_length).decode("utf-8")

        # Parse and verify the JSON response
        server_data = json.loads(response)

        if "description" in server_data and "players" in server_data:
            #print(f"Found Minecraft server on port {port_number}")
            return True
        else:
            #print(f"Port {port_number} is not a valid Minecraft server.")
            return False

    except Exception as e:
        #print(f"Exception on port {port_number}: {e}")
        return False

    finally:
        if sock is not None:
            sock.close()


def read_varint(sock):
    """Reads a VarInt from the socket."""
    value = 0
    size = 0
    while True:
        byte = sock.recv(1)
        if len(byte) == 0:
            raise IOError("Unexpected end of stream while reading VarInt")
        byte = ord(byte) if isinstance(byte, bytes) else byte  # Extract int from byte
        value |= (byte & 0x7F) << (7 * size)
        size += 1
        if size > 5:
            raise IOError("VarInt is too big.")
        if not (byte & 0x80):
            break
    return value

def find_minecraft_java_port():
    """
    Finds the port number on which a Minecraft Java server is listening.

    Returns:
        int: The port number if found, otherwise None.
    """
    # Iterate over all network connections
    for conn in psutil.net_connections(kind='inet'):
        # Check if the connection is listening
        if conn.status == psutil.CONN_LISTEN:
            try:
                # Check the process associated with this connection
                process = psutil.Process(conn.pid)
                if 'java' in process.name().lower():
                    # Check for a common identifier of Minecraft server in command line args
                    cmdline = process.cmdline()
                    if any('minecraft' in arg.lower() for arg in cmdline):
                        if verify_minecraft_server("127.0.0.1", conn.laddr.port):
                            return conn.laddr.port
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    return None

def create_new_checkpoint(skill_library_path, default_prompt=""):
    """Creates a new checkpoint directory and returns its sanitized name."""
    prompt = "Enter a name for the new checkpoint" + (f" ({default_prompt}): " if default_prompt else ": ")
    checkpoint_name = input(prompt).strip() or default_prompt
    sanitized_name = "".join(c for c in checkpoint_name if c.isalnum() or c in ('-', '_')).rstrip()
    new_checkpoint_path = os.path.join(skill_library_path, sanitized_name)
    os.makedirs(new_checkpoint_path)
    return sanitized_name

if __name__ == "__main__":

    print("                  _   _                                   ")
    print("                 | | | |                                  ")
    print("                 | | | | ___  _   _  __ _  __ _  ___ _ __ ")
    print("                 | | | |/ _ \| | | |/ _` |/ _` |/ _ \ '__|")
    print("                 \ \_/ / (_) | |_| | (_| | (_| |  __/ |   ")
    print("                  \___/ \___/ \__, |\__,_|\__, |\___|_|   ")
    print("                               __/ |       __/ |          ")
    print("                              |___/       |___/           ")
    print()
    print("        An Open-Ended Embodied Agent with Large Language Models")
    print()
    print("                          original authors:")
    print("             Guanzhi Wang and Yuqi Xie and Yunfan Jiang and")
    print("              Ajay Mandlekar and Chaowei Xiao and Yuke Zhu")
    print("                  and Linxi Fan and Anima Anandkumar")
    print()

    # Load environment variables from .env file
    load_dotenv()

    # Find the port number for the Minecraft Java server
    mc_port = find_minecraft_java_port()

    # Get OpenAI API key from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("OPENAI_MODEL")

    if mc_port is None:
        print()
        print("\033[41;33m************************************************************************* \033[0m")
        print("\033[41;33m*** Unable to connect to Minecraft. Please make sure Minecraft is     *** \033[0m")
        print("\033[41;33m*** running and that 'Open to LAN' has been clicked.                  *** \033[0m")
        print("\033[41;33m************************************************************************* \033[0m")
        print()
        exit()


    skill_library_path = "ckpts"
    selected_checkpoint = None
    resume = False

    if not os.path.exists(skill_library_path):
        os.makedirs(skill_library_path)
        selected_checkpoint = create_new_checkpoint(skill_library_path, "default")
        resume = True
    else:
        try:
            checkpoints = [
                name for name in os.listdir(skill_library_path)
                if os.path.isdir(os.path.join(skill_library_path, name))
            ]
            checkpoints.append("New...")
            selected_checkpoint = select_option(checkpoints)
            
            if selected_checkpoint == "New...":
                selected_checkpoint = create_new_checkpoint(skill_library_path)
                resume = False
        except FileNotFoundError:
            checkpoints = []
    
    # Initialize the Voyager instance with the Minecraft port and OpenAI API key
    voyager = Voyager(
        mc_port=mc_port,
        openai_api_key=openai_api_key,
        action_agent_model_name=openai_model,
        curriculum_agent_model_name=openai_model,
        curriculum_agent_qa_model_name=openai_model,
        critic_agent_model_name=openai_model,
        skill_manager_model_name=openai_model,
        resume=resume,
        ckpt_dir = "ckpts\\" + selected_checkpoint
    )

    # Start lifelong learning
    voyager.learn()