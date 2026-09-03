import pygame
import numpy as np

class Renderer:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Parallax Interlaced")
        self.width = width
        self.height = height

        self.background = pygame.Surface((width, height))
        self.middle = pygame.Surface((width, height), pygame.SRCALPHA)
        self.foreground = pygame.Surface((width, height), pygame.SRCALPHA)

        self.background.fill((50, 50, 70))
        pygame.draw.rect(self.middle, (100, 100, 130), (250, 150, 780, 420))
        pygame.draw.circle(self.foreground, (220, 220, 220), (640, 360), 100)

        self.lpi = 60
        self.stripe_width = 2

    def render_view(self, ox, oy):
        surf = pygame.Surface((self.width, self.height))
        surf.fill((20, 20, 20))
        surf.blit(self.background, (ox * 10, oy * 10))
        surf.blit(self.middle, (ox * 30, oy * 30))
        surf.blit(self.foreground, (ox * 60, oy * 60))
        return pygame.surfarray.array3d(surf)

    def draw(self, offset_x, offset_y):
        v_left = self.render_view(offset_x - 20, offset_y)
        v_right = self.render_view(offset_x + 20, offset_y)

        final = np.zeros((self.width, self.height, 3), dtype=np.uint8)

        for x in range(self.width):
            if (x // self.stripe_width) % 2 == 0:
                final[x] = v_left[x]
            else:
                final[x] = v_right[x]

        pygame.surfarray.blit_array(self.screen, final)
        pygame.display.flip()

    def close(self):
        pygame.quit()
