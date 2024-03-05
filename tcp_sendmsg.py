import socket
"""
This module will send the tcp command as required
to the constant IP: '10.16.0.23'
                PORT:10003
"""

def send_message_and_receive_response(message):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        s.connect(('10.16.0.23', 10003))
        # Send the message
        s.sendall(message.encode()+b'\r\n')     #this way to communicate msg -> robot
        # Receive the response
        response = s.recv(1024).decode()
        return response

    except Exception as e:
        print("An error occurred:", e)
        return None


