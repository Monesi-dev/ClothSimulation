from point import Point
from vpython import curve

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

    def apply_constraints(self) -> None:

        # Compute Elastic Force
        nodes_displacement = self.node1.pos - self.node2.pos
        deformation = nodes_displacement.mag - self.length
        elastic_force = deformation * self.elasticity * nodes_displacement.norm()

        # Add Elastic Force to the two Nodes
        self.node1.add_force(-1 * elastic_force)
        self.node2.add_force(elastic_force)

    def elastic_energy(self) -> float:
        nodes_displacement = self.node1.pos - self.node2.pos
        deformation = nodes_displacement.mag - self.length
        return 1 / 2 * self.elasticity * deformation ** 2
        

    def display(self) -> None:

        # Rendering the Updated Spring 
        self.line.modify(0, self.node1.pos)
        self.line.modify(1, self.node2.pos)
