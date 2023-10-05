import cv2
import numpy as np
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
from skimage import filters

root = tkinter.Tk()
root.filename =  filedialog.askopenfilename()#initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

print(''' 
                Cell Culture Well Area

    This software segmentates the selected area in a binary way
    and returns the percetage of area occupied by cells (dark)
    and by background (light). Built for culture cell applications.

    Intructions:
    - Click and drag the region of interest to be processed
    - (OPTIONAL) Hold 'Ctrl' while moving the mouse to vizualize the circle area filled
    - Release mouse button when the circle matches region of interest
    - Press 'ENTER' to proceed
    
    Please, select image...
      ''')

img_path = root.filename
root.destroy()

drawing = False # true if mouse is pressed
ix,iy = -1,-1
img = cv2.imread(img_path,0)

def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode,img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            radius = np.int32(np.hypot(ix-x, iy-y))
            img = cv2.imread(img_path,0)
            #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('image', 800,800)
            cv2.imshow('image',img)
            circle = cv2.circle(img,(x,y),radius,(0,0,255), thickness=2)
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        radius = np.int32(np.hypot(ix-x, iy-y))
        circle = cv2.circle(img,(x,y),radius,(0,0,255),-1)
    
    if flags == cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON:
        radius = np.int32(np.hypot(ix-x, iy-y))
        circle = cv2.circle(img,(x,y),radius,(0,0,255),-1)
        
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 800,800)

while(1):            
    cv2.imshow('image',img)
    #a, b, c, d = cv2.getWindowImageRect('image')
    circle = cv2.setMouseCallback('image',draw_circle)
    k = cv2.waitKey(1) & 0xFF
    #if k == 13:
     #   fill = not fill
    #if k == ord('m'):
        #mode = not mode
    if k == 13:
        #out = img 
        break

cv2.destroyAllWindows()

mask = img == 0

coord = np.where(mask==True)

c0 = coord[0]
c1 = coord[1]
sin = np.unique(c0)
cos = np.unique(c1)

top = np.min(sin)
bottom = np.max(sin)+1
left = np.min(cos)
right = np.max(cos)+1

img = cv2.imread(img_path,0)

#rcenter = np.int32(np.mean(sin))
#ccenter = np.int32(np.mean(cos))
#radius = np.int32(np.max(cos) - np.min(cos))//2

thres = filters.threshold_mean(img)
raw_binary = img > thres

#img_cp = img.copy()

#img_cp[mask==False] = 255 
roi_img = img[top:bottom, left:right]
raw_binary[mask==False] = 255 
roi_bin = raw_binary[top:bottom, left:right]

cell = img[mask==True] < thres
bg = img[mask==True] > thres

total = np.bincount(mask.ravel())[1]
cell = np.bincount(cell)[1]
bg = np.bincount(bg)[1]

cell_p = cell/total * 100
bg_p = bg/total * 100

print('''
    Results:
    
    Percetage of area occupied by
    
    cells      = {} %
    background = {} %

    '''.format(np.round(cell_p,3), np.round(bg_p,3)))

res_visualize = np.hstack((roi_img,roi_bin*255))

plt.imshow(res_visualize, cmap='gray'); plt.show()