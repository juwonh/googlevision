import os
import cv2
import numpy as np
from PIL import Image

def read_bbox(image_file, txt_file):
  """ Reads bbox txt file associated with image file and returns bbox and text list 
  Args: 
    image_file (str): image file name
  Return:
     box (int list): [x1,y1,x2,y2,x3,y3,x4,y4] image coordinates clockwise from upper left corner
     txt (str list): text[i] = text content for each bbox corresponding to box[i]
  """

  with open(txt_file, 'r', encoding='utf-8') as f:
    lines = [l for l in f]   
  
  box = []
  txt = []

  for i, line in enumerate(lines):
    l = line.split('\t')
    box.append([int(l[1]),int(l[2]),int(l[3]),int(l[4]),int(l[5]),int(l[6]),int(l[7]),int(l[8])])
    txt.append(l[9].split('\n')[0])

  return box, txt

def write_bbox(boxes, txt, txt_file):
  """ Writes bbox & texts on a txt file """
  with open(txt_file, 'w', encoding='utf-8') as fo:
    for i, box in enumerate(boxes):
      fo.write("{}\t".format(i))
      fo.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t".format(box[0],box[1],box[2],box[3],box[4],box[5],box[6],box[7]))
      fo.write("{}\n".format(txt[i]))

def draw_bbox(image_file, boxes):
  """ draw box on the image_file and writes res_image_file """
  folder = os.path.dirname(image_file)
  filename, _ = os.path.splitext(os.path.basename(image_file))

  res_image_file = folder + '/' + filename + '_res_.jpg'
  img = Image.open(image_file)
  img_array = np.array(img)
  b = img_array[:,:,0]
  g = img_array[:,:,1]
  r = img_array[:,:,2]
  corrected_img = np.dstack((r, g, b)) 

  for i, box in enumerate(boxes):
    
    pts = np.array([[box[0],box[1]],[box[2],box[3]],[box[4],box[5]],[box[6],box[7]]],np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(corrected_img, [pts], True, color=(0,0,255), thickness=2)
  
  cv2.imwrite(res_image_file, corrected_img)
  # cv2.imshow('Rectangle using polylines', corrected_img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()

def combine_box(box0, box1, txt0, txt1):
  """combine two boxes into one"""
  xmin = box0[0] 
  xmax = box1[2]
  ymin = box0[1] if box0[1] < box1[1] else box1[1]
  ymax = box0[5] if box0[5] > box1[5] else box1[5]
  box2 = [xmin,ymin,xmax,ymin,xmax,ymax,xmin,ymax]
  txt2 = txt0 + txt1
  return box2, txt2
  
def combine_txt(boxes, txt):
  """combine adjoining text boxes into one"""
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
      box0 = [xmin0,ymin0,xmax0,ymin0,xmax0,ymax0,xmin0,ymax0]
      txt0 = txt[0]
      h0 = ymax0 - ymin0
      
    else:
      xmin1 = box[0] if box[0] < box[6] else box[6]
      xmax1 = box[2] if box[2] > box[4] else box[4]
      ymin1 = box[1] if box[1] < box[3] else box[3]
      ymax1 = box[5] if box[5] > box[7] else box[7]
      box1 = [xmin1,ymin1,xmax1,ymin1,xmax1,ymax1,xmin1,ymax1]
      txt1 = txt[i]
      h1 = ymax1 - ymin1
      
      if abs(ymin0-ymin1) < h1*0.3 and abs(ymax0-ymax1) < h1*0.3 and (xmin1-xmax0) < h1*0.1:
        # print("{}{}".format(txt[i-1], txt[i]))
        count += 1
        box, txt2 = combine_box(box0,box1,txt0,txt1)
        xmin0 = box[0]
        xmax0 = box[2]
        ymin0 = box[1]
        ymax0 = box[5]
        box0 =  [xmin0,ymin0,xmax0,ymin0,xmax0,ymax0,xmin0,ymax0]
        txt0 = txt2
        
      else:
        newbox.append(box0)
        newtxt.append(txt0)
        xmin0 = xmin1
        xmax0 = xmax1
        ymin0 = ymin1
        ymax0 = ymax1
        box0 =  [xmin0,ymin0,xmax0,ymin0,xmax0,ymax0,xmin0,ymax0]
        txt0 = txt1
  newbox.append(box0)
  newtxt.append(txt0)

  # print(newbox)
  # print(newtxt)
  print(count)

  return newbox, newtxt
    


# imagefile = './data/sign.png'
imagefile = './data/e2.jpg'
txtfile = './data/e2.txt'
newtxtfile = './data/e2_.txt'

box, txt = read_bbox(imagefile, txtfile)
# print(box[0])
# print(txt[0])

newbox, newtxt = combine_txt(box, txt)
write_bbox(newbox, newtxt, newtxtfile)

draw_bbox(imagefile, newbox)

# 