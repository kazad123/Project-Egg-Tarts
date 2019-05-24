from time import time

INFLICTED_DAMAGE_SCALE = 2
# DAMAGE_TAKEN_SCALE = INFLICTED_DAMAGE_SCALE * 0.90
TIME_SCALE = 0.01
DISTANCE_SCALE = 0.01


class AgentResult:
    def __init__(self):
        self.last_time = time()
        self.distance_area = 0.0
        self.inflicted_damage = 0
        self.damage_taken = 0
        self.mission_time = 0

        self.isAlive = True
        self.life = 20
        self.killed_fighter = False

    def AppendDistance(self,distance):
        cur_time = time()
        time_dif = cur_time - self.last_time
        self.distance_area += time_dif * distance
        self.last_time = cur_time

    def GetFitness(self):
        if self.life == 0:
            fitness = -10000
        else:
            fitness = self.inflicted_damage * INFLICTED_DAMAGE_SCALE - (self.mission_time * TIME_SCALE) - (DISTANCE_SCALE * self.distance_area)

        print("Agent fitness: " + str(fitness))
        print("\n")
        return fitness

    def SetDamageInflicted(self, damage):
        self.inflicted_damage = damage

    def SetMissionTime(self, time):
        self.mission_time = time
        
    def SetDamageTaken(self, damage):
        self.damage_taken = damage




