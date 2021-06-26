#bin/usr/etc 
#Python 3.9.0
#Author Amshen Yesudas


#Importing Essentials
import cv2 as cv #OpenCv for reading,manupiulating and rendering the webcam images
from mediapipe.python.solutions import drawing_utils, holistic #ML models to idenfify our body parts
import math #to do some complex math operations
from ctypes import cast, POINTER 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume #To controll our vol

#Assigning the valuse
holi = holistic          #it will find identify where is your hands
drawings = drawing_utils #it help us to draw our hands
cam = cv.VideoCapture(0)  #Accessing your device default cam
drawing_spec_connector = drawings.DrawingSpec(color=(255,0,255), thickness=2, circle_radius=3) #dot connector line style
drawing_spec_dot = drawings.DrawingSpec(color=(0,255,255),thickness=2, circle_radius=5,)       #dot style



#The Engine Starts here
with holi.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistatic: #function for mapping our body parts

    while True:
        ret,frame = cam.read() #Reading our cam
        img = cv.cvtColor(frame,cv.COLOR_BGR2RGB) #converting the BGR image to RGB for mediapipe to identify the hands
        result = holistatic.process(img)          #this var will contain all the information about the image that we captured in line 21
        drawings.draw_landmarks(img,result.right_hand_landmarks,holi.HAND_CONNECTIONS,drawing_spec_dot,drawing_spec_connector)
                                                  #i am using my right hand to controll my pc vol you can choose what you like

        #drawings.draw_landmarks(img,result.left_hand_landmarks,holi.HAND_CONNECTIONS,drawing_spec_dot,drawing_spec_connector)
                                                  #code for using your left hand
                                                
                                                
        try:    #if we don't show our hand to the cam, there is a chance of  err
            x1,y1,z1 = result.right_hand_landmarks.landmark[4].x,result.right_hand_landmarks.landmark[4].y,result.right_hand_landmarks.landmark[4].z
                                                                                                     #Collecting the coordinates of our thumb finger

            x2,y2,z2 = result.right_hand_landmarks.landmark[8].x,result.right_hand_landmarks.landmark[8].y,result.right_hand_landmarks.landmark[8].z
                                                                                                    #Collecting the coordinates of our index finger
                                                                                                    
            imgH, imgW  = frame.shape           #Getting the height and width of our webcam screen
            x1Pos, y1Pos = int(imgW*x1), int(imgH*y1)   #Finding the real coordinates of our thumb
            x2Pos, y2Pos = int(imgW*x2), int(imgH*y2)   #Finding the real coordinates of our index finger
            cx,cy = int((x2Pos+x1Pos)/2) , int((y2Pos+y1Pos)/2) #Finding the the middle coordinates between the point thumb and index finger


            cv.circle(img,(x1Pos,y1Pos),5,(0,0,255),cv.FILLED)  #drawing a circle on the point of our thumb
            cv.circle(img,(x2Pos,y2Pos),5,(0,0,255),cv.FILLED)  #drawing a circle on the point of our index finger
            cv.line(img,(x1Pos,y1Pos),(x2Pos,y2Pos),(255,0,0),3)    #drawing a line connecting our index and thumb
            cv.circle(img,(cx,cy),8,(0,255,0), cv.FILLED)   #drawing a circle on the mid point of the line we have drawn before

            length = math.floor(math.hypot(x2Pos-x1Pos, y2Pos-y1Pos)) #finding the lenght between the point of thumb and index finger
            vol = math.floor((length/200)*60)   #Converting the length into the ratio of volume(00-65)

            devices = AudioUtilities.GetSpeakers()  #Identifying our audio device
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) #making it in our control(this script control)
            volume = cast(interface, POINTER(IAudioEndpointVolume)) #getting the volume property from the our audio devise
            currentVolumeDb = volume.GetMasterVolumeLevel() #getting our current vol

            try:
                if(vol>65):
                    volume.SetMasterVolumeLevel(0, None)    #setting the vol(max)
                else:

                    volume.SetMasterVolumeLevel(-70+vol, None)  #changing as per our fingers move
            except:
                pass
            

        except:
            pass

        img = cv.cvtColor(img,cv.COLOR_RGB2BGR) #converting the image back from RGB to BGR to render through out screen 
        cv.imshow("Amshen",img) #rendering our image

        key = cv.waitKey(1) #waiting for 1ms to check wether want to exit
        if key == ord('q'): #if we click the button "q" in our keyboad
            break               #if will break the loop and close the webcam widow

#Killing our Engine
cam.release()   #killing our cam 
cv.destroyAllWindows()  #Closing all the window opened by OpenCv
