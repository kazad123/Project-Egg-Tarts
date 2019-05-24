import MalmoPython
import uuid
import sys
import time
import random
import json
import pickle
import os
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from Fighter import Fighter
import neat


def get_mission_XML():
    mission_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    
      <About>
        <Summary>Fighting 1v1</Summary>
      </About>
    
      <ServerSection>
        <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>true</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
        </ServerInitialConditions>
        <ServerHandlers>
          <FlatWorldGenerator generatorString="3;7,3*10;1;"/>
          <DrawingDecorator>
    
                <DrawLine type="diamond_block" y1="10" y2="10" x1="0" x2="11" z1="0" z2="0" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="0" x2="0" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="1" x2="1" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="2" x2="2" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="3" x2="3" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="4" x2="4" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="5" x2="5" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="6" x2="6" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="7" x2="7" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="8" x2="8" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="9" x2="9" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="10" x2="10" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="11" x2="11" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="11" x2="0" z1="11" z2="11" />
    
          </DrawingDecorator>
    
          <ServerQuitFromTimeUp description="" timeLimitMs="10000"/>
          <ServerQuitWhenAnyAgentFinishes/>
        </ServerHandlers>
      </ServerSection>
    
      <AgentSection mode="Adventure">
        <Name>Fighter1</Name>
        <AgentStart>
            <Placement pitch="0" x="3" y="11" yaw="0" z="3"/>
            <Inventory>
                <InventoryItem slot="0" type="stick" quantity="1" />
            </Inventory>
    
        </AgentStart>
        <AgentHandlers>
        <ObservationFromFullStats/>
        <ContinuousMovementCommands turnSpeedDegs="360"/>
          <ObservationFromNearbyEntities>
            <Range name="entities" xrange="10" yrange="1" zrange="10"/>
          </ObservationFromNearbyEntities>
          <ObservationFromGrid>
            <Grid name="floor">
                <min x="-1" y="0" z="-1"/>
                <max x="1" y="0" z="1"/> </Grid>
          </ObservationFromGrid>
          <RewardForTouchingBlockType>
            <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
            </RewardForTouchingBlockType>
        </AgentHandlers>
      </AgentSection>
      
        <AgentSection mode="Adventure">
    <Name>Fighter2</Name>
    <AgentStart>
        <Inventory>
                <InventoryItem slot="0" type="stick" quantity="1" />
        </Inventory>
        <Placement pitch="0" x="11" y="11" yaw="0" z="11"/>
    </AgentStart>
    <AgentHandlers>
    <ObservationFromFullStats/>
    <ContinuousMovementCommands turnSpeedDegs="360"/>
      <ObservationFromNearbyEntities>
        <Range name="entities" xrange="10" yrange="1" zrange="10"/>
      </ObservationFromNearbyEntities>
      <ObservationFromGrid>
        <Grid name="floor">
            <min x="-1" y="0" z="-1"/>
            <max x="1" y="0" z="1"/> </Grid>
      </ObservationFromGrid>
    </AgentHandlers>
  </AgentSection>
  
        
    </Mission> '''

    return mission_xml


def get_mission():
    mission_xml = get_mission_XML()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    return my_mission


class World:
    def __init__(self, client_pool): 
        self.client_pool = client_pool
        self.best_genome = None
        self.mission = get_mission()

    def train(self, population):
        i = 0
        while True:
            i += 1
            self.best_genome = population.run(self.evaluate_genome, 1)
            with open('gen-{}-winner'.format(i), 'wb') as f:
                print("Dumping best genome.....")
                pickle.dump(self.best_genome, f)

            return self.best_genome

    def start_fight(self,genome1, genome2, config):
        agents, agents_fighter = self.setup_fighters([genome1, genome2], config)
        return self.run_fighters(*agents_fighter)

    def setup_fighters(self, genomes, config):
        if len(genomes) != 2:
            raise Exception("Size of argument genomes is not 2")

        agents = [MalmoPython.AgentHost() for i in range(len(genomes))]
        self.start_mission(agents)
        agents_fighter = []
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
                # print("printing the genomes")
                # print (genome)
                del agents
                del agents_fighter

    def run_fighters(self, fighter1, fighter2):
        print("Running.....\n")
        while fighter1.isRunning() or fighter2.isRunning():
            fighter1.run()
            fighter2.runNothing()
            time.sleep(1)

            for error in fighter1.agent.peekWorldState().errors:
                print ("Fighter 1 Error:",error.text)
            for error in fighter2.agent.peekWorldState().errors:
                print ("Fighter 2 Error:",error.text)

        if fighter1.data is not None:
            print("Fighter 1 data: ")
            print(fighter1.data)
            print("Damage taken: " + str(fighter1.data.get(u'DamageTaken')))
            print("Past dmg: " + str(fighter1.fighter_result.damage_taken))

        if fighter2.data is not None:
            fighter2_life = fighter2.data.get(u'life')
            if fighter2_life == 0:
                fighter1.fighter_result.killed_fighter = True
                print("Fighter 2 was slain!!!!")


        fighter1.fighter_result.isAlive = fighter1.data.get(u'IsAlive')
        fighter1.fighter_result.life = fighter1.data.get(u'Life')
        fighter1_damage_taken = fighter1.data.get(u'DamageTaken')
        fighter1_mission_time = fighter1.data.get(u'TotalTime')
        fighter1.fighter_result.SetMissionTime(fighter1_mission_time)
        fighter1.fighter_result.SetDamageTaken(fighter1_damage_taken)
        fighter1_fitness = fighter1.fighter_result.GetFitness()

        return fighter1_fitness

    def start_mission(self, agent_hosts):
        expId = str(uuid.uuid4())
        for i in range(len(agent_hosts)):
            while True:
                try:
                    print("trying to start agent {}".format(i))
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


