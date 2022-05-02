import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

angle_grad = 45  # °
efficiency = 100  # %
wind_speed = 0  # m/s
g = 9.8  # m/s^2
x0, y0 = 0, 0  # starting point
q = 3800  # J/g
n = 10  # g/number
m = 5  # kg

angle = angle_grad * math.pi / 180
initial_speed = math.sqrt((2 * efficiency * q * n) / (100 * m))
time_interval = (math.sin(angle) * initial_speed + math.sqrt((math.sin(angle) * initial_speed) ** 2 + 2 * g * y0)) / g

fig, ax = plt.subplots()
ax.axes.set_aspect("equal")

# fig = plt.figure()
# ax = plt.axes(xlim=(-500, 5000), ylim=(-500, 1000))
track, = ax.plot([], [], lw=2)

x_data, y_data = [], []


def update_track(t):
    x = x0 + (math.cos(angle) * initial_speed - wind_speed) * t
    y = y0 + math.sin(angle) * initial_speed * t - g * (t ** 2) / 2

    if x not in x_data:
        x_data.append(x)
        y_data.append(y)
        track.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view(scalex=True, scaley=True)

    return track,


plt.xlabel("x, m")
plt.ylabel("y, m")
plt.grid(True)

time = np.arange(0, time_interval, 0.1)
animation = FuncAnimation(fig, func=update_track, frames=time, interval=20, blit=False)

plt.show()
