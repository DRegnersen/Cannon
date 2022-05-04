import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox
from tkinter import messagebox as mbox

show_prev_track = True
angle_grad = 45  # °
efficiency = 100  # %
gunpowder = 10  # g/number
g = 9.8  # m/s^2
x0, y0 = 0, 0  # starting point
q = 3800  # J/g
M = 100  # kg
m = 5  # kg

angle = 0
initial_speed = 0
time_interval = 0
x_offset = 0
y_offset = 0

x_prev_data, y_prev_data = [], []

fig = plt.figure()
gs = GridSpec(ncols=4, nrows=8, figure=fig)

ax = plt.subplot(gs[:7, 2:])
ax.set_aspect("equal")

plt.xlabel("x, m")
plt.ylabel("y, m")
plt.grid(True)

axButton_launch = plt.subplot(gs[0, :2])
button_launch = Button(ax=axButton_launch, label="Launch")


def clear_track():
    global x_prev_data, y_prev_data

    for line in ax.get_lines():
        line.remove()

    if show_prev_track:
        ax.plot(x_prev_data, y_prev_data, "--", lw=2)


def update_config():
    global angle, initial_speed, time_interval, x_offset, y_offset

    angle = angle_grad * np.pi / 180
    initial_speed = np.sqrt((2 * efficiency * q * gunpowder) / (100 * m))
    time_interval = (np.sin(angle) * initial_speed + np.sqrt(
        (np.sin(angle) * initial_speed) ** 2 + 2 * g * y0)) / g
    x_offset = x0
    y_offset = y0

    return np.arange(0, time_interval, 0.1)


def run_animation():
    global x_prev_data, y_prev_data

    def update_track(t):
        x_bullet = x_offset + (np.cos(angle) * initial_speed) * t
        y_bullet = y_offset + np.sin(angle) * initial_speed * t - g * (t ** 2) / 2

        x_cannon = x_offset - (np.cos(angle) * initial_speed * (m / M)) * t
        y_cannon = y_offset

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

    bullet_track, = ax.plot([], [], lw=2)
    cannon_track, = ax.plot([], [], lw=2)

    x_data, y_data = {"cannon": [], "bullet": []}, {"cannon": [], "bullet": []}

    x_prev_data = x_data["bullet"]
    y_prev_data = y_data["bullet"]

    FuncAnimation(fig, func=update_track, frames=update_config(), interval=20, blit=False)


def launch(event):
    clear_track()
    run_animation()


button_launch.on_clicked(launch)

axSlider_angle = plt.subplot(gs[1, :2])
slider_angle = Slider(ax=axSlider_angle, label="Angle", valmin=1, valmax=89, valinit=45, valstep=1)


def update_angle(val):
    global angle_grad
    angle_grad = slider_angle.val


slider_angle.on_changed(update_angle)

axSlider_gunpowder = plt.subplot(gs[2, :2])
slider_gunpowder = Slider(ax=axSlider_gunpowder, label="Gunpowder", valmin=10, valmax=100, valstep=10)


def update_gunpowder(val):
    global gunpowder
    gunpowder = slider_gunpowder.val


slider_gunpowder.on_changed(update_gunpowder)

axSlider_efficiency = plt.subplot(gs[3, :2])
slider_efficiency = Slider(ax=axSlider_efficiency, label="Efficiency", valmin=1, valmax=100, valstep=1, valinit=100)


def update_efficiency(val):
    global efficiency
    efficiency = slider_efficiency.val


slider_efficiency.on_changed(update_efficiency)

axTextBox_x_start = plt.subplot(gs[4, 0])
axTextBox_x_start.set_title("X coordinate of the starting point")

textbox_x_start = TextBox(ax=axTextBox_x_start, label="X", initial="0", textalignment="center")


def update_x0(label):
    global x0

    if not (label.isdigit()):
        mbox.showerror("Cannon Setup", "Incorrect measure format")
        return

    x0 = int(label)


textbox_x_start.on_submit(update_x0)

axTextBox_y_start = plt.subplot(gs[4, 1])
axTextBox_y_start.set_title("Y coordinate of the starting point")

textbox_y_start = TextBox(ax=axTextBox_y_start, label="Y", initial="0", textalignment="center")


def update_y0(label):
    global y0

    if not (label.isdigit()):
        mbox.showerror("Cannon Setup", "Incorrect measure format")
        return

    y0 = int(label)


textbox_y_start.on_submit(update_y0)

axTextBox_bullet_m = plt.subplot(gs[5, :2])
axTextBox_bullet_m.set_title("Cannonball mass:")

textbox_bullet_m = TextBox(ax=axTextBox_bullet_m, label="m", initial="5", textalignment="center")


def update_bullet_m(label):
    global m

    if not (label.isdigit()):
        mbox.showerror("Cannon Setup", "Incorrect measure format")
        return

    m = int(label)


textbox_bullet_m.on_submit(update_bullet_m)

axTextBox_cannon_m = plt.subplot(gs[6, :2])
axTextBox_cannon_m.set_title("Cannon mass:")

textbox_cannon_m = TextBox(ax=axTextBox_cannon_m, label="M", initial="100", textalignment="center")


def update_cannon_m(label):
    global M

    if not (label.isdigit()):
        mbox.showerror("Cannon Setup", "Incorrect measure format")
        return

    M = int(label)


textbox_cannon_m.on_submit(update_cannon_m)

plt.show()
