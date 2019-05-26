from time import time

scale = .01
damage_scale = 5
base = 100

class AgentResult:
    def __init__(self):
        # self.last_time = time()
        # self.mission_time = 0
        self.distance = 0
        self.damage_dealt = 0
        self.kill_count = 0
        self.life = 20

    def AppendDistance(self,distance):
        self.distance = distance

    def GetFitness(self):
        if self.life == 0:
            fitness = -1000
        elif self.kill_count == 1:
            fitness = 10000
        else:
            fitness = (self.damage_dealt * damage_scale) - (self.distance * scale) - base

        print("Agent fitness: " + str(fitness))
        print("\n")
        return fitness

    def SetDamageInflicted(self, damage):
        self.inflicted_damage = damage

    def SetMissionTime(self, time):
        self.mission_time = time

    def SetDamageTaken(self, damage):
        self.damage_taken = damage




