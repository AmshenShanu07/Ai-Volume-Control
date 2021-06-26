import cv2 as cv
from mediapipe.python.solutions import drawing_utils, holistic
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

drawings = drawing_utils
holi = holistic
cam = cv.VideoCapture(0)
drawing_spec_face = drawings.DrawingSpec(color=(255,0,255), thickness=1, circle_radius=3)
drawing_spec_hand = drawings.DrawingSpec(color=(0,255,255),thickness=2, circle_radius=5,)

with holi.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistatic:

    while True:
        ret,frame = cam.read()
        img = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        result = holistatic.process(img)
        drawings.draw_landmarks(img,result.right_hand_landmarks,holi.HAND_CONNECTIONS,drawing_spec_hand)
        drawings.draw_landmarks(img,result.left_hand_landmarks,holi.HAND_CONNECTIONS,drawing_spec_hand)
        try:
            x1,y1,z1 = result.right_hand_landmarks.landmark[4].x,result.right_hand_landmarks.landmark[4].y,result.right_hand_landmarks.landmark[4].z
            x2,y2,z2 = result.right_hand_landmarks.landmark[8].x,result.right_hand_landmarks.landmark[8].y,result.right_hand_landmarks.landmark[8].z
            imgH, imgW, imgC = frame.shape
            x1Pos, y1Pos = int(imgW*x1), int(imgH*y1)
            x2Pos, y2Pos = int(imgW*x2), int(imgH*y2)
            cx,cy = int((x2Pos+x1Pos)/2) , int((y2Pos+y1Pos)/2)


            cv.circle(img,(x1Pos,y1Pos),5,(0,0,255),cv.FILLED)
            cv.circle(img,(x2Pos,y2Pos),5,(0,0,255),cv.FILLED)
            cv.line(img,(x1Pos,y1Pos),(x2Pos,y2Pos),(255,0,0),3)
            cv.circle(img,(cx,cy),8,(0,255,0), cv.FILLED)

            length = math.floor(math.hypot(x2Pos-x1Pos, y2Pos-y1Pos))
            vol = math.floor((length/100)*60)
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            currentVolumeDb = volume.GetMasterVolumeLevel()
            try:
                if(vol>65):
                    volume.SetMasterVolumeLevel(0, None)
                else:

                    volume.SetMasterVolumeLevel(-70+vol, None)
            except:
                pass
            

        except:
            pass
        img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
        key = cv.waitKey(1)
        if key == ord('q'):
            break

cam.release()
cv.destroyAllWindows()
