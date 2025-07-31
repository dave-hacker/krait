import argparse
from random import randint
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM

BUFFER_SIZE = 1024
FTP_PORT = 21

def parse_args():
    """
    Parses command-line arguments and returns the parsed arguments object.
    """
    parser = argparse.ArgumentParser(description="A simple script with command-line arguments.")

    # Add arguments
    parser.add_argument("-i", "--ip-address", type=str, help="Target IP address of FTP server")
    parser.add_argument("-c","--command", type=str, help="Action to perform. E.g. upload, list, download, delete")
    parser.add_argument("-u","--username", type=str, help="Specify FTP username")
    parser.add_argument("-p","--password", type=bool, action="store_true", help="Add if a password is required for authentication (will be requested at runtime)")
    # parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    return parser.parse_args()

def upload():
    """
    # Tell the server we are about to store a file
    # The `curl --ftp-create-dirs` functionality is not handled here
    # This example assumes the directory already exists.
    control_socket.send(f"STOR {remote_file_path}\r\n".encode('utf-8'))
    response = control_socket.recv(1024).decode('utf-8')
    print(f"STOR response: {response.strip()}")
    if not response.startswith(('150', '125')):
        print("STOR command failed.")
        return False

    # Open and send the local file
    try:
        with open(local_file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                data_socket.sendall(data)
        print("File sent successfully.")
    except FileNotFoundError:
        print(f"Error: Local file '{local_file_path}' not found.")
        return False
    except Exception as e:
        print(f"An error occurred during file transfer: {e}")
        return False
    finally:
        # Close the data connection
        data_socket.close()

    # Wait for the transfer complete message from the control connection
    response = control_socket.recv(1024).decode('utf-8')
    print(f"Transfer complete response: {response.strip()}")
    if not response.startswith('226'):
        print("File transfer was not successful according to server.")
        return False
        
    # Close the control connection
    control_socket.send("QUIT\r\n".encode('utf-8'))
    response = control_socket.recv(1024).decode('utf-8')
    print(f"QUIT response: {response.strip()}")
    control_socket.close()
    
    return True
    """
    pass

def connect(s: socket, target: str, port: int, username: str, password: bool, command: str="") -> socket:
    # Connect to the server
    print("Sending server request...")
    try:
        s.connect((target, port))
        print=("Connection sucessful!")
         # Check for initial server greeting (220)
        response = s.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Server greeting: {response.strip()}")
        if not response.startswith('220'):
            print("Initial connection failed.")
            return False
        # Authenticate with USER and PASS
        s.send(f"USER {username}\r\n".encode('utf-8'))
        response = s.recv(BUFFER_SIZE).decode('utf-8')
        print(f"USER response: {response.strip()}")
        if not response.startswith('331'):
            print("Username rejected.")
            return False
        if password:
            pw = input("Password: ")
        socket.send(f"PASS {pw}\r\n".encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        print(f"PASS response: {response.strip()}")
        if not response.startswith('230'):
            print("Password rejected.")
            return False
        # Enter Passive Mode (PASV)
        s.send("PASV\r\n".encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        print(f"PASV response: {response.strip()}")
        # Parse PASV response to get data connection details
        # The response will be in the format: "227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)."
        # IP address = h1.h2.h3.h4
        # Port = p1 * 256 + p2
        if not response.startswith('227'):
            print("Failed to enter passive mode.")
            return False
        parts = response.strip().split('(')[1].split(')')[0].split(',')
        data_ip = ".".join(parts[:4])
        data_port = int(parts[4]) * 256 + int(parts[5])
        print(f"Data connection details: {data_ip}:{data_port}")
        print("Connecting to data port...")
        ds = socket(AF_INET, SOCK_STREAM)
        try:
            ds.connect((data_ip, data_port))
        except socket.error as e:
            print(f"Error connecting to data port: {e}")
            return False
        while True:
            action = command
            if action == "":
                action = input("{username}@{target}:{port}> ")
            match action:
                case "upload":
                    pass
                case "download":
                    pass
                case "list":
                    pass
                case "delete":
                    pass
    except:
        return False

def main():
    """
    This is the main function of the script.
    It gets the parsed arguments and performs an action based on them.
    """
    # Get the parsed arguments from the separate function
    args = parse_args()

    # Variables
    target: str = args.ip
    s: socket = socket(AF_INET, SOCK_STREAM)
    username: str = args.username
    password: bool = args.password
        
    # verbose_mode = args.verbose
    if connect(s, target, FTP_PORT, username, password):
        pass
    else:
        print("Connection unsucessful.")
        exit()



if __name__ == "__main__":
    main()