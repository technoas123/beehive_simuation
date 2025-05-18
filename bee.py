import random

class Bee:
    def __init__(self, bee_id, bee_type):
        self.id = bee_id
        self.type = bee_type
        self.position = (0, 0)
        self.state = "idle"
        self.direction = (0, 0)
        self.has_nectar = False
        self.age = 0
        self.deposit_count = 0
        self.warmup_time = random.randint(3, 6)        
        self.search_timer = 0                          
        self.search_patience = random.randint(2, 5)    
        self.energy = random.randint(3, 6)
        self.rest_timer = 0
        self.rest_duration = random.randint(2,4)
        self.death_reason = None

    def get_random_direction(self, terrain = None):
        for _ in range(10):
            dx = random.choice([-1,0,1])
            dy = random.choice([-1,0,1])
            if dx == 0 and dy == 0:
                continue
            new_x = self.position[0] + dx
            new_y = self.position[0] + dy
            if terrain and 0 <= new_x < terrain.width and 0 <= new_y < terrain.height:
                return (dx, dy)
        return (0,0)

    def step_change(self, hive=None, terrain=None):
        self.age += 1

        if self.age < self.warmup_time:
            print(f"Bee {self.id} is warming up.")
            return

        if self.type in ["queen", "drone"]:
            print(f"Bee {self.id} ({self.type}) remains in hive.")
            return
        
        if self.type == "worker":
            if self.state == "idle":
                self.state = "searching"
                self.direction = self.get_random_direction(terrain)
                print(f"Worker Bee {self.id} starts searching in direction {self.direction}.")
                return
            
            elif self.state == "searching":
                for _ in range(10):
                    self.direction = self.get_random_direction(terrain)
                    dx, dy = self.direction
                    new_pos = (self.position[0] + dx, self.position[1] + dy)
                    if 0 <= new_pos[0] < terrain.width and 0 <= new_pos[1] < terrain.height:
                        self.position = new_pos
                        break

                self.search_timer += 1
                print(f"Worker Bee {self.id} is searching at {self.position} (step {self.search_timer})")

                if terrain:
                    cell = terrain.get_cell(*self.position)
                    if cell == "F":
                        self.has_nectar = True
                        self.state = "returning"
                        print(f"Worker bee {self.id} found a flower at {self.position}! Returning to Hive ")
                        return 
                    elif cell == "W" or cell == "T":
                        print(f"Worker bee {self.id} hit an obstacle at {self.position}, returning hive ")
                        self.state = "idle"
                        self.search_timer = 0
                        self.position = (0, 0)
                        self.direction = (0, 0)
                        return
                    elif cell == "A":
                        print(f"Worker bee {self.id} was attacked by an animal at {self.position} and died")
                        self.state = "dead"
                        self.death_reason = "attacked by animal"
                        return

                if self.search_timer > self.search_patience + 2 and random.random() < 0.1:
                    print(f"Worker bee {self.id} got lost and died during search")
                    self.state = "dead"
                    self.death_reason = "lost while searching"
                    return

                if self.search_timer >= 2 and random.random() < 0.3:
                    self.has_nectar = True
                    self.state = "returning"
                    print(f"Worker Bee {self.id} found nectar! Returning to hive.")
                    return

                if self.search_timer >= self.search_patience:
                    self.state = "idle"
                    self.search_timer = 0
                    self.direction = (0, 0)
                    print(f"Worker Bee {self.id} gave up and returned to hive.")
                    return

            elif self.state == "returning":
                self.position = (0, 0)
                self.has_nectar = False
                self.search_timer = 0
                self.direction = self.get_random_direction(terrain)
                self.deposit_count += 1

                print(f"Worker Bee {self.id} returned to hive and deposited nectar.")
                print(f"Bee {self.id} made {self.deposit_count} deliveries.")

                if hive:
                    hive.deposit_nectar()

                if self.deposit_count >= self.energy:
                    self.state = "resting"
                    print(f"Bee {self.id} is resting after {self.deposit_count} deliveries.")
                else:
                    self.state = "idle"

                
            elif self.state == "resting":
                self.rest_timer += 1
                print(f"Bee {self.id} is resting... ({self.rest_timer}/{self.rest_duration})")

                if self.rest_timer >= self.rest_duration:
                    self.rest_timer = 0
                    self.deposit_count = 0  
                    self.energy = random.randint(3, 6)  
                    self.state = "idle"
                    print(f"Bee {self.id} is active again after resting.")
