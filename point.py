from vpython import vector, sphere, color

class Point:

    __slots__ = ('pos', 'first_pos', 'prev_pos', 'mass', 'fixed', 'vel', 'acc', 'friction', 'object', 'integration')

    def __init__(self, pos: vector, mass: float, friction: float = 1, fixed: bool = False, integration: str = 'Verlet') -> None:

        # Variable Declaration
        self.pos = pos               # Position of the Node
        self.first_pos = pos         # Used to compute gravitational Potential Energy
        self.prev_pos = pos          # Used for Numerical Integration
        self.mass = mass             # Mass of the Node
        self.fixed = fixed           # Determines whether the Node is Fixed
        self.vel = vector(0, 0, 0)   # Velocity of the Node
        self.acc = vector(0, 0, 0)   # Acceleration of the Node
        self.friction = friction     # Adds Friction if required
        self.integration = integration      # Method Used for Numerical Integration

        # Rendering the Node with a Sphere
        self.object = sphere(
            pos = pos,          # Position of the Node
            radius = 0.1,         # Radius of the Node
            color = color.red   # Color of the Node
        )

    def add_force(self, force: vector) -> None:
        self.acc += force / self.mass   # Simply Computing Acceleration From Force

    def kinetic_energy(self) -> float:
        return 1 / 2 * self.mass * self.vel.mag ** 2

    def gravitational_energy(self, g: vector) -> float:
        return -self.mass * g.dot(self.pos - self.first_pos)

    # Updates Position doing Numerical Integration and Renders the Node
    def update(self, dt: float) -> None:

        # If the point is fixed the position won't be updated
        if self.fixed:  return

        # Numerical Integration
        match self.integration:

            # Basically Euler Method
            case 'RK1':
                self.acc -= self.friction * self.vel
                self.vel += self.acc * dt
                self.pos += self.vel * dt

            # Verlet Integration
            case _:
                disp = self.pos - self.prev_pos
                self.vel = disp / dt
                self.acc -= self.friction * self.vel 
                self.pos = 2 * self.pos - self.prev_pos + self.acc * dt ** 2
                self.prev_pos = disp + self.prev_pos

        self.acc = vector(0, 0, 0)

        # Rendering the Node
        self.object.pos = self.pos
