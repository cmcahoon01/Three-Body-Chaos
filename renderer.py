import collections
import pygame
from constants import *


class Renderer:
    def __init__(self, simulation):
        pygame.init()

        self.width, self.height = 800, 800
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Three-Body Orbit Simulation")

        self.screen = screen
        self.simulation = simulation
        self.frame_rate = 60
        self.clock = pygame.time.Clock()

        self.trail_duration = 3  # seconds
        self.trail_length = self.frame_rate * self.trail_duration
        self.trails = [collections.deque(maxlen=self.trail_length) for _ in simulation.bodies]

    def run(self):
        while self.simulation.running:
            self.handle_events()
            self.render()
            self.clock.tick(self.frame_rate)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.simulation.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.simulation.sim_speed *= 1.1
                elif event.key == pygame.K_DOWN:
                    self.simulation.sim_speed /= 1.1
                elif event.key == pygame.K_RIGHT:
                    self.frame_rate = min(240, self.frame_rate + 5)
                    self.trail_length = self.frame_rate * self.trail_duration
                elif event.key == pygame.K_LEFT:
                    self.frame_rate = max(10, self.frame_rate - 5)
                    self.trail_length = self.frame_rate * self.trail_duration

    def render(self):
        bg = (108, 188, 204)
        self.screen.fill(bg)

        for i, body in enumerate(self.simulation.bodies):
            self.trails[i].append((int(body.x * self.width // max_x),
                                   int(body.y * self.height // max_y)))
            self.draw_trail(self.trails[i], body.color, bg)

        # Draw bodies
        for body in self.simulation.bodies:
            pygame.draw.circle(self.screen, (0, 0, 0),
                               (body.x * self.width // max_x,
                                body.y * self.height // max_y),
                               int(body.mass) + 2)
            pygame.draw.circle(self.screen, body.color,
                               (body.x * self.width // max_x,
                                body.y * self.height // max_y),
                               int(body.mass))

        # Display simulation speed and frame rate
        font = pygame.font.Font(None, 36)
        speed_text = font.render(f"Simulation Speed:    {self.simulation.sim_speed:.2f}x          (up & down arrows)",
                                 True, (255, 255, 255))
        fps_text = font.render(f"Frame Rate:                {self.frame_rate} FPS       (left & right arrows)", True,
                               (255, 255, 255))
        self.screen.blit(speed_text, (10, 10))
        self.screen.blit(fps_text, (10, 50))

        pygame.display.flip()

    def draw_trail(self, trail, color, bg):
        for i, pos in enumerate(trail):
            alpha = int(255 * i / len(trail))
            pygame.draw.circle(self.screen, self.weighted_average_color([color, bg], [alpha, 255 - alpha]), pos, 2)

    def weighted_average_color(self, colors, weights):
        r = sum(c[0] * w for c, w in zip(colors, weights)) / sum(weights)
        g = sum(c[1] * w for c, w in zip(colors, weights)) / sum(weights)
        b = sum(c[2] * w for c, w in zip(colors, weights)) / sum(weights)
        return r, g, b
