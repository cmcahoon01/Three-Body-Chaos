import math
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from utils import evaluate_periodicity
from constants import *


def center_of_mass(bodies):
    total_mass = sum(body.mass for body in bodies)
    com_x = sum(body.mass * body.x for body in bodies) / total_mass
    com_y = sum(body.mass * body.y for body in bodies) / total_mass
    return com_x, com_y


def average_velocity(bodies):
    total_velocity = 0
    for body in bodies:
        total_velocity += math.sqrt(body.vx ** 2 + body.vy ** 2)
    return total_velocity / len(bodies)


def average_distance_from_center(bodies, center=(500, 500)):
    total_distance = 0
    for body in bodies:
        total_distance += math.sqrt((body.x - center[0]) ** 2 + (body.y - center[1]) ** 2)
    return total_distance / len(bodies)


class Tracker:
    def __init__(self, simulation):
        self.simulation = simulation
        self.bodies = None
        self.center_of_mass = []
        self.average_velocity = []
        self.average_distance_from_center = []
        self.lifetime = 0

    def get_score(self):
        if self.lifetime < max_steps:
            return self.lifetime
        center_score = evaluate_periodicity(self.average_distance_from_center, (0, 0.05))
        velocity_score = evaluate_periodicity(self.average_velocity, (0, 0.05))
        return 1000 + center_score + velocity_score

    def tick(self):
        if self.bodies is None:
            self.bodies = self.simulation.bodies
        self.center_of_mass.append(center_of_mass(self.bodies))
        self.average_velocity.append(average_velocity(self.bodies))
        self.average_distance_from_center.append(average_distance_from_center(self.bodies))
        self.lifetime += 1

    def plot(self):
        # plt.figure(figsize=(10, 5))
        # plt.plot([x[0] for x in self.center_of_mass], label="Center of mass x")
        # plt.plot([x[1] for x in self.center_of_mass], label="Center of mass y")
        # plt.title("Center of mass")
        # plt.legend()
        # plt.show()

        plt.figure(figsize=(10, 5))
        plt.plot(self.average_distance_from_center)
        plt.title("Average distance from center")
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.plot(self.average_velocity)
        plt.title("Average velocity")
        plt.show()

        plot_frequency(self.average_distance_from_center, "Average distance from center")
        plot_frequency(self.average_velocity, "Average velocity")


def plot_frequency(data, title):
    # Perform a Fast Fourier Transform on the data
    fft_data = fft(data)

    # Get the frequencies corresponding to the data
    frequencies = fftfreq(len(data))

    # Filter the frequencies and FFT data to include only those frequencies less than 0.1
    upper_mask = frequencies < 0.05
    lower_mask = frequencies > -0.05
    mask = upper_mask & lower_mask
    mask[0] = 0  # Exclude the DC component
    filtered_frequencies = frequencies[mask]
    filtered_fft_data = abs(fft_data)[mask]

    # Plot the filtered frequency spectrum
    plt.plot(filtered_frequencies, filtered_fft_data)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.show()
