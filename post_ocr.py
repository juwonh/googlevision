import os
import cv2
import numpy as np
from PIL import Image

def read_bbox(image_file):
  """ Reads bbox txt file associated with image file and returns bbox and text list 
  Args: 
    image_file (str): image file name
  Return:
     box (int list): [x1,y1,x2,y2,x3,y3,x4,y4] image coordinates clockwise from upper left corner
     txt (str list): text[i] = text content for each bbox corresponding to box[i]
  """
  folder = os.path.dirname(image_file)
  filename, _ = os.path.splitext(os.path.basename(image_file))
  txt_file = folder + '/' + filename + '.txt'
  
  with open(txt_file, 'r', encoding='utf-8') as f:
    lines = [l for l in f]   
  
  box = []
  txt = []

  for i, line in enumerate(lines):
    l = line.split('\t')
    box.append([int(l[1]),int(l[2]),int(l[3]),int(l[4]),int(l[5]),int(l[6]),int(l[7]),int(l[8])])
    txt.append(l[9].split('\n')[0])

  return box, txt

def draw_bbox(image_file, boxes):
  """ draw box on the image_file and writes res_image_file """
  folder = os.path.dirname(image_file)
  filename, _ = os.path.splitext(os.path.basename(image_file))

  res_image_file = folder + '/' + filename + '_res.jpg'
  img = Image.open(image_file)
  img_array = np.array(img)
  b = img_array[:,:,0]
  g = img_array[:,:,1]
  r = img_array[:,:,2]
  corrected_img = np.dstack((r, g, b)) 

  for i, box in enumerate(boxes):
    print(box)
    pts = np.array([[box[0],box[1]],[box[2],box[3]],[box[4],box[5]],[box[6],box[7]]],np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(corrected_img, [pts], True, color=(0,0,255), thickness=2)
  
  cv2.imwrite(res_image_file, corrected_img)
  # cv2.imshow('Rectangle using polylines', corrected_img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()


## 
def treat_symbols(boxes, txt):
  newbox = []
  newtxt = []
  height = []
  count = 0
  
  for i, box in enumerate(boxes):
    if i == 0:
      xmin0 = box[0] if box[0] < box[6] else box[6]
      xmax0 = box[2] if box[2] > box[4] else box[4]
      ymin0 = box[1] if box[1] < box[3] else box[3]
      ymax0 = box[5] if box[5] > box[7] else box[7]
      h0 = ymax0 - ymin0
      box0 = box
      txt0 = txt[i]
      
    else:
      xmin1 = box[0] if box[0] < box[6] else box[6]
      xmax1 = box[2] if box[2] > box[4] else box[4]
      ymin1 = box[1] if box[1] < box[3] else box[3]
      ymax1 = box[5] if box[5] > box[7] else box[7]
      h1 = ymax1 - ymin1
      th = h1*0.1
      
      if abs(ymin0-ymin1) < th and abs(ymax0-ymax1) < th and (xmin1-xmax0) < th*0.75:
        # print("{}{}".format(txt[i-1], txt[i]))
        count += 1
        
      else:
        newbox.append(box0)
        newtxt.append(txt0)
      xmin0 = xmin1
      xmax0 = xmax1
      ymin0 = ymin1
      ymax0 = ymax1
  print(count)











  #   h = box[5] - box[3]
  #   height.append(h)
  # # print(height)


  return newbox, newtxt
    


# imagefile = './data/sign.png'
imagefile = './data/e2.jpg'

box, txt = read_bbox(imagefile)
# print(box[0])
# print(txt[0])

newbox, newtxt = treat_symbols(box, txt)

# draw_bbox(imagefile, box)

# 