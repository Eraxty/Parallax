import pygame

class Renderer:
    def __init__(self, width=1280, height=720):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Parallax")

        self.width = width
        self.height = height

        self.background = pygame.Surface((width, height))
        self.middle = pygame.Surface((width, height), pygame.SRCALPHA)
        self.foreground = pygame.Surface((width, height), pygame.SRCALPHA)

        self.background.fill((50, 50, 70))

        pygame.draw.rect(
            self.middle,
            (100, 100, 130),
            (250, 150, 780, 420)
        )

        pygame.draw.circle(
            self.foreground,
            (220, 220, 220),
            (640, 360),
            100
        )

    def draw(self, offset_x, offset_y):
        self.screen.fill((20, 20, 20))

        background_x = offset_x * 10
        background_y = offset_y * 10

        middle_x = offset_x * 30
        middle_y = offset_y * 30

        foreground_x = offset_x * 60
        foreground_y = offset_y * 60

        self.screen.blit(self.background,(background_x, background_y))

        self.screen.blit(self.middle,(middle_x, middle_y))

        self.screen.blit(self.foreground,(foreground_x, foreground_y))

        pygame.display.flip()

    def close(self):
        pygame.quit()