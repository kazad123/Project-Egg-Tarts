dist_scale = 1
travel_scale = .001
angle_scale = .01
damage_scale = 10
base = 100


class AgentResult:
    def __init__(self):
        self.ent_distance = 0
        self.dist_travelled = 0
        self.damage_dealt = 0
        self.kill_count = 0
        self.life = 20
        self.angle = 0

    def get_fitness(self):
        # Normalize angle
        if self.angle > 180:
            self.angle = 360 - self.angle
        # Angle scaling, larger penalty for doing badly, reward for facing other anet
        if self.angle < 15:
            self.angle = 0
        else:
            self.angle = self.angle ** 2
        # Scale distance away from entity?
        # self.ent_distance = self.ent_distance ** 2
        # Calculate fitness
        fitness = (self.damage_dealt * damage_scale) - (self.ent_distance * dist_scale) - \
                  (self.angle * angle_scale) + (self.dist_travelled * travel_scale) - base
        # Add reward for winning/losing
        if self.life == 0:
            fitness -= 1000
        if self.kill_count == 1:
            print("Killed other agent! ")
            fitness += 10000

        print("Agent fitness: " + str(fitness))
        print("\n")
        return fitness
