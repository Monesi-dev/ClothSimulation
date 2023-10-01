from point import Point 
from constraint import Spring
from vpython import * 
import matplotlib.pyplot as plt
import logging

class Simulation:

    __slots__ = ('points', 'total_graph', 'kinetic_graph', 'elastic_graph', 'gravitational_graph', 'springs', 'elasticity', 'mass', 'friction', 'integration', 'gravity', 'dt', 't', 'simulating', 'event', 'drag', 'dragged_point')

    def __init__(self, elasticity: float, mass: float, friction: float, gravity: vector, dt: float, integration: str):

        # Variables
        self.points = []
        self.springs = []
        self.elasticity = elasticity
        self.mass = mass
        self.friction = friction
        self.gravity = gravity
        self.integration = integration
        self.dt = dt
        self.t = 0 

        # Graph
        graph(scroll=True, xmin = 0, xmax = 5)
        self.total_graph = gcurve(color=color.black, label="E<sub>total</sub>", interval=1)
        self.kinetic_graph = gcurve(color=color.red, label="E<sub>kinetic</sub>", interval=1)
        self.elastic_graph = gcurve(color=color.green, label="E<sub>elastic</sub>", interval=1)
        self.gravitational_graph = gcurve(color=color.blue, label="E<sub>gravitational</sub>", interval=1)
        
        # Simulation
        self.simulating = False 
        self.drag = False
        button(
            pos = scene.title_anchor,       # Displayed above the scene
            text = 'Run',                   # Text on the Button 
            bind = self.start_and_stop      # Function Invoked when the Button is Clicked
        )

        # Mouse Events
        def mouse_click(ev):
            logging.debug(f"mouse_click \n ev.pos: {ev.pos}, object: {scene.mouse.pick}")

            if isinstance(scene.mouse.pick, curve):
                self.delete_spring(scene.mouse.pick)

        scene.bind('click', mouse_click)


        def mouse_down():
            logging.debug(f"mouse_down \n object: {scene.mouse.pick}")

            if isinstance(scene.mouse.pick, sphere):
                for point in self.points:
                    if point.object == scene.mouse.pick:
                        self.drag = True
                        self.dragged_point = point

        scene.bind('mousedown', mouse_down)


        def mouse_move():
            logging.debug(f"mouse_move \n pos: {scene.mouse.pos}")
            if self.drag and self.dragged_point:
                self.dragged_point.pos = scene.mouse.pos 
                self.dragged_point.object.pos = scene.mouse.pos 

        scene.bind('mousemove', mouse_move)


        def mouse_up():
            self.dragged_point = None 
            self.drag = False

        scene.bind('mouseup', mouse_up)

    def delete_spring(self, line_to_delete):

        for spring in self.springs:
            if spring.line == line_to_delete:
                spring.line.visible = False 
                self.springs.remove(spring)

    def start_and_stop(self):
        self.simulating = not self.simulating
        logging.warning("Button Pressed")

    def print_energy(self):

        kinetic_energy = 0 
        gravitational_energy = 0 
        elastic_energy = 0

        for point in self.points:
            kinetic_energy += point.kinetic_energy() 
            gravitational_energy += point.gravitational_energy(self.gravity)
        for spring in self.springs: 
            elastic_energy += spring.elastic_energy()
        total_energy = kinetic_energy + gravitational_energy + elastic_energy

        self.kinetic_graph.plot(self.t, kinetic_energy)
        self.gravitational_graph.plot(self.t, gravitational_energy)
        self.elastic_graph.plot(self.t, elastic_energy)
        self.total_graph.plot(self.t, total_energy)

    def rope(self):

        points_num = 10
        for i in range(points_num):
            self.points.append(Point(
                pos = vector(i, -i / 3, 0),
                mass = self.mass,
                friction = self.friction,
                fixed = (i == 0 or i == points_num - 1),
                integration = self.integration
            ))

        springs_num = 9
        for i in range(springs_num):
            self.springs.append(Spring(
                node1 = self.points[i],
                node2 = self.points[i + 1],
                length = 0.5,
                elasticity = self.elasticity
            ))
        self.run()

    def grid(self):

        points_num = 100
        for i in range(points_num):
            self.points.append(Point(
                pos = vector((i % 10 - 4.5), 0, (i // 10 - 4.5)),
                mass = self.mass,
                friction = self.friction,
                fixed = (i == 0 or i == 9 or i == 90 or i == 99),
                integration = self.integration
            ))

        for i in range(points_num):
            if (i % 10 != 9):
                self.springs.append(Spring(
                    node1 = self.points[i],
                    node2 = self.points[i + 1],
                    length = 0.5,
                    elasticity = self.elasticity
                ))
            if (i // 10 != 9):
                self.springs.append(Spring(
                    node1 = self.points[i],
                    node2 = self.points[i + 10],
                    length = 0.5,
                    elasticity = self.elasticity
                ))
        self.run()

    def cloth(self):

        points_num = 64
        for i in range(points_num):
            self.points.append(Point(
                pos = vector((i % 8 - 3.5), (i // 8 - 3.5), 0),
                mass = self.mass,
                friction = self.friction,
                fixed = (i == 56 or i == 63),
                integration = self.integration
            ))

        for i in range(points_num):
            # Horizontal Springs
            if (i % 8 != 7):
                self.springs.append(Spring(
                    node1 = self.points[i],
                    node2 = self.points[i + 1],
                    length = 0.5,
                    elasticity = self.elasticity
                ))

            # Vertical Springs
            if (i // 8 != 7):
                self.springs.append(Spring(
                    node1 = self.points[i],
                    node2 = self.points[i + 8],
                    length = 0.5,
                    elasticity = self.elasticity
                ))

    def cloth1(self):
        self.cloth()
        self.run()

    def cloth2(self):

        self.cloth()
        for i in range(64):
            # Vertical Springs
            if (i // 8 != 7):
                self.springs.append(Spring(
                    node1 = self.points[i],
                    node2 = self.points[i + 8],
                    length = 0.5,
                    elasticity = self.elasticity
                ))

            # Cross Springs 
            if (i % 8 != 7):
                if (i // 8 != 7):
                    self.springs.append(Spring(
                        node1 = self.points[i],
                        node2 = self.points[i + 9],
                        length = 0.5,
                        elasticity = self.elasticity / 8
                    ))
                if (i // 8 != 0):
                    self.springs.append(Spring(
                        node1 = self.points[i],
                        node2 = self.points[i - 7],
                        length = 0.5,
                        elasticity = self.elasticity / 8
                    ))


        self.run()

    def run(self):

        dt, g = self.dt, self.gravity

        while True:
            rate(1/dt)
            if self.drag or not self.simulating: continue

            # if self.event.event == 'mousedown':
            #     logging.warning('Mouse Down')

            for spring in self.springs:
                spring.apply_constraints()
            for point in self.points:
                point.add_force(point.mass * g) # A bit ugly
                point.update(dt)
            for spring in self.springs:
                spring.display()

            self.print_energy()
            self.t += dt
            plt.show(block=False)


