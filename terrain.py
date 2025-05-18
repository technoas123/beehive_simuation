import random

class Terrain:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = self.generate_grid()

    def generate_grid(self):
        elements = ["F", "T", "W", ".", "A", "D"]  
        weights = [0.2, 0.2, 0.1, 0.4, 0.05, 0.05]
        grid = []

        for _ in range(self.height):
            row = random.choices(elements, weights=weights, k=self.width)
            grid.append(row)
        return grid
    
    

    def display(self):
        print("\nTERRAIN MAP")
        for row in self.grid:
            print(" ".join(row))

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]  
        return "O"  
