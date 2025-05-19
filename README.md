# 🐝 Bee Simulation Project

A visual and interactive simulation that models the behavior of bees in a hive-based ecosystem. This project showcases worker bees exploring terrain, collecting nectar from flowers, avoiding obstacles, and returning resources to the hive — all in a dynamic, animated environment using Python and Matplotlib.

---

## 🚀 Features

- Worker, Drone, and Queen bee roles simulated
- Realistic nectar collection and energy/rest cycles
- Smart terrain interaction with flowers, trees, water, animals
- Animated real-time visualization with bee paths and hive activity
- Extensible and readable code structure for educational use

---

## 🛠️ Tools & Technologies

| Tool         | Purpose                            |
|--------------|------------------------------------|
| Python       | Main programming language          |
| Matplotlib   | Animation and visualization        |
| Tkinter      | Backend for GUI rendering          |
| NumPy        | (Optional) Grid and data handling  |

---


---

## ▶️ How to Run

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/bee-simulation.git
   cd bee-simulation
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
3. **Start Simulation**
   ```bash
   python main.py


---

## 🔧 Tools & Technologies Used

- **Python 3.11+**
- `matplotlib` — for visual output
- `tkinter` — GUI support (underlying)
- `random` — for bee movement, energy, decisions

---

## 💡 Code Highlights

### 1. Bee Movement Logic

```python
def step_change(self, hive=None, terrain=None):
    if self.state == "searching":
        dx, dy = self.direction
        self.position = (self.position[0] + dx, self.position[1] + dy)
        if terrain.get_cell(*self.position) == "F":
            self.state = "returning"
```
Each bee:
- Picks a direction
- Moves step-by-step
- Reacts to what’s in the terrain (flower, water, etc.)
- Returns to hive if successful

