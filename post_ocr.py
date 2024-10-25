import os
import cv2

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

##
def draw_bbox(image_file):
  folder = os.path.dirname(image_file)
  filename, _ = os.path.splitext(os.path.basename(image_file))


## 
def combine_symbols(box, txt):
  newbox = []
  newtxt = []

  return newbox, newtxt
    




image_file = '/home/jw/data/sign.png'
image_file = '/home/jw/data/test/4/e2.png'

box, txt = read_bbox(image_file)
print(box[0])
print(txt[0])

newbox, newtxt = add_symbols(box, txt)