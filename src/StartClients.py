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
    population.add_reporter(neat.Checkpointer(100, 300))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    try:
        winner = world.train(population)
    except KeyboardInterrupt:
        winner = population.best_genome










