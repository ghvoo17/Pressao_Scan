import numpy as np
import cv2 as cv



cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

 
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    print(frame.shape)

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

   # cv.Canny(frame, )
    
    # Exibe a janela com a camera do notebook
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()