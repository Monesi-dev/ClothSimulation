from vpython import *
import sys

# Create a Point and Spring Class
# Create a Simulation Class (Factory, Singleton)
# 1) Add Type Hints
# 2) Create Spring Class
# 3) Create Simulation Class

class Point:

    __slots__ = ('pos', 'prev_pos', 'mass', 'fixed', 'vel', 'acc', 'friction', 'object')

    def __init__(self, pos: vector, mass: float, friction: float = 1, fixed: bool = False, integration: str = 'Verlet') -> None:

        # Variable Declaration
        self.pos = pos               # Position of the Node
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

    # Updates Position doing Numerical Integration and Renders the Node
    def update(self, dt: float) -> None:

        # If the point is fixed the position won't be updated
        if self.fixed:  return

        # Numerical Integration
        print(sys.version)
        match self.integration:
            case 'Verlet':
                disp = self.pos - self.prev_pos
                self.acc -= self.friction * disp / dt
                self.pos = 2 * self.pos - self.prev_pos + self.acc * dt ** 2
                self.prev_pos = disp + self.prev_pos

        # Numerical Integration
        # self.acc -= self.friction * self.vel
        # self.vel += self.acc * dt
        # self.pos += self.vel * dt

        self.acc = vector(0, 0, 0)

        # Rendering the Node
        self.object.pos = self.pos

class Spring:

    __slots__ = ('node1', 'node2', 'length', 'elasticity', 'line')

    def __init__(self, node1: Point, node2: Point, length: float, elasticity: float) -> None:

        # Variable Declaration
        self.node1 = node1              # Node attached to the Beginning of the Spring
        self.node2 = node2              # Node attached to the End of the Spring    
        self.length = length            # Length at Rest
        self.elasticity = elasticity    # Elasticity of the Spring

        # Rendering the Spring
        self.line = curve(self.node1.pos, self.node2.pos)

    def apply_constraints(self):

        # Compute Elastic Force
        nodes_displacement = self.node1.pos - self.node2.pos
        deformation = nodes_displacement.mag - self.length
        elastic_force = deformation * self.elasticity * nodes_displacement.norm()

        # Add Elastic Force to the two Nodes
        self.node1.add_force(-1 * elastic_force)
        self.node2.add_force(elastic_force)

    def display(self):

        # Rendering the Updated Spring 
        self.line.modify(0, self.node1.pos)
        self.line.modify(1, self.node2.pos)

class Simulation:

    __slots__ = ('points', 'springs', 'elasticity', 'mass', 'friction', 'gravity', 'dt')

    def __init__(self, elasticity, mass, friction, gravity, dt):
        self.points = []
        self.springs = []
        self.elasticity = elasticity
        self.mass = mass
        self.friction = friction
        self.gravity = gravity
        self.dt = dt

    def rope(self):

        points_num = 10
        for i in range(points_num):
            self.points.append(Point(
                vector(i, -i / 3, 0),
                self.mass,
                self.friction,
                (i == 0 or i == points_num - 1)
            ))

        springs_num = 9
        for i in range(springs_num):
            self.springs.append(Spring(
                self.points[i],
                self.points[i + 1],
                0.5,
                self.elasticity
            ))
        self.run()

    def grid(self):

        points_num = 100
        for i in range(points_num):
            self.points.append(Point(
                vector((i % 10 - 4.5), 0, (i // 10 - 4.5)),
                self.mass,
                self.friction,
                (i == 0 or i == 9 or i == 90 or i == 99)
            ))

        for i in range(points_num):
            if (i % 10 != 9):
                self.springs.append(Spring(
                    self.points[i],
                    self.points[i + 1],
                    0.5,
                    self.elasticity
                ))
            if (i // 10 != 9):
                self.springs.append(Spring(
                    self.points[i],
                    self.points[i + 10],
                    0.5,
                    self.elasticity
                ))
        self.run()

    def run(self):

        dt, g = self.dt, self.gravity

        while True:
            rate(1/dt)
            for spring in self.springs:
                spring.apply_constraints()
            for point in self.points:
                point.add_force(point.mass * g) # A bit ugly
                point.update(dt)
            for spring in self.springs:
                spring.display()
            pass

# UML is a general purpose modelling language
# It is used to describe a system

if __name__ == "__main__":

    sim = Simulation(1000, 10, 0.5, vector(0,-9.81, 0), 0.01)
    sim.grid()

    """
    points_num = 5
    springs_num = 4
    points = []
    for i in range(points_num):
        points.append(Point(
            vector(i, -i, 0),
            10,
            0.3,
            (i == 0 or i == points_num - 1)
        ))
    springs = []
    for i in range(springs_num):
        springs.append(Spring(
            points[i],
            points[i + 1],
            0.5,
            100
        ))
    g = vector(0, -9.81, 0)
    dt = 0.01

    while True:
        rate(1/dt)
        for spring in springs:
            spring.apply_constraints()
        for point in points:
            point.add_force(point.mass * g) # A bit ugly
            point.update(dt)
        for spring in springs:
            spring.display()
        pass
    """
