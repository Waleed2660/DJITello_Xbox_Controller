import pygame
from time import sleep
from djitellopy import tello
from pygame.constants import JOYBUTTONDOWN, JOYHATMOTION
from main.XboxController import ControllerButtons, suppress_stdout


pygame.init()
# initialize
drone = tello.Tello()
print("Connecting to Tello...")
drone.connect()

print("Battery Level: " + str(drone.get_battery()))

joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

# Print out the name of the controller
print("Controller => ", pygame.joystick.Joystick(0).get_name())


def reset_motion():
    drone.send_rc_control(0, 0, 0, 0)


# Main Loop
while True or KeyboardInterrupt:

    # Check for joystick events
    for event in pygame.event.get():

        # print("Event -------------------> ", event.type)

        if event.type == JOYBUTTONDOWN:
            if event.button == ControllerButtons.BUTTON.Y.value:
                print("Take Off")
                drone.takeoff()
                sleep(1.5)
                reset_motion()
            if event.button == ControllerButtons.BUTTON.A.value:
                print(" .. Landing .. ")
                reset_motion()
                drone.land()
                sleep(2.5)
            if event.button == ControllerButtons.BUTTON.X.value:
                print("Force Reset Motion")
                reset_motion()
                sleep(2)
            if event.button == ControllerButtons.BUTTON.B.value:
                print("Drone Height ==> ", drone.get_height())

            # Rotates the drone on horizontal axis
            if event.button == ControllerButtons.BUTTON.RB.value:
                print("turning RIGHT")
                drone.send_rc_control(0, 0, 0, 65)
            if event.button == ControllerButtons.BUTTON.LB.value:
                print("turning LEFT")
                drone.send_rc_control(0, 0, 0, -65)

        # Stunts
        if event.type == JOYHATMOTION:
            hat_x, hat_y = pygame.joystick.Joystick(0).get_hat(0)
            if hat_x == 1:
                print("Right button pressed")
                drone.flip_right()
                sleep(1.5)
            elif hat_x == -1:
                print("Left button pressed")
                drone.flip_left()
                sleep(1.5)
            elif hat_y == 1:
                print("Up button pressed")
                drone.flip_forward()
                sleep(1.5)
            elif hat_y == -1:
                print("Down button pressed")
                drone.flip_back()
                sleep(1.5)

        # Controls for Left Joystick
        if event.type == pygame.JOYAXISMOTION:
            if event.axis < 2:  # Left stick
                if event.axis == 0:  # left/right
                    if event.value < -0.999:
                        print("Yawing LEFT")
                        drone.send_rc_control(-55, 0, 0, 0)
                        sleep(0.01)
                        # reset_motion()

                    if event.value == 1.00:
                        print("Yawing RIGHT")
                        drone.send_rc_control(55, 0, 0, 0)
                        sleep(0.01)
                        # reset_motion()

                if event.axis == 1:  # up/down
                    if event.value < -0.999:
                        print("going FORWARD")
                        drone.send_rc_control(0, 50, 0, 0)
                        sleep(0.01)
                        # reset_motion()

                    if event.value == 1.00:
                        print("going BACKWARD")
                        drone.send_rc_control(0, -50, 0, 0)
                        sleep(0.01)
                        # reset_motion()

            if event.axis in (4, 5):
                if event.axis == ControllerButtons.TRIGGERS.RIGHT.value:
                    print("going DOWN")
                    drone.send_rc_control(0, 0, 60, 0)
                if event.axis == ControllerButtons.TRIGGERS.LEFT.value:
                    print("going UP")
                    drone.send_rc_control(0, 0, -60, 0)

