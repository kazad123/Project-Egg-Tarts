dist_scale = .01
travel_scale = .0025
angle_scale = .1
damage_scale = 10
base = 0


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

        if self.life == 0:
            fitness = -1000
        elif self.kill_count == 1:
            print("Killed other agent! ")
            fitness = 10000
        else:
            fitness = (self.damage_dealt * damage_scale) - (self.ent_distance * dist_scale) - \
                      (self.angle * angle_scale) + (travel_scale * self.dist_travelled) - base

        print("Agent fitness: " + str(fitness))
        print("\n")
        return fitness



