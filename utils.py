import colorsys
from random import random, gauss
import math
from constants import *
import numpy as np


def evaluate_periodicity(signal, freq_band, threshold_ratio=0.1, penalty_weight=1.0):
    # Compute the Fourier Transform
    fft_result = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal))

    # Get the power spectrum
    power_spectrum = np.abs(fft_result) ** 2

    # Exclude the DC component (frequency 0)
    freqs = freqs[1:]
    power_spectrum = power_spectrum[1:]

    # Filter frequencies to those in the desired band
    band_mask = (freqs >= freq_band[0]) & (freqs <= freq_band[1])
    band_freqs = freqs[band_mask]
    band_powers = power_spectrum[band_mask]

    # Determine the threshold for significant frequencies
    max_power = np.max(band_powers)
    threshold = threshold_ratio * max_power

    # Count significant frequencies within the band
    significant_freqs_count = np.sum(band_powers > threshold)

    # The score could be inversely proportional to the number of significant frequencies
    score = 1.0 / significant_freqs_count if significant_freqs_count > 0 else float('inf')

    # Apply penalty for frequencies outside the band
    total_power = np.sum(power_spectrum)
    band_power = np.sum(band_powers)
    penalty = penalty_weight * (total_power - band_power) / total_power

    return score - penalty


def random_color():
    hue = random()
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def random_centered():
    while True:
        # Generate a random number from a normal distribution
        # with mean 0.5 and standard deviation
        value = gauss(0.5, 0.1)

        # Clamp the value between 0 and 1
        value = max(0., min(1., value))

        # Reject values that are exactly 0 or 1 to ensure they're never returned
        if 0 < value < 1:
            return value


def rough_escape_velocity(masses):
    mass = sum(masses) - max(masses)
    return math.sqrt(2 * gravitational_constant * mass / max_x / 2)


def has_escaped(simulation):
    for body in simulation.bodies:
        velocity = math.sqrt(body.vx ** 2 + body.vy ** 2)
        if body.x < 0 or body.x > max_x or body.y < 0 or body.y > max_y:
            # if velocity > simulation.escape_velocity:
            return True
    return False
