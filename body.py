class Body:
    def __init__(self, mass, x, y, vx, vy, color):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def update_position(self, dt, sim_speed):
        self.x += self.vx * dt * sim_speed
        self.y += self.vy * dt * sim_speed
