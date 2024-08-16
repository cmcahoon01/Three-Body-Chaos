import math
import time
from random import random, seed
from body import Body
from utils import random_color, random_centered, rough_escape_velocity, has_escaped
from tracking import center_of_mass
from constants import *


class Simulation:
    def __init__(self, parameters=None, sim_speed=1):
        self.parameters = parameters
        if parameters is None:
            self.randomize_parameters()
        self.dt = 1  # Time step
        self.running = True
        self.sim_speed = sim_speed  # Simulation speed multiplier

        self.bodies = []
        self.add_two_bodies()
        seed(0)
        self.add_balancing_body()
        print("Initial state:")
        for i, body in enumerate(self.bodies):
            print(f"Body {i + 1}: mass={body.mass:.2f}, x={body.x:.2f}, y={body.y:.2f}, "
                  f"vx={body.vx:.2f}, vy={body.vy:.2f}")

        self.tracker = None

        self.escape_velocity = rough_escape_velocity([body.mass for body in self.bodies])

    def add_two_bodies(self):
        p = self.parameters

        vx = p["a v"] * math.cos(p["a theta"])
        vy = p["a v"] * math.sin(p["a theta"])
        self.bodies.append(Body(p["a mass"], p["a x"], p["a y"], vx, vy, random_color()))

        vx = p["b v"] * math.cos(p["b theta"])
        vy = p["b v"] * math.sin(p["b theta"])
        self.bodies.append(Body(p["b mass"], p["b x"], p["b y"], vx, vy, random_color()))

    def add_balancing_body(self):
        # Calculate the current center of mass and total momentum
        total_mass = sum(body.mass for body in self.bodies)
        com_x = sum(body.mass * body.x for body in self.bodies) / total_mass
        com_y = sum(body.mass * body.y for body in self.bodies) / total_mass
        total_px = sum(body.mass * body.vx for body in self.bodies)
        total_py = sum(body.mass * body.vy for body in self.bodies)

        distance_from_center = random_centered() * max_x / 2
        # Calculate the position for the new body
        center_x, center_y = 500, 500
        angle = math.atan2(center_y - com_y, center_x - com_x)
        new_x = center_x + distance_from_center * math.cos(angle)
        new_y = center_y + distance_from_center * math.sin(angle)

        # Calculate the mass for the new body
        new_mass = total_mass * math.sqrt((com_x - center_x) ** 2 + (com_y - center_y) ** 2) / distance_from_center

        # Calculate the velocity for the new body
        new_vx = -total_px / new_mass
        new_vy = -total_py / new_mass

        # Create and add the new body
        new_body = Body(new_mass, new_x, new_y, new_vx, new_vy, (235, 231, 21))
        self.bodies.append(new_body)

    def run(self):
        while self.running:
            self.update()
            time.sleep(0.001)  # Small delay to prevent this thread from consuming too much CPU

    def update(self):
        # Update velocities
        for i, body1 in enumerate(self.bodies):
            for body2 in self.bodies[i + 1:]:
                dx = body2.x - body1.x
                dy = body2.y - body1.y
                r = math.sqrt(dx ** 2 + dy ** 2)
                f = gravitational_constant * body1.mass * body2.mass / (r ** 2 + 1e-6)

                body1.vx += f * dx / r / body1.mass * self.dt * self.sim_speed
                body1.vy += f * dy / r / body1.mass * self.dt * self.sim_speed
                body2.vx -= f * dx / r / body2.mass * self.dt * self.sim_speed
                body2.vy -= f * dy / r / body2.mass * self.dt * self.sim_speed

        # Update positions
        for body in self.bodies:
            body.update_position(self.dt, self.sim_speed)

        self.tracker.tick()
        if has_escaped(self):
            self.running = False
        if self.tracker.get_score() > max_steps and self.sim_speed > 10:
            self.running = False

    def randomize_parameters(self):
        self.parameters = {}
        for name, value in parameter_domains.items():
            self.parameters[name] = random_centered() * (value[1] - value[0]) + value[0]
