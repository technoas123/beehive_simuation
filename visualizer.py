from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, RegularPolygon, Rectangle, Polygon


def run_visual_simulation(bees, hive, terrain, total_steps=30):
    fig, (hive_ax, world_ax) = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle("Bee Simulation - Live View")

    for bee in bees:
        bee.path_history = [bee.position]

    def draw_symbol(ax, x, y, symbol_type):
        if symbol_type == "flower":
            ax.add_patch(RegularPolygon((x + 0.5, y + 0.5), numVertices=5, radius=0.3, color="yellow"))
        elif symbol_type == "tree":
            ax.add_patch(Polygon([[x+0.5, y+0.1], [x+0.1, y+0.9], [x+0.9, y+0.9]], closed=True, color="darkgreen"))
        elif symbol_type == "water":
            ax.add_patch(Circle((x + 0.5, y + 0.5), radius=0.3, color="blue"))
        elif symbol_type == "animal":
            ax.add_patch(Polygon([[x+0.3, y+0.3], [x+0.7, y+0.3], [x+0.5, y+0.7]], closed=True, color="red"))
        elif symbol_type == "danger":
            ax.add_patch(RegularPolygon((x + 0.5, y + 0.5), numVertices=3, radius=0.4, color="black"))

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

        world_ax.set_facecolor("lightgreen")

        for y in range(terrain.height):
            for x in range(terrain.width):
                cell = terrain.get_cell(x, y)
                if cell == "F":
                    draw_symbol(world_ax, x, y, "flower")
                elif cell == "T":
                    draw_symbol(world_ax, x, y, "tree")
                elif cell == "W":
                    draw_symbol(world_ax, x, y, "water")
                elif cell == "A":
                    draw_symbol(world_ax, x, y, "animal")
                elif cell == "D":
                    draw_symbol(world_ax, x, y, "danger")

        for bee in bees:
            if bee.state != "dead":
                x, y = bee.position
                color = {
                    "worker": "yellow",
                    "queen": "purple",
                    "drone": "cyan"
                }.get(bee.type, "white")
                world_ax.plot(x + 0.5, y + 0.5, "o", markersize=7, color=color)

                if bee.type == "worker" and hasattr(bee, "path_history"):
                    path_x = [px + 0.5 for px, py in bee.path_history]
                    path_y = [py + 0.5 for px, py in bee.path_history]
                    world_ax.plot(path_x, path_y, color="orange", alpha=0.4, linewidth=1)

        hive_ax.cla()
        hive_ax.set_title("Hive Storage")
        fill_levels = []
        for i, frame in enumerate(hive.frames):
            if hasattr(frame, "cells"):
                fill = sum(frame.cells)
                fill_levels.append(fill / len(frame.cells))
            else:
                fill_levels.append(0)
        hive_ax.bar(range(len(fill_levels)), fill_levels, color="gold", edgecolor="black")
        hive_ax.set_ylim(0, 5)
        hive_ax.set_xlabel("Frame")
        hive_ax.set_ylabel("Avg Nectar Fill")

    ani = FuncAnimation(fig, update, frames=total_steps, interval=1200, repeat=False)
    plt.tight_layout()
    plt.show()

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