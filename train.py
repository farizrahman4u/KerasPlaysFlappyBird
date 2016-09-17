from model import model
from qlearning4k import Agent
from flappy_bird import FlappyBird

game = FlappyBird(frame_rate=10000, sounds=False)
agent = Agent(model, memory_size=100000)
agent.train(game, epsilon=[0.01, 0.00001], epsilon_rate=0.3, gamma=0.99, nb_epoch=1000000, batch_size=32, checkpoint=250)
