import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

angle_grad = 45  # °
efficiency = 100  # %
wind_speed = 0  # m/s
g = 9.8  # m/s^2
x0, y0 = 0, 0  # starting point
q = 3800  # J/g
n = 10  # g/number
M = 100  # kg
m = 5  # kg

angle = angle_grad * math.pi / 180
initial_speed = math.sqrt((2 * efficiency * q * n) / (100 * m))
time_interval = (math.sin(angle) * initial_speed + math.sqrt((math.sin(angle) * initial_speed) ** 2 + 2 * g * y0)) / g

fig, ax = plt.subplots()
ax.axes.set_aspect("equal")

bullet_track, = ax.plot([], [], lw=2)
cannon_track, = ax.plot([], [], lw=2)

x_data, y_data = {"cannon": [], "bullet": []}, {"cannon": [], "bullet": []}


def update_track(t):
    x_bullet = x0 + (math.cos(angle) * initial_speed - wind_speed) * t
    y_bullet = y0 + math.sin(angle) * initial_speed * t - g * (t ** 2) / 2

    x_cannon = x0 - (math.cos(angle) * initial_speed * (m / M) + wind_speed) * t
    y_cannon = y0

    if x_bullet not in x_data["bullet"]:
        x_data["bullet"].append(x_bullet)
        y_data["bullet"].append(y_bullet)

        bullet_track.set_data(x_data["bullet"], y_data["bullet"])

    if x_cannon not in x_data["cannon"]:
        x_data["cannon"].append(x_cannon)
        y_data["cannon"].append(y_cannon)

        cannon_track.set_data(x_data["cannon"], y_data["cannon"])

    ax.relim()
    ax.autoscale_view(scalex=True, scaley=True)


plt.xlabel("x, m")
plt.ylabel("y, m")
plt.grid(True)

time = np.arange(0, time_interval, 0.1)
animation = FuncAnimation(fig, func=update_track, frames=time, interval=20, blit=False)

plt.show()
