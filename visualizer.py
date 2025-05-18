from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches

def run_visual_simulation(bees, hive, terrain, total_steps=30):
    fig, (hive_ax, world_ax) = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle("Bee Simulation - Live View")

    for bee in bees:
        bee.path_history = [bee.position]

    def update(frame_number):
        print(f"\nTime Step {frame_number + 1}")

        if (frame_number + 1) % 5 == 0 and len(bees) < 50:
            new_id = len(bees)
            new_bee = bees[0].__class__(new_id, "worker")
            bees.append(new_bee)
            new_bee.path_history = [new_bee.position]
            print(f"Queen Bee created a new worker bee {new_id}")

        for bee in bees:
            bee.step_change(hive, terrain)
            if hasattr(bee, "path_history"):
                bee.path_history.append(bee.position)
                if len(bee.path_history) > 20:
                    bee.path_history.pop(0)

        world_ax.cla()
        world_ax.set_title("World Terrain")
        world_ax.set_xlim(0, terrain.width)
        world_ax.set_ylim(0, terrain.height)
        world_ax.set_xticks([])
        world_ax.set_yticks([])

        color_map = {"F": "green", "W": "blue", "T": "darkgreen", "A": "red", "D": "black"}
        for y in range(terrain.height):
            for x in range(terrain.width):
                cell = terrain.get_cell(x, y)
                color = color_map.get(cell, "lightgrey")
                world_ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color, alpha=0.3))

        for bee in bees:
            if bee.state != "dead":
                x, y = bee.position
                marker_color = {
                    "worker": "yellow",
                    "queen": "purple",
                    "drone": "cyan"
                }.get(bee.type, "white")
                world_ax.plot(x + 0.5, y + 0.5, "o", markersize=7, color=marker_color)

                if bee.type == "worker" and hasattr(bee, "path_history"):
                    path_x = [px + 0.5 for px, py in bee.path_history]
                    path_y = [py + 0.5 for px, py in bee.path_history]
                    world_ax.plot(path_x, path_y, color="orange", alpha=0.4, linewidth=1)

        worker_patch = mpatches.Patch(color='yellow', label='Worker Bee')
        queen_patch = mpatches.Patch(color='purple', label='Queen Bee')
        drone_patch = mpatches.Patch(color='cyan', label='Drone Bee')
        flower_patch = mpatches.Patch(color='green', label='Flower')
        water_patch = mpatches.Patch(color='blue', label='Water')
        tree_patch = mpatches.Patch(color='darkgreen', label='Tree')
        animal_patch = mpatches.Patch(color='red', label='Animal')

        world_ax.legend(handles=[worker_patch, queen_patch, drone_patch, flower_patch, water_patch, tree_patch, animal_patch], loc='upper right', fontsize=7)

        hive_ax.cla()
        hive_ax.set_title("Hive Storage")
        fill_levels = []
        for frame in hive.frames:
            fill = sum(frame.cells) if hasattr(frame, "cells") else 0
            fill_levels.append(fill / len(frame.cells) if hasattr(frame, "cells") else 0)
        hive_ax.bar(range(len(fill_levels)), fill_levels, color="gold", edgecolor="black")
        hive_ax.set_ylim(0, 5)
        hive_ax.set_xlabel("Frame")
        hive_ax.set_ylabel("Avg Nectar Fill")

    ani = FuncAnimation(fig, update, frames=total_steps, interval=1200, repeat=False)
    plt.tight_layout()
    plt.show()

    # Show summary once animation ends
    print("\nSimulation Summary")
    print(f"Total nectar collected: {hive.total_nectar}")
    dead_bees = [b for b in bees if b.state == "dead"]
    print(f"Total bees died: {len(dead_bees)}")
    for b in dead_bees:
        print(f"Bee {b.id} ({b.type}) died due to: {b.death_reason}")
    top_bee = max([b for b in bees if b.type == "worker"], key=lambda b: b.deposit_count, default=None)
    if top_bee:
        print(f"Top performer: Bee {top_bee.id} with {top_bee.deposit_count} deliveries")
    print(f"Final Bee Count: {len(bees)}")
