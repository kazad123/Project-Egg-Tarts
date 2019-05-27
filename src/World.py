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
import statistics


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
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
        </ServerInitialConditions>
        <ServerHandlers>
          <FlatWorldGenerator generatorString="3;7,3*10;1;"/>
          <DrawingDecorator>
                <DrawLine type="diamond_block" y1="10" y2="10" x1="4" x2="4" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="5" x2="5" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="6" x2="6" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="7" x2="7" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="8" x2="8" z1="0" z2="11" />
                <DrawLine type="diamond_block" y1="10" y2="10" x1="9" x2="9" z1="0" z2="11" />
          </DrawingDecorator>
    
          <ServerQuitFromTimeUp description="" timeLimitMs="10000"/>
          <ServerQuitWhenAnyAgentFinishes/>
        </ServerHandlers>
      </ServerSection>
    
      <AgentSection mode="Survival">
        <Name>Fighter1</Name>
        <AgentStart>
            <Placement pitch="0" x="6" y="11" yaw="0" z="6"/>
            <Inventory>
                <InventoryItem slot="0" type="wooden_sword" quantity="1" />
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
      
        <AgentSection mode="Survival">
    <Name>Fighter2</Name>
    <AgentStart>
        <Inventory>
                <InventoryItem slot="0" type="wooden_sword" quantity="1" />
        </Inventory>
        <Placement pitch="0" x="8" y="11" yaw="0" z="8"/>
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
        self.damage_list = []
        self.distance_list = []
        self.agents_killed = 0

    def train(self, population):
        i = 0
        while True:
            i += 1
            self.best_genome = population.run(self.evaluate_genome, 1)
            with open('gen-{}-winner'.format(i), 'wb') as f:
                pickle.dump(self.best_genome, f)
            return self.best_genome

    def start_fight(self, genome1, genome2, config):
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
            print("Running genome {}".format(genome_id))
            agents, agents_fighter = self.setup_fighters([genome, self.best_genome], config)
            genome.fitness = self.run_fighters(*agents_fighter)
            del agents
            del agents_fighter

    def run_fighters(self, fighter1, fighter2):
        count = 0

        while fighter1.is_running() or fighter2.is_running():
            print("Action " + str(count))
            count += 1
            # 2nd agent does nothing
            fighter1.run()
            fighter2.run_nothing()
            # Runs for 10 seconds, every second send command
            time.sleep(1)

            for error in fighter1.agent.peekWorldState().errors:
                print("Fighter 1 Error: ", error.text)
            for error in fighter2.agent.peekWorldState().errors:
                print("Fighter 2 Error:", error.text)

        if fighter1.data is not None:
            print("Fighter 1 data: " + str(fighter1.data) + "\n")

            # Calculate damage dealt, distance traveled
            self.damage_list.append(fighter1.data.get(u'DamageDealt'))
            self.distance_list.append(fighter1.data.get(u'DistanceTravelled'))

            if len(self.damage_list) > 1:
                damage_dealt = self.damage_list[-1] - self.damage_list[-2]
                distance_travelled = self.distance_list[-1] - self.distance_list[-2]
                fighter1.fighter_result.damage_dealt = damage_dealt
                fighter1.fighter_result.dist_travelled = distance_travelled
            else:
                # Set to 0 at first because world will save previous missions result (if mission is not closed)
                fighter1.data[u'DamageDealt'] = 0
                fighter1.fighter_result.damage_dealt = fighter1.data.get(u'DamageDealt')
                fighter1.fighter_result.distance = 0

            # Grab players killed
            if self.agents_killed != fighter1.data.get(u'PlayersKilled'):
                fighter1.fighter_result.kill_count = 1
                self.agents_killed = fighter1.data.get(u'PlayersKilled')
            else:
                fighter1.fighter_result.kill_count = 0

            fighter1.fighter_result.life = fighter1.data.get(u'Life')
            # Average angle to other agent
            fighter1.fighter_result.angle = statistics.mean(fighter1.angle_list)
            print("Fighter 1 damage dealt: " + str(fighter1.fighter_result.damage_dealt))
            print("Fighter 1 average angle: " + str(fighter1.fighter_result.angle))
            print("Fighter 1 distance travelled: " + str(fighter1.fighter_result.dist_travelled) + '\n')

        # if fighter2.data is not None:
        #     print("Fighter 2 data: ")
        #     print(fighter2.data)
        #     print("")

        # Only use fighter 1 fitness
        fighter1_fitness = fighter1.fighter_result.get_fitness()

        return fighter1_fitness

    def start_mission(self, agent_hosts):
        expId = str(uuid.uuid4())
        for i in range(len(agent_hosts)):
            while True:
                try:
                    print("trying to start agent {}".format(i))
                    agent_hosts[i].startMission(self.mission, self.client_pool,
                                                MalmoPython.MissionRecordSpec(), i, expId)
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
                    hasBegun += 1
                if len(world_state.errors):
                    hadErrors = True
                    print("Errors from agent")
                    for error in world_state.errors:
                        print("Error:", error.text)
        if hadErrors:
            print("not ABORTING ERROR DETECTED")


