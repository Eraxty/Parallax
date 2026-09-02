class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def normalize(self, position):
        x, y = position
        nx = (x - self.width * 0.5) / (self.width * 0.5)
        ny = (y - self.height * 0.5) / (self.height * 0.5)
        return nx, ny
