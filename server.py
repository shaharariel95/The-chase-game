import socket
import sys
import threading
import argparse
from player import Player

"""
class server:
initizling the server and handleing the threads, connections, and termination of the game
"""
class Server:
    def __init__(self, Host, Port):
        self.host = Host
        self.port = Port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((Host, Port))
        self.threads = []
        self.semaphore = threading.Semaphore(3)
    
    # start the server and start listening for connections, creating new threads and handling a max of 3 players at once
    def run(self):
        self.server_socket.listen()
        print(f'Server running in IP: {self.host} and Port: {self.port}!')
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                if self.semaphore.acquire(blocking=False):
                    thread = threading.Thread(target=new_client, args=(client_socket, client_address, self.semaphore))
                    print(f'New player connected: {client_address}')
                    self.threads.append(thread)
                    thread.start()
                else:
                    print("Server full, new connection denied!\n")
                    client_socket.send(("Server at capacity! please try again soon!\n").encode())
                    client_socket.close()
        except (KeyboardInterrupt, ConnectionAbortedError, BrokenPipeError):
            self.shutdown()

    #waiting for threads to finish and then closes the server and exits
    def shutdown(self):
        print(f'starting to close the server\n')
        for thread in self.threads:
            thread.join()
        self.server_socket.close()
        print(f'server shutdown completed!\n')
        sys.exit(0)

#handle the new thread and connection and start the game for the player
def new_client(client_socket, client_address, semaphore):
        try:
            player = Player(client_socket, client_address)
            player.start_game()
        except (BrokenPipeError, ConnectionResetError):
            print(f'a client was disconnected {player.client_address}')
        finally:
            player.client_socket.close()
            semaphore.release()
    

#add agrs and uses them to start the server with the chosen ip and port
if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Game Server Started!")
    args.add_argument("Host", type=str, help="The Host IP address for the server.")
    args.add_argument("Port", type=int, help="The Port number to bind the server to.")
    args = args.parse_args()
    server = Server(args.Host, args.Port)
    server.run()
