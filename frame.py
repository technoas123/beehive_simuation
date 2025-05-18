class Frame:
    def __init__(self, num_cells=10):
        self.cells = [0] * num_cells

    def add_nectar(self):
        for i in range(len(self.cells)):
            if self.cells[i] < 5:
                self.cells[i] += 1
                print(f"Nectar added to cell {i}. Fill level: {self.cells[i]}/5")
                return True
        print(f"Frame is full, no space to add nectar")
        return False

    @property
    def fill_level(self):
        # Returns total nectar in the frame (sum of all cell nectar values)
        return sum(self.cells)
