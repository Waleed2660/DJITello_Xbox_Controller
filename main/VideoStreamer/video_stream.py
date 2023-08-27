from djitellopy import tello
import cv2


print("Opencv: " + str(cv2.__version__))

# initialize
drone = tello.Tello()  
print("Connecting to Tello...")
drone.connect()


# print("Battery: " + str(drone.get_battery()))
print(" ================== STREAMING ======================= ")
# Stream
drone.streamon()


while(True):
    img = drone.get_frame_read().frame
    print("Frame from drone: " + str(img))
    cv2.imshow('Drone Footage', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
drone.release()
cv2.destroyAllWindows()