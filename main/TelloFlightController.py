import sys
import pygame
from time import sleep
from djitellopy import tello
from pygame.constants import JOYBUTTONDOWN, JOYHATMOTION
from main.XboxController import ControllerButtons

# initialize
pygame.init()
drone = tello.Tello()
print("Connecting to Tello...")
drone.connect()
drone.set_speed(70)
print("Battery Level: " + str(drone.get_battery()))
joysticks = []


def connectXboxController():
    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        # Print out the name of the controller
        print("Controller => ", pygame.joystick.Joystick(i).get_name())
        joysticks[-1].init()


def reset_motion():
    drone.send_rc_control(0, 0, 0, 0)


def fly(droneXSpeed):
    try:
        while True:
            # Check for joystick events
            for event in pygame.event.get():
                if event.type == JOYBUTTONDOWN:
                    print("BUTTON ---> ", event.button)
                    if event.button == ControllerButtons.BUTTON.Y.value:
                        print("Take Off")
                        drone.takeoff()
                        sleep(1)
                        reset_motion()
                    if event.button == ControllerButtons.BUTTON.A.value:
                        print(" .. Landing .. ")
                        drone.land()
                        sleep(1)
                    if event.button == ControllerButtons.BUTTON.X.value:
                        print("Force Reset Motion")
                        reset_motion()
                        sleep(0.01)
                    if event.button == ControllerButtons.BUTTON.B.value:
                        print("Drone Height ==> ", drone.get_height())
                        print("Speed => ", drone.get_speed_x())

                    # Rotates the drone on horizontal axis
                    if event.button == ControllerButtons.BUTTON.RB.value:
                        print("turning RIGHT")
                        drone.send_rc_control(0, 0, 0, 65)
                        sleep(0.01)
                    if event.button == ControllerButtons.BUTTON.LB.value:
                        print("turning LEFT")
                        drone.send_rc_control(0, 0, 0, -65)
                        sleep(0.01)

                    if event.button == ControllerButtons.BUTTON.MID_RIGHT.value:
                        if droneXSpeed < 80:
                            droneXSpeed += 20
                            print("Increased Speed to => ", droneXSpeed)
                            drone.set_speed(droneXSpeed)
                    if event.button == ControllerButtons.BUTTON.MID_LEFT.value:
                        if droneXSpeed > 39:
                            droneXSpeed -= 20
                            print("Decreased Speed to => ", droneXSpeed)
                            drone.set_speed(droneXSpeed)
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
                        # left/right
                        if event.axis == 0:
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
                    # Controls for altitude
                    if event.axis in (4, 5):
                        if event.axis == ControllerButtons.TRIGGERS.RIGHT.value:
                            print("going DOWN")
                            drone.send_rc_control(0, 0, 60, 0)
                            sleep(0.01)
                        if event.axis == ControllerButtons.TRIGGERS.LEFT.value:
                            print("going UP")
                            drone.send_rc_control(0, 0, -60, 0)
                            sleep(0.01)

    except KeyboardInterrupt or Exception:
        print("MAY DAY MAY DAY .....")
        drone.land()
        return


if __name__ == "__main__":
    xSpeed = 5
    connectXboxController()
    fly(xSpeed)
    sys.exit(1)
