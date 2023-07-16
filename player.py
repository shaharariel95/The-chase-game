from game import Game
from color_text import ColorText

"""
handles the client,
sending messages
receiving messages
their position and money, as well as the chaser postion
"""
class Player:
    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address
        self.bank = 0
        self.dis = -1
        self.chaser = 0
        self.questions = []
        self.game = Game(self)
    
    #send message to the client
    def send_message(self, message):
        self.client_socket.send(message.encode())

    #receive message from the client and check for validity
    def receive_message(self):
        message = self.client_socket.recv(1024).decode().strip()
        if message and message != '':
            return message
        return None

    #start the game for the client, and moves it to the correct stage of the game
    def start_game(self):
        print(f'Player {self.client_address} has started playing\n')
        self.first_phase()
        if self.bank == 0:
            self.send_message(f'you have {ColorText.colorize("0$", "red")} Do you want to play again?\n')
            message = self.receive_message()
            if 'shutdown' in message:
                raise BrokenPipeError
        self.second_phase()

        self.third_phase()
    
    #hanldes the first stage of the games
    def first_phase(self):
        self.send_message(f'\t\t{ColorText.colorize("Welcome", "blue")} {ColorText.colorize("to", "magenta")} {ColorText.colorize("the", "cyan")} {ColorText.colorize("to", "green")} {ColorText.colorize("Chaser!!", "red")}\n')

        for i in range(3):
            self.game.send_question(self)
            message = self.receive_message()
            if 'shutdown' in message:
                raise BrokenPipeError
            self.game.process_phase_one_answer(message, self)

        self.send_message(f'You have {ColorText.colorize(str(self.bank)+ "$", "yellow")} in the bank! beat stage two to win it!\n')
    
    #hanldes the second stage of the game
    def second_phase(self):
        while True:
            self.send_message(f'You have a distance of 3 from the bank\n')
            self.send_message(f'You have 3 choices:\n')
            self.send_message(f'{ColorText.colorize("1) move one step closer to the chaser -> double the money in the bank", "red")}\n')
            self.send_message(f'{ColorText.colorize("2) stay at your distance from the chaser and play for the amount you have in the bank", "yellow")}\n')
            self.send_message(f'{ColorText.colorize("3) move one step closer to the bank -> play for half the money in the bank", "green")}\n')

            message = self.receive_message()

            if message == "1":
                self.dis = 2
                self.bank *= 2
                break
            elif message == "2":
                self.dis = 3
                break
            elif message == "3":
                self.dis = 4
                self.bank //= 2
                break
            self.send_message(f'Invalid input, please try again\n')

        while self.dis < 7 and self.dis > 0:
            self.game.send_board(self)
            self.send_message(f"\n")
            self.game.send_question(self)
            message = self.receive_message()
            if 'shutdown' in message:
                raise BrokenPipeError
            self.game.process_phase_two_answer(self, message)
            if self.dis == 7:
                self.send_message(f'{ColorText.colorize("you have reached the bank!!", "green")}\n')
                self.send_message(f'You earned {ColorText.colorize(str(self.bank), "yellow")}$!\n')
                return
            if self.dis == self.chaser:
                self.send_message(f'{ColorText.colorize("the Chaser has caught you!", "red")}\n')
                return
            
    #handles end game.
    def third_phase(self):
        self.send_message(f'Do you want to play again?\n')


                   



        
