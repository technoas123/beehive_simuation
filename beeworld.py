from bee import Bee
from hive import Hive
from terrain import Terrain
from visualizer import run_visual_simulation

def main():

    hive = Hive()
    terrain = Terrain(width =10, height=10)
    terrain.display()

    bees = []

    bees.append(Bee(0, "queen"))
    for i in range(1, 5):
        bees.append(Bee(i, "drone"))
    for i in range(5, 12):
        bees.append(Bee(i, "worker"))

    run_visual_simulation(bees, hive, terrain, total_steps=30)


if __name__ == "__main__":
    main()
