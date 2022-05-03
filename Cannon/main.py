import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox

show_prev_track = False
angle_grad = 45  # °
efficiency = 100  # %
wind_speed = 0  # m/s
g = 9.8  # m/s^2
x0, y0 = 0, 0  # starting point
q = 3800  # J/g
n = 10  # g/number
M = 100  # kg
m = 5  # kg

fig = plt.figure()
gs = GridSpec(ncols=3, nrows=8, figure=fig)

ax = plt.subplot(gs[:8, 1:])
ax.set_aspect("equal")

x_prev_data, y_prev_data = [], []

plt.xlabel("x, m")
plt.ylabel("y, m")
plt.grid(True)

axButton_launch = plt.subplot(gs[0, 0])
button_launch = Button(ax=axButton_launch, label="Launch")


def launch(event):
    global x_prev_data, y_prev_data

    def clear_track():
        for line in ax.get_lines():
            line.remove()

        if show_prev_track:
            ax.plot(x_prev_data, y_prev_data, "--", lw=2)

    angle = angle_grad * math.pi / 180
    initial_speed = math.sqrt((2 * efficiency * q * n) / (100 * m))
    time_interval = (math.sin(angle) * initial_speed + math.sqrt(
        (math.sin(angle) * initial_speed) ** 2 + 2 * g * y0)) / g

    clear_track()

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

    x_prev_data = x_data["bullet"]
    y_prev_data = y_data["bullet"]

    time = np.arange(0, time_interval, 0.1)
    FuncAnimation(fig, func=update_track, frames=time, interval=20, blit=False)


button_launch.on_clicked(launch)

axSlider_gunpowder = plt.subplot(gs[1, 0])
slider_gunpowder = Slider(ax=axSlider_gunpowder, label="Gunpowder", valmin=10, valmax=100, valstep=10)

axSlider_efficiency = plt.subplot(gs[2, 0])
slider_efficiency = Slider(ax=axSlider_efficiency, label="Efficiency", valmin=1, valmax=100, valstep=1)

axSlider_wind = plt.subplot(gs[3, 0])
slider_wind = Slider(ax=axSlider_wind, label="Wind speed", valmin=0, valmax=20, valstep=1)

axTextBox_s_point = plt.subplot(gs[4, 0])
textbox_s_point = TextBox(ax=axTextBox_s_point, label="Starting point", textalignment="center")

axTextBox_cannon_w = plt.subplot(gs[5, 0])
textbox_cannon_w = TextBox(ax=axTextBox_cannon_w, label="Cannon weight", textalignment="center")

axTextBox_bullet_w = plt.subplot(gs[6, 0])
textbox_bullet_w = TextBox(ax=axTextBox_bullet_w, label="Bullet weight", textalignment="center")

plt.show()
