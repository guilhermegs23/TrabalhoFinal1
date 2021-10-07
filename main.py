import sys
import pygame
from pygame.locals import *
from simulation import Simulation
from drone import Drone


def interpolate(x, x_min, x_max, y_min, y_max):
    return ((x - x_min) / (x_max - x_min) * (y_max - y_min)) + y_min


screen_width_px = 900
screen_height_px = 800

screen_width_m = 60.0
screen_height_m = 50.0

step = 0.005

increment = 5.0

init_pos_m = [screen_width_m / 2.0, screen_height_m / 2.0]

init_x_px = interpolate(init_pos_m[0], 0, screen_width_m, 0, screen_width_px)

init_y_px = interpolate(init_pos_m[1], 0, screen_height_m, 0, screen_height_px)
init_y_px = screen_height_px - init_y_px

waypoints = [[30.0, 20.0], [45.0, 20.0], [8.0, 5.0], [30.0, 45.0], [30.0, 20.0]]

# sim = Simulation(step_sim=step, init_pos=init_pos_m, init_waypoint=init_pos_m)
sim = Simulation(step_sim=step, init_pos=init_pos_m, init_waypoint=None, init_trajectory=waypoints)
drone = Drone(image_path='drone.png', init_pos=(init_x_px, init_y_px))

pygame.init()
pygame.display.set_caption('Drone Simulator')
bg_image = pygame.image.load('images/sky.jpg')
screen = pygame.display.set_mode((screen_width_px, screen_height_px))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                waypoint_x = sim.get_waypoint_x() + increment
                waypoint_x = max(0.0, min(waypoint_x, screen_width_m))
                sim.set_waypoint_x(waypoint_x)
            elif event.key == K_LEFT:
                waypoint_x = sim.get_waypoint_x() - increment
                waypoint_x = max(0.0, min(waypoint_x, screen_width_m))
                sim.set_waypoint_x(waypoint_x)
            elif event.key == K_UP:
                waypoint_y = sim.get_waypoint_y() + increment
                waypoint_y = max(0.0, min(waypoint_y, screen_height_m))
                sim.set_waypoint_y(waypoint_y)
            elif event.key == K_DOWN:
                waypoint_y = sim.get_waypoint_y() - increment
                waypoint_y = max(0.0, min(waypoint_y, screen_height_m))
                sim.set_waypoint_y(waypoint_y)

    pos_m, angle = sim.iterate()

    x_px = interpolate(pos_m[0], 0, screen_width_m, 0, screen_width_px)

    y_px = interpolate(pos_m[1], 0, screen_height_m, 0, screen_height_px)
    y_px = screen_height_px - y_px

    drone.update(int(x_px), int(y_px), angle)

    screen.blit(bg_image, (0, 0))
    drone.draw(screen)

    pygame.display.update()

    clock.tick(1 / step)
