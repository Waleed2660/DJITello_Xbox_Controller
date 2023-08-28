import pygame
from time import sleep
from djitellopy import tello
from pygame.constants import JOYBUTTONDOWN, JOYHATMOTION
from XboxController import ControllerButtons, suppress_stdout
import cv2


# For Testing
allowBroadcasting = False  # Set to False for testing


# initialize
pygame.init()
drone = tello.Tello()
print("Connecting to Tello...")
drone.connect()
drone.streamon()

print("Battery Level: " + str(drone.get_battery()))

joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    print("Controller => ", pygame.joystick.Joystick(i).get_name())
    joysticks[-1].init()


def reset_motion():
    drone.send_rc_control(0, 0, 0, 0)


def broadcast():
    if allowBroadcasting:
        # print("Broadcasting ........")
        raw_frame = drone.get_frame_read().frame

        # Display the frame
        frame = cv2.resize(raw_frame, (360,250))
        cv2.imshow('Tello Video Stream', frame)

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return 0

    return 1

# Main Loop
while True or KeyboardInterrupt:

    if broadcast() == 0:
        cv2.destroyAllWindows()
        break

    # Check for joystick events
    for event in pygame.event.get():

        if event.type == JOYBUTTONDOWN:
            
            print("++++++++++++++++++ Button --> ", event.button)
            
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
            

            elif event.axis in (4, 5):
                if event.axis == ControllerButtons.TRIGGERS.RIGHT.value:
                    print("going UP")
                    drone.send_rc_control(0, 0, 60, 0)
                    sleep(0.5)
                if event.axis == ControllerButtons.TRIGGERS.LEFT.value:
                    print("going DOWN")
                    drone.send_rc_control(0, 0, -60, 0)
                    sleep(0.5)
        

