from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import time

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 25

        # Initial random destination
        self.dest_x = random.randint(0, 1000)
        self.dest_y = random.randint(0, 1000)

        # Frame counter (used to change direction over time)
        self.frame_count = 0
        self.change_interval = 30  # 2 seconds (40 frames)

    def update(self):
        # Increase frame counter
        self.frame_count += 1

        # Change destination every 2 seconds
        if self.frame_count >= self.change_interval:
            self.dest_x = random.randint(0, 1000)
            self.dest_y = random.randint(0, 1000)
            self.frame_count = 0

        # Direction vector toward destination
        dx = self.dest_x - self.x
        dy = self.dest_y - self.y

        distance = sqrt(dx**2 + dy**2)

        if distance == 0:
            return
        
        if distance < self.speed:
            self.x = self.dest_x
            self.y = self.dest_y
            return

        # Normalize direction
        dx /= distance
        dy /= distance

        # Move target
        self.x += dx * self.speed
        self.y += dy * self.speed


class Rocket:
    def __init__(self, x, y, speed=0, acceleration=0.25, max_speed=20):
        # Position
        self.x = x
        self.y = y

        # Real speed
        self.vx = 0
        self.vy = 0

        # Motion parameters
        self.acceleration = acceleration
        self.max_speed = max_speed

        # Flight phase
        self.phase = "boost"
        self.boost_height = 80
        self.start_y = y

        # Fuel simulator
        self.fuel = 200

        # Gravity
        self.gravity_acceleration = 0.6

        # curve smoothing
        self.turn_rate = 0.7

        self.pause_frames = 0.2
        self.pause_counter = 0

    def update(self, target):
        # -----------------------------------
        # PHASE 1 | BOOST
        # -----------------------------------

        if self.phase == "boost":
            if self.fuel > 0:   
                self.vy += self.acceleration
                if self.vy > self.max_speed:
                    self.vy = self.max_speed
                self.fuel -= 1

            self.y += self.vy

            if self.y >= self.start_y + self.boost_height:
                self.vy = 0
                self.phase = "pause"

            return False
        

        # -----------------------------------
        # PHASE 2 | PAUSE
        # -----------------------------------
        if self.phase == "pause":
            self.pause_counter += 1

            # Apply gravity
            self.vy -= self.gravity_acceleration
            self.y += self.vy

            if self.y < self.start_y + self.boost_height:
                self.y = self.start_y + self.boost_height
                self.vy = 0

            if self.pause_counter >= self.pause_frames:
                self.phase = "guidance"

            return False
        

        # -----------------------------------
        # PHASE 2 | GUIDANCE
        # -----------------------------------
        dx = target.x - self.x
        dy = target.y - self.y
        distance = sqrt(dx**2 + dy**2)

        # Check if rocket reached the target
        if distance < 6:
            self.x = target.x
            self.y = target.y
            return True
        if distance != 0:
            dir_x = dx / distance
            dir_y = dy / distance
        else:
            dir_x = 0
            dir_y = 0

        if self.fuel > 0:
            desired_vx = dir_x * self.max_speed
            desired_vy = dir_y * self.max_speed

            # Smooth
            self.vx += (desired_vx - self.vx) * self.turn_rate
            self.vy += (desired_vy - self.vy) * self.turn_rate

            self.fuel -= 1


        self.vy -= self.gravity_acceleration


        # Update position
        self.x += self.vx
        self.y += self.vy

        return False

target = Target(250, 200)
rocket = Rocket(25, 0)

fig, ax = plt.subplots(figsize=(16, 10))

# Set plot limits
ax.set_xlim(0, 1000)
ax.set_ylim(0, 1000)

# Visual elements
rocket_dot, = ax.plot([], [], 'b^', label="Rocket")
target_dot, = ax.plot(target.x, target.y, 'ro', label="Target")
trajectory_line, = ax.plot([], [], '--', label="Trajectory")

ax.legend()
ax.grid()

# HUD text
info_text = ax.text(
    0.02, 0.95, "",
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment='top',
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

# Lists to store rocket trajectory
rocket_x = []
rocket_y = []

# time
start_time = time.time()

def update(frame):
    global rocket_x, rocket_y

    # Save current rocket position
    rocket_x.append(rocket.x)
    rocket_y.append(rocket.y)

    current_time = time.time()
    elapsed_time = current_time - start_time

    # Update target movement
    target.update()
    
    # Update rocket movement
    hit = rocket.update(target)

    # Update visual elements
    rocket_dot.set_data([rocket.x], [rocket.y])
    trajectory_line.set_data(rocket_x, rocket_y)
    target_dot.set_data([target.x], [target.y])

    # Distance between rocket and target
    dx = target.x - rocket.x
    dy = target.y - rocket.y
    distance = sqrt(dx**2 + dy**2)

    # Total speed
    total_speed = sqrt(rocket.vx**2 + rocket.vy**2)

    # Pause phase
    pause_remaining = ""
    if rocket.phase == "pause":
        frames_left = rocket.pause_frames - rocket.pause_counter
        seconds_left = frames_left / 60
        pause_remaining = f"\nLançando em: {seconds_left:.1f}s"

    info_text.set_text(
        f"Rocket X: {rocket.x:.1f}\n"
        f"Rocket Y: {rocket.y:.1f}\n"
        f"Distance: {distance:.2f}\n"
        f"Phase: {rocket.phase}{pause_remaining}\n"
        f"Fuel: {rocket.fuel}\n"
        "\n"
        f"Speed vy: {rocket.vy:.2f}\n"
        f"Speed vx: {rocket.vx:.2f}\n"
        f"Total Speed: {total_speed:.2f}\n"
        f"Time: {elapsed_time:.2f}s\n"

    )

    # Stop animation if target is hit
    if hit:
        print("Target hit!")
        ani.event_source.stop()

    return rocket_dot, trajectory_line


ani = FuncAnimation(fig, update, frames=200, interval=16)

plt.title("Missile Simulation")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
