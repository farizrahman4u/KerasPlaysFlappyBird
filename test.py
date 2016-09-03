from model import model
from qlearning4k import Agent
from flappy_bird import FlappyBird

game = FlappyBird()
model.load_weights('weights.dat')
agent = Agent(model)
agent.play(game, nb_epoch=1)
