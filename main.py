from vpython import *
import argparse
import logging
from point import Point 
from constraint import Spring 
from simulation import Simulation

# Use Numba - Cannot work with this library
# Fix Argparse with default values
# Custom gravity 
# Write C Modules to speed up the code - Useless
# Create a New Simulation

# UML is a general purpose modelling language
# It is used to describe a system
                    
if __name__ == "__main__":


    """
        Setting up Argument Parsing using argparse 

        I only read the type of simulation to run (rope default), the integration method that has
        to be used (Verlet default) and the timestep (0.01 default)
    """
    parser = argparse.ArgumentParser(
        prog='Cloth Simulation',
        description='These are the options that you can use with the script',
        epilog='Check out the Readme file to have a clear and thorough understanding of how to use the script'
    )
    parser.add_argument('-t', '--type', default = 'rope')
    parser.add_argument('-i', '--integration', default = 'Verlet')
    parser.add_argument('-dt', '--deltatime', type = float, default = 0.01)
    parser.add_argument('-f', '--friction', action = 'store_true', default = False)
    parser.add_argument('-d', '--debug', action = 'store_true')
    parser.add_argument('-gx', '--gravityx', type = float);
    parser.add_argument('-gy', '--gravityy', type = float);
    parser.add_argument('-gz', '--gravityz', type = float);
    args = parser.parse_args()

    simulation_object = args.type       # Object that is Simulated (e.g. rope, cloth)
    integration = args.integration      # Integration Method Used
    friction = args.friction            # Friction is used in the simulation or not
    dt = args.deltatime                 # Timestep used for integration

    # Get Custom Gravity
    gravity_x = args.gravityx
    gravity_y = args.gravityy
    gravity_z = args.gravityz
    if (gravity_x is None and gravity_y is None and gravity_z is None):
        gravity = vector(0, -9.81, 0)
    else:
        gravity = vector(
            0 if gravity_x is None else gravity_x,
            0 if gravity_y is None else gravity_y,
            0 if gravity_z is None else gravity_z
        )

    # Debug Mode 
    if args.debug:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)




    """
        Setting up the Simulation 
    """
    sim = Simulation(
        elasticity = 1000, 
        mass = 10, 
        friction = friction, 
        gravity = gravity, 
        dt = dt, 
        integration = integration 
    )
    match simulation_object:
        case 'grid':
            sim.grid()
        case 'cloth':
            sim.cloth1()
        case 'cloth2':
            sim.cloth2()
        case _:
            sim.rope()

