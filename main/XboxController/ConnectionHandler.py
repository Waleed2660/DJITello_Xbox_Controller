
# Allows Controller to be connected/disconnected while the Drone is flying
def ControllerConnectionHandler(pygame, joysticks, stick_event, controllerConnection):
    # Handles hot-plugging
    if stick_event.type == pygame.JOYDEVICEADDED and controllerConnection is not True:
        # This event will be generated when the program starts for every
        # joystick, filling up the list without needing to create them manually.
        joy = pygame.joystick.Joystick(stick_event.device_index)
        joysticks[joy.get_instance_id()] = joy
        print(f"Joystick {joy.get_instance_id()} connected")
        controllerConnection = True

    if stick_event.type == pygame.JOYDEVICEREMOVED and controllerConnection is True:
        del joysticks[stick_event.instance_id]
        print(f"Joystick {stick_event.instance_id} disconnected")
        controllerConnection = False

    return controllerConnection, joysticks
