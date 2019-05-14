from time import time

INFLICTED_DAMAGE_SCALE = 2#40
DAMAGE_TAKEN_SCALE = INFLICTED_DAMAGE_SCALE * 0.90
TIME_SCALE = 0.01#1
DISTANCE_SCALE = 0.01#100

class AgentResult:
    def __init__(self):
        self.last_time = time()
        self.distance_area = 0.0
        self.inflicted_damage = 0
        self.damage_taken = 0
        self.mission_time = 0

    def AppendDistance(self,distance):
        cur_time = time()
        time_dif = cur_time - self.last_time
        self.distance_area += time_dif * distance
        self.last_time = cur_time

    def GetFitness(self):
        return self.inflicted_damage * INFLICTED_DAMAGE_SCALE - (self.mission_time * TIME_SCALE) - (DISTANCE_SCALE * self.distance_area) - (DAMAGE_TAKEN_SCALE * self.damage_taken)

    def SetDamageInflicted(self, damage):
        self.inflicted_damage = damage

    def SetMissionTime(self, time):
        self.mission_time = time
        
    def SetDamageTaken(self, damage):
        self.damage_taken = damage




