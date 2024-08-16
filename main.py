import pygame
import threading
from simulation import Simulation
from tracking import Tracker
from renderer import Renderer

stable_configurations = [
    {'a x': 293.4831059332122, 'a y': 340.7526146133576, 'b x': 207.6874621748057, 'b y': 526.290457384429,
     'a theta': 1.1499371903248015, 'b theta': 2.609578070620085, 'a v': 0.5612483578055892,
     'b v': 0.301090192241877, 'a mass': 3.666566944968005, 'b mass': 7.776398736154373,
     'c distance': 59.46102594961805},
    {'a x': 104.17737708365757, 'a y': 569.227423981332, 'b x': 671.6452572949624, 'b y': 324.961823394208,
     'a theta': 3.9197229974057177, 'b theta': 0.6133406953066498, 'a v': 0.09528244951152949,
     'b v': 0.25696968791320324, 'a mass': 4.146595972750713, 'b mass': 6.029078482784673,
     'c distance': 446.8401251757416},
    {'a x': 813.9563716536032, 'a y': 552.1546570021276, 'b x': 546.732381025328, 'b y': 349.3744660022239,
     'a theta': 3.3254127917925818, 'b theta': 4.974676475824828, 'a v': 0.26361858250369113,
     'b v': 0.4762417047995062, 'a mass': 7.847380566972252, 'b mass': 9.485741772349007,
     'c distance': 18.749995469478684},
]


def main():
    simulation = Simulation(stable_configurations[-1])  # Change this to test different configurations
    tracker = Tracker(simulation)
    simulation.tracker = tracker
    renderer = Renderer(simulation)

    # Start simulation thread
    sim_thread = threading.Thread(target=simulation.run)
    sim_thread.start()

    # Start rendering loop
    renderer.run()

    # Clean up
    simulation.running = False
    sim_thread.join()

    tracker.plot()


if __name__ == "__main__":
    main()
