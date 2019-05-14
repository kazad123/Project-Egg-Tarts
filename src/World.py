import MalmoPython
import uuid
import sys
import time
import random
import json
import pickle
sys.path.insert(0, '../../')
from Neat_Fighter.src.Fighter import Fighter
sys.path.insert(0, '../neat-python')
import neat


def get_mission_XML():
    mission_xml =

    return mission_xml

def get_mission():
    mission_xml = get_mission_XML()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    return my_mission

class World:
    def __init__(self, client_pool): 
        self.client_pool = client_pool
        self.best_genome = None

    def train(self, population):
        i = 0
        while True:
            i += 1
            self.best_genome = population.run(self.evaluate_genome, 1)
            with open('gen-{}-winner'.format(i), 'wb') as f:
                pickle.dump(self.best_genome, f)
            return self.best_genome


    def start_fight(self,genome1, genome2, config):
        agents, agents_fighter = self.setup_fighters([genome1, genome2], config)
        return self.run_fighters(*agents_fighter)


    def setup_fighters(self, genomes, config):
        if len(genomes) != 2:
            raise Exception("Size of argument genomes is not 2")
        agents = [MalmoPython.AgentHost() for i in range(2)]
        self.start_mission(agents)
        agents_fighter = []
        print("setup fighters")
        for i in range(2):
            agents_fighter.append(Fighter(agents[i], None if genomes[i] == None else
                                  neat.nn.FeedForwardNetwork.create(genomes[i], config)))
        return agents, agents_fighter

    def evaluate_genome(self, genomes, config):
        for genome_id, genome in genomes:
            # if (DEBUGGING):
                print ("Running genome {}".format(genome_id))
                agents, agents_fighter = self.setup_fighters([genome, self.best_genome], config)
                genome.fitness = self.run_fighters(*agents_fighter)
                # if DEBUGGING:
                print("printing the genomes")
                print (genome)
                del agents
                del agents_fighter

    def run_fighters(self, fighter1, fighter2):
        while fighter1.isRunning() or fighter2.isRunning():
            fighter1.run()
            fighter2.run()
            time.sleep(0.2)
            for error in fighter1.agent.peekWorldState().errors:
                print ("Fighter 1 Error:",error.text)
            for error in fighter2.agent.peekWorldState().errors:
                print ("Fighter 2 Error:",error.text)

        fighter1_damage_inflicted = fighter2.data.get(u'DamageTaken')
        fighter1_damage_taken = fighter1.data.get(u'DamageTaken')
        fighter1_mission_time = fighter1.data.get(u'TotalTime')
        fighter1.fighter_result.SetDamageInflicted(fighter1_damage_inflicted)
        fighter1.fighter_result.SetMissionTime(fighter1_mission_time)
        fighter1.fighter_result.SetDamageTaken(fighter1_damage_taken)
        fighter1_fitness = fighter1.fighter_result.GetFitness()

        return fighter1_fitness


    def start_mission(self, agent_hosts):
        self.mission = get_mission()
        expId = str(uuid.uuid4())
        for i in range(len(agent_hosts)):
            while True:
                try:
                    print("trying to start agent {}".format(i))
                    # print(self.client_pool)
                    # print(agent_hosts)
                    agent_hosts[i].startMission(self.mission, self.client_pool, MalmoPython.MissionRecordSpec(), i, expId )
                    break
                except Exception as e:
                    # print ("Failed to start mission for agent {}: retrying again in 1 seconds".format(i))
                    print(str(e))
                    time.sleep(1)

        hasBegun = 0
        hadErrors = False
        while hasBegun < len(agent_hosts) and not hadErrors:
            time.sleep(0.1)
            for ah in agent_hosts:
                world_state = ah.peekWorldState()
                if world_state.has_mission_begun:
                    hasBegun+= 1
                if len(world_state.errors):
                    hadErrors = True
                    print ("Errors from agent")
                    for error in world_state.errors:
                        print ("Error:",error.text)
        if hadErrors:
            print ("not ABORTING ERROR DETECTED")


