# snake_AI
A snake game to play and a machine learning application for the game using NEAT.

"Snake_to_Play.py" is for playing the game. "Snake_AI.py" is the machine learning application using NEAT.
Before running, you should install "pygame" and "python-neat". Also do not forget to include "configuration.txt" file in the project directory.

In each generation, the game starts with 150 snakes and their foods. Although 150 snakes are running at the same time, only the snake with the best fitness is shown on the screen. Therefore, the screen may change as the fitness of another genome gets better than the existing one.

The algorithm fits; closest distance to an obstacle (snake's body) in each direction (up, down, right, left), the distance to food in each direction (up, down, right, left) and the current direction to the next decision. Any improvement advice is very welcome.
