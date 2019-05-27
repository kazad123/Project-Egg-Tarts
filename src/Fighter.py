import MalmoPython
import random
import time
import sys
import os
sys.path.insert(0, '../../')
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import json
from threading import Timer
import math
from AgentResult import AgentResult

'''
Fighter will holds all the definition of what our agents can do
'''

#DEBUGGING = World.DEBUGGING #i think there's a better way to do this with env vars or cmd line args or something but *shrug*


def angle(a1,a2,b1,b2):
    rt = math.atan2(b2-a2, b1-a1)
    return rt if rt >= 0 else rt + 2*math.pi


def angle_between_agents(a1,a2,yaw1,b1,b2):
    angl = angle(a1,a2,b1,b2)
    relative_angle = angl - yaw1
    rad = (2 * math.pi) - ((relative_angle + math.pi)%(2*math.pi))

    return (2 * math.pi) - ((relative_angle + math.pi)%(2*math.pi))


def scale_state_inputs(state_inputs):
    a, d = state_inputs
    return [scale_angle(a), scale_distance(d)]


def scale_distance(distance):
    return distance/9


def scale_angle(theta):
    return (theta/math.pi)


class Fighter:
    def __init__(self, agent_file, neural):
        self.neural = neural
        self.agent = agent_file
        self.fighter_result = AgentResult()
        self.mission_ended = False
        self.world_state = None
        self.data = None
        self.angle_list = []

    def is_running(self):
        return not self.mission_ended and self.agent.peekWorldState().is_mission_running

    def run_nothing(self):
        while self.agent.peekWorldState().number_of_observations_since_last_state == 0:
            if not self.is_running():
                print("agent not running")
                return

        if self.mission_ended or not self.agent.peekWorldState().is_mission_running:
            return

        self.world_state = self.agent.getWorldState()
        self.data = json.loads(self.world_state.observations[-1].text)
        return

    def run(self):
        while self.agent.peekWorldState().number_of_observations_since_last_state == 0:
            if not self.is_running():
                return
            time.sleep(0.1)

        self.world_state = self.agent.getWorldState()
        self.data = json.loads(self.world_state.observations[-1].text)

        # Random input
        # rnd = random.random()
        # actions = ["jump 1", "wait 1", "move 1", "turn 1"]
        # a = random.randint(0, len(actions) - 1)
        #
        # print(actions[a])
        # self.agent.sendCommand(actions[a])

        if self.neural is None:
            return

        agent_state_input = self._get_agent_state_input()
        scaled_state_input = scale_state_inputs(agent_state_input)
        output = self.neural.activate(scaled_state_input)
        # print("angle {:.2f}; dist {:.2f};   move {:.3f}; strafe {:.3f}; turn {:.3f}; attack {:.3f}".format(*(agent_state_input + output)))

        if self.mission_ended or not self.agent.peekWorldState().is_mission_running:
            return

        print("move: {}".format(output[0]))
        print("strafe: {}".format(output[1]))
        print("turn: {}".format(output[2]))
        print("attack: 1\n")

        self.agent.sendCommand("move {}".format(output[0]))
        self.agent.sendCommand("strafe {}".format(output[1]))
        self.agent.sendCommand("turn {}".format(output[2]))
        # self.agent.sendCommand("attack {}".format(0 if output[3] <= 0 else 1))
        # Always attack
        self.agent.sendCommand("attack 1")

    def _get_agent_state_input(self):
        to_return = []
        entities = self.data.get(u'entities')
        #
        # if self.data.get(u'PlayersKilled') == 1:
        #     self.mission_ended = True

        agent_x, agent_z, agent_yaw = entities[0][u'x'], entities[0][u'z'], math.radians((entities[0][u'yaw'] - 90) % 360)

        if len(entities) > 1:
            other_entities = entities[1:]
            other_entities = [(ent, math.hypot(entities[0][u'x'] - ent[u'x'], entities[0][u'z'] - ent[u'z']))
                              for ent in other_entities]
            other_entities = sorted(other_entities, key=lambda x: x[1])[0]

            closest_ent_x, closest_ent_z, closest_ent_dist = other_entities[0][u'x'], other_entities[0][u'z'], \
                                                             other_entities[1]
            self.fighter_result.ent_distance = closest_ent_dist
            rad = angle_between_agents(agent_x, agent_z, agent_yaw, closest_ent_x, closest_ent_z)

            degrees = rad*(180/math.pi)
            self.angle_list.append(degrees)
            # print("Angle: " + str(degrees))
            to_return.extend([angle_between_agents(agent_x, agent_z, agent_yaw, closest_ent_x, closest_ent_z),
                              closest_ent_dist])
        else:
            to_return.extend([0, 0])

        return to_return
