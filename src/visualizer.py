from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self):
        self.visualization_keywords = [
            "graph",
            "plot",
            "chart",
            "diagram",
            "spectrum",
            "frequency",
            "signal",
            "power",
            "modulation",
            "bandwidth",
            "throughput",
        ]

    def should_visualize(self, query: str, response: str) -> bool:
        # Check if any visualization keywords are in the query or response
        return any(
            keyword in query.lower() or keyword in response.lower()
            for keyword in self.visualization_keywords
        )

    def create_visualization(
        self, query: str, response: str
    ) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(10, 6))

        if "spectrum" in query.lower() or "frequency" in query.lower():
            self._create_spectrum_plot(ax)
        elif "signal" in query.lower():
            self._create_signal_plot(ax)
        elif "modulation" in query.lower():
            self._create_modulation_plot(ax)
        else:
            self._create_generic_plot(ax)

        return fig, ax

    def _create_spectrum_plot(self, ax):
        frequencies = np.linspace(0, 10, 1000)
        power = np.exp(-0.5 * (frequencies - 5) ** 2) + 0.1 * np.random.random(1000)
        ax.plot(frequencies, power)
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Power (dBm)")
        ax.set_title("Frequency Spectrum")

    def _create_signal_plot(self, ax):
        t = np.linspace(0, 1, 1000)
        signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)
        ax.plot(t, signal)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title("Signal Waveform")

    def _create_modulation_plot(self, ax):
        t = np.linspace(0, 1, 1000)
        carrier = np.sin(2 * np.pi * 50 * t)
        message = np.sin(2 * np.pi * 5 * t)
        modulated = carrier * (1 + 0.5 * message)
        ax.plot(t, modulated)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title("Amplitude Modulated Signal")

    def _create_generic_plot(self, ax):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y)
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_title("Generic Plot")
