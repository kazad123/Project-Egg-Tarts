#!/usr/bin/python

import MalmoPython
import random
#, GetMission
import os
import sys
# from . import World
sys.path.insert(0, '../neat-python')
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from World import World
import neat
import pickle


def SetupClientPools(num_agents):
    client_pool = MalmoPython.ClientPool()
    for i in range(num_agents):
        client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000+i))
    return client_pool


def InitalizeNeatConfig():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-fighter')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path) 
    return config


def InitalizeNEATPopulation():
    config = InitalizeNeatConfig()
    pop = neat.Population(config)
    return pop, config

if __name__ == "__main__":
    num_agents = 2
    world = World(SetupClientPools(num_agents))

    if len(sys.argv) == 2:
        population, config = neat.Checkpointer.restore_checkpoint(str(sys.argv[1])), InitalizeNeatConfig()
    else:
        population, config = InitalizeNEATPopulation()

    population.add_reporter(neat.StdOutReporter(True))
    # population.add_reporter(neat.Checkpointer(100, 1500))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    check_pointer = neat.Checkpointer(generation_interval=1, filename_prefix='generation-checkpoint-')
    population.add_reporter(check_pointer)
    winner = world.train(population, config)


    # except KeyboardInterrupt:
    #     winner = population.best_genome

    # if (check_pointer.last_generation_checkpoint >= 0) and (check_pointer.last_generation_checkpoint < 100):
    #     filename = 'neat-checkpoint-{0}'.format(check_pointer.last_generation_checkpoint)
    #     print("Restoring from {!s}".format(filename))
    #     population2 = neat.checkpoint.Checkpointer.restore_checkpoint(filename)
    #     population2.add_reporter(neat.StdOutReporter(True))
    #     stats2 = neat.StatisticsReporter()
    #     population2.add_reporter(stats2)
    #
    #     try:
    #         winner2 = world.train(population2, config)
    #     except KeyboardInterrupt:
    #         winner = population.best_genome










