import cv2
import numpy as np 

# img = cv2.imread('Litten.png',0)
# cv2.imshow('image',img)


rows=500
cols=512
frame=0.0*np.ones((rows,cols,3));
frametxt=frame.copy()

cv2.putText(frame,"fooo", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.imshow("Audio Spectrogram, filter: f, sampling: s, quit:q",frame+frametxt)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.imwrite('littengray.png',img)
#     cv2.destroyAllWindows()