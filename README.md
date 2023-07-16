# The Chase Game

This repository contains the code for a game inspired by the TV gameshow 'The Chase'. The game is implemented in Python and uses TCP for client-server communication and threading. 

## Files

The project consists of the following files:

### server.py

The `server.py` file manages the main thread of the server. It initializes new threads for each connection, acknowledges up to three connections, and starts the game for each connection.

- **RUN function:** Initializes the server and starts listening for connections. When a connection is established, it activates a new thread and records a video of up to three players.

- **SHUTDOWN function:** Waits for all threads to finish and safely closes the server.

- **new_client function:** Initializes a new game for the client, starts the game run, and checks for any errors during the run. At the end of the game, it releases the thread.

### player.py

The `player.py` file contains information about the player, such as the client connection, the amount of money in the bank, and the locations of the player and the chaser. It manages the sending of messages to the client and receiving answers.

- **send and receive functions:** These functions send and receive messages to and from the client.

- **start_game function:** Manages the stages of the game.

- **phase_one function:** Manages the first stage by asking three questions and allocating money for each correct answer.

- **phase_two function:** Manages the second stage by checking the player's starting point, asking questions to manage the chase, and checking end conditions such as reaching the bank or catching the chaser.

- **third_phase function:** Sends a message to the client alerting the start of a new game after it ends.

### game.py

The `game.py` file contains information about the game, such as the game taker for the second part, the questions assigned to the client, and the success percentage of the chaser in answering questions. It manages the analysis of the client's answers, the granting of money, and progress in the game.

- **send_question function:** Allocates a question from the player's repository, sends it to the client, saves its answer, and removes it from the repository to prevent repetition for the same player.

- **process_phase_one_answer function:** Receives and analyzes the player's answer in the first stage, allocating money if the answer is correct.

- **process_phase_two_answer function:** Receives and analyzes the player's answer in the second stage, promotes the player a step if they answered correctly, and checks if the chaser answered correctly, promoting them if so.

- **mv_player and mv_chaser functions:** Promote the player and the chaser a step if they answered correctly.

- **send_board function:** Sends the client the game board in the second stage.

### questions.py

The `questions.py` file contains the questions, which are copied to each player.

### color_text.py

The `color_text.py` file contains a function for text coloring, enhancing the game management at the client.

### client.py

The `client.py` file manages the course of the game at the client side. It prints and receives the client's input and connects to the server to start the game.

- **connect function:** Connects to the game server.

- **send and receive message functions:** These functions send and receive messages to and from the server.

- **process_question function:** Receives the user's answer to the question asked by the server and returns it.

- **process_distance_select function:** Receives from the client at which distance they want to start the second stage of the game.

- **process_play_again function:** Asks the user if they want to play again after the game ends.

- **process_message function:** Analyzes and sends the code to the appropriate location based on the message received from the server.

- **PLAY function:** Manages the client's game process.

## How to Play

The game has two stages:

1. **First stage**: The player is asked 3 questions. For each correct answer, a reward is added to the bank.

2. **Second stage (The Chase)**: For each correct answer, the player moves closer to the bank. However, the chaser also answers questions, and if correct, moves closer to the player. The game ends if the player reaches the bank and wins the money or if the chaser reaches the player, in which case the player wins nothing.
3. please remember this is only a small project to test TCP on python so not alot of questions and not hard ones either, have fun!

## Running the Game

You need to use command line arguments to enter the server IP and port, both for the server and the client.

For example, to run the server:

```bash
python server.py 127.0.0.1 5000
```

```bash
python client.py 127.0.0.1 5000
```
Please replace 127.0.0.1 and 5000 with your server's IP and port.
