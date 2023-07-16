from tabulate import tabulate
from questions import questions
from color_text import ColorText
import random

"""
class game
manages the state of a game for a client,
the amount of money,
chaser and player position and the question pool
"""
class Game:
    def __init__(self, player):
        self.player = player
        self.chaser_success_rate = 0.75
        self.questions = questions.copy()
        self.current_question = 0
        self.current_answer = "e"
        self.board=[['','Chaser'],
                    [1, ''],
                    [2,'' ],
                    [3,'' ],
                    [4,'' ],
                    [5, ''],
                    [6,'' ],
                    [7, 'Bank']]
    
    #sends a question from the question pool and removes it to make sure not to sends the same questions twice
    def send_question(self, player):
        question = random.choice(self.questions)
        self.questions.remove(question)
        self.current_question = question
        self.current_answer = question['correct_option']
        options = question['options']
        full_question = question['question'] + "\n"
        for choice, answer in options.items():
            full_question += f"{choice}. {answer}\n"
        player.send_message(full_question)

    #processes the stage 1 answers from the client,
    #add money to the bank if the message is correct
    def process_phase_one_answer(self, message, player):
        answer = message.strip()
        if answer == self.current_answer:
            player.bank += 5000
            player.send_message(f'{ColorText.colorize("Correct answer!", "green")}\n')
        else:
            player.send_message(f'{ColorText.colorize("Wrong answer!", "red")}\n')
    
    #processes the stage 2 answers form the client
    #moves the player a step if they are corect, moves the chaser if he is correct
    def process_phase_two_answer(self, player, message):
        answer = message
        if answer == self.current_answer:
            player.dis += 1
            player.send_message(f'{ColorText.colorize("Correct answer!!", "green")} you moved one step closer to the bank!\n')
        else:
            player.send_message(f'{ColorText.colorize("wrong answer!!", "red")} you have stayed in place\n')
        if self.chaser_success_rate > random.random(): #checks for a 75% success
            player.chaser += 1
            player.send_message(f'{ColorText.colorize("the chaser was correct!", "red")} he moved one step closer to you!\n')
        else: 
            player.send_message(f'{ColorText.colorize("the chaser was Wrong!", "yellow")} he stayed in place!\n')

    #moves the player a step closer to the bank 
    def mv_player(self,player):
        self.board[player.dis-1][1]=''
        self.board[player.dis][1]= f'{ColorText.colorize(str(player.bank), "yellow")}'

    #moves the chaser a step closer to the bank
    def mv_chaser(self,player):
        self.board[player.chaser-1][1]=''
        self.board[player.chaser][1]=f'{ColorText.colorize("chaser", "red")}'

    #sends the board to the player
    def send_board(self,player):
        self.mv_player(player)
        self.mv_chaser(player)
        self.board[7][1] = f'{ColorText.colorize("Bank", "blue")}'
        player.send_message(tabulate(self.board, tablefmt="jira"))