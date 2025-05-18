from frame import Frame

class Hive:
    def __init__(self, num_frames = 6):
        self.total_nectar = 0
        self.frames = [Frame() for _ in range(num_frames)]

    def deposit_nectar(self):
        self.total_nectar += 1
        for frame in self.frames:
            if frame.add_nectar():
                return True
        print(f"All frames are full! Cannot store more nectar")
        return False