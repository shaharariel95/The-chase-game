import argparse
import socket

"""
Client class
hanldes all the client side of the game.
"""
class Client:
    def __init__(self, server_host, server_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = server_host
        self.server_port = server_port
    
    #hanldes the conenction to the server
    def connect(self):
        try:
            self.client_socket.connect((self.server_host, self.server_port))
        except ConnectionRefusedError:
            print("The Game server refused to connect!")
            exit(1)
        
    #sends a message to the server
    def send_message(self, message):
        self.client_socket.send(message.encode())
        
    #receive a message from the server
    def receive_message(self):
        return self.client_socket.recv(1024).decode().strip()
    
    #check the client for the answer and sends it to the server
    def process_question(self):
        answer = input(f'Your answer (a,b,c,d): ')
        self.send_message(answer)
        return
    
    #check for the client choice for the distance in the start of stage 2
    def process_distance_select(self):
        choice = input('Your choice: ')
        self.send_message(choice)
        return

    #when the game ends, it tell the server its closed and then checks the player if to start a new game, if so start a new connection
    def process_play_again(self):
        self.send_message('shutdown')
        self.client_socket.close()
        choice = input('Enter 1 to play agian\n Enter 2 to exit\n Your choice: ')
        if choice == "1":
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect()
        else:
            print('thank you for playing!')
            exit(0)
    
    #process the message, check if its good or not, check in it what type of message and handles it
    def process_message(self, message):
        if message == b'' or None:
            raise Exception
        print(message)
        if "Question:" in message:
            self.process_question()
        if "You have 3 choices:" in message:
            self.process_distance_select()
        if "Do you want to play again?" in message:
            self.process_play_again()
        

    #start the game
    def play(self):
        self.connect()

        while True:
            message = self.receive_message()
            if 'Server at capacity!' in message:
                print(message)
                self.client_socket.close()
                exit(0)
            try:
                self.process_message(message)
            except Exception as e:
                print(f'\n\nGame Crashed!\n\n {e}')
                self.client_socket.close()
                exit(1)
            except KeyboardInterrupt:
                self.send_message('shutdown')
                self.client_socket.close()
                print('\n\n client shutting down')
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client for game server')
    parser.add_argument('Host', type=str, help='Host address for the server')
    parser.add_argument('Port', type=int, help='Port for the server')
    args = parser.parse_args()
    client = Client(args.Host, args.Port)
    
    client.play()
    