from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 3

        # Initial random destination
        self.dest_x = random.randint(0, 300)
        self.dest_y = random.randint(0, 300)

        # Frame counter (used to change direction over time)
        self.frame_count = 0
        self.change_interval = 40  # 2 seconds (40 frames)

    def update(self):
        # Increase frame counter
        self.frame_count += 1

        # Change destination every 2 seconds
        if self.frame_count >= self.change_interval:
            self.dest_x = random.randint(0, 300)
            self.dest_y = random.randint(0, 300)
            self.frame_count = 0

        # Direction vector toward destination
        dx = self.dest_x - self.x
        dy = self.dest_y - self.y

        distance = sqrt(dx**2 + dy**2)

        if distance == 0:
            return

        # Normalize direction
        dx /= distance
        dy /= distance

        # Move target
        self.x += dx * self.speed
        self.y += dy * self.speed


class Rocket:
    def __init__(self, x, y, speed=0, acceleration=0.15, max_speed=2.8):
        # Position
        self.x = x
        self.y = y

        # Motion parameters
        self.speed = speed
        self.acceleration = acceleration
        self.max_speed = max_speed

        # Flight phase
        self.phase = "boost"
        self.boost_height = 50
        self.start_y = y

    def update(self, target):
        # Accelerate until reaching max speed
        if self.speed < self.max_speed:
            self.speed += self.acceleration
            if self.speed > self.max_speed:
                self.speed = self.max_speed

        # Boost phase (vertical launch)
        if self.phase == "boost":
            self.y += self.speed

            # Check if boost phase is complete
            if self.y >= self.start_y + self.boost_height:
                self.phase = "guidance"

            return False

        # Calculate distance to target
        dx = target.x - self.x
        dy = target.y - self.y
        distance = sqrt(dx**2 + dy**2)

        # Check if rocket reached the target
        if distance < self.speed:
            self.x = target.x
            self.y = target.y
            return True

        # Normalize direction
        dx /= distance
        dy /= distance

        # Move rocket toward target
        self.x += dx * self.speed
        self.y += dy * self.speed

        return False


target = Target(250, 200)
rocket = Rocket(25, 0)

fig, ax = plt.subplots(figsize=(10, 7))

# Set plot limits
ax.set_xlim(0, 300)
ax.set_ylim(0, 300)

# Visual elements
rocket_dot, = ax.plot([], [], 'b^', label="Rocket")
target_dot, = ax.plot(target.x, target.y, 'ro', label="Target")
trajectory_line, = ax.plot([], [], '--', label="Trajectory")

ax.legend()
ax.grid()

# Lists to store rocket trajectory
rocket_x = []
rocket_y = []


def update(frame):
    global rocket_x, rocket_y

    # Save current rocket position
    rocket_x.append(rocket.x)
    rocket_y.append(rocket.y)

    # Update target movement
    target.update()

    # Update rocket movement
    hit = rocket.update(target)

    # Update visual elements
    rocket_dot.set_data([rocket.x], [rocket.y])
    trajectory_line.set_data(rocket_x, rocket_y)
    target_dot.set_data([target.x], [target.y])

    # Stop animation if target is hit
    if hit:
        print("🎯 Target hit!")
        ani.event_source.stop()

    return rocket_dot, trajectory_line


ani = FuncAnimation(fig, update, frames=200, interval=16)

plt.title("Rocket Simulation")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
