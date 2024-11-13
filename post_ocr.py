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
    box.append([int(l[1]),int(l[2]),int(l[3]),int(l[4]),int(l[5]),int(l[6]),int(l[7]),int(l[8]),int(l[0])])
    txt.append(l[9].split('\n')[0])

  return box, txt

def write_bbox(boxes, txts, txt_file):
  """ Writes bbox & texts on a txt file """
  with open(txt_file, 'w', encoding='utf-8') as fo:
    for i, box in enumerate(boxes):
      fo.write("{}\t".format(box[8]))
      fo.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t".format(box[0],box[1],box[2],box[3],box[4],box[5],box[6],box[7]))
      fo.write("{}\n".format(txts[i]))

def draw_bbox(image_file, boxes, res_image_file, putText):
  """ draw box on the image_file and writes res_image_file """

  img = Image.open(image_file)
  img_array = np.array(img)
  b = img_array[:,:,0]
  g = img_array[:,:,1]
  r = img_array[:,:,2]
  corrected_img = np.dstack((r, g, b)) 
  font = cv2.FONT_HERSHEY_SIMPLEX

  for i, box in enumerate(boxes):
    
    pts = np.array([[box[0],box[1]],[box[2],box[3]],[box[4],box[5]],[box[6],box[7]]],np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(corrected_img, [pts], True, color=(0,0,255), thickness=2)
    if (putText) :
      cv2.putText(corrected_img, "{}".format(box[8]), (box[0],box[1]), fontFace=font,fontScale = 0.7, color=(100, 0,100), thickness=1)
  
  cv2.imwrite(res_image_file, corrected_img)
  # cv2.imshow('Rectangle using polylines', corrected_img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()

def combine_box(box0, box1, txt0, txt1):
  """combine two boxes into one"""
  xmin = box0[0] if box0[0] < box1[0] else box1[0]
  xmax = box1[2] if box0[2] > box1[2] else box1[2]
  ymin = box0[1] if box0[1] < box1[1] else box1[1]
  ymax = box0[5] if box0[5] > box1[5] else box1[5]
  box2 = [xmin,ymin,xmax,ymin,xmax,ymax,xmin,ymax]
  txt2 = txt0 + txt1
  return box2, txt2
  
def get_intersection(min0, max0, min1, max1, h):
  h0 = max0 - min0
  h1 = max1 - min1
  intersection_start = max(min0, min1)
  intersection_end = min(max0, max1)
    
    # Check if there is a valid intersection
  if intersection_start <= intersection_end:
    inter = intersection_end - intersection_start
    return inter/h
  else:
      return 0  # No intersection


def combine_txt(boxes, txt):
  """combine adjoining text boxes into one"""
  newbox = []
  newtxt = []
  height = []
  count = 0
  id0 = 0
  
  for i, box in enumerate(boxes):
    if i == 0:
      box_pre = box
      id0 = box[8]
      xmin0 = box[0] if box[0] < box[6] else box[6]
      xmax0 = box[2] if box[2] > box[4] else box[4]
      ymin0 = box[1] if box[1] < box[3] else box[3]
      ymax0 = box[5] if box[5] > box[7] else box[7]
      box0 = [xmin0,ymin0,xmax0,ymin0,xmax0,ymax0,xmin0,ymax0,id0]
      txt0 = txt[0]
      h0 = box[7] - box[1]
      
    else:
      box_aft = box
      id1 = box[8]
      xmin1 = box[0] if box[0] < box[6] else box[6]
      xmax1 = box[2] if box[2] > box[4] else box[4]
      ymin1 = box[1] if box[1] < box[3] else box[3]
      ymax1 = box[5] if box[5] > box[7] else box[7]
      box1 = [xmin1,ymin1,xmax1,ymin1,xmax1,ymax1,xmin1,ymax1,id1]
      txt1 = txt[i]
      h1 = box[7] - box[1]

      hmin = min(h0, h1)
      hmax = max(h0, h1)
      
      if get_intersection(ymin0, ymax0, ymin1, ymax1, hmin) > 0.6 and (abs(box_aft[0]-box_pre[2]) < hmax*0.2 or (box_aft[0] < box_pre[2] and abs(box_aft[0]-box_pre[2])<hmax*0.5)):
        # print( get_intersection(ymin0, ymax0, ymin1, ymax1, hmin))
        # print(hmax)
        # print(box_aft[0]-box_pre[2])
        # print("{}{}".format(txt[i-1], txt[i]))

        count += 1
        box, txt2 = combine_box(box0,box1,txt0,txt1)
        xmin0 = box[0]
        xmax0 = box[2]
        ymin0 = box[1]
        ymax0 = box[5]
        box0 =  [xmin0,ymin0,xmax0,ymin0,xmax0,ymax0,xmin0,ymax0,id0]
        txt0 = txt2
        box_pre = box
        
      else:
        newbox.append(box0)
        newtxt.append(txt0)
        xmin0 = xmin1
        xmax0 = xmax1
        ymin0 = ymin1
        ymax0 = ymax1
        txt0 = txt1
        id0 = id1
        h0 = h1
        box0 =  [xmin0,ymin0,xmax0,ymin0,xmax0,ymax0,xmin0,ymax0,id0]
        box_pre = box
  newbox.append(box0)
  newtxt.append(txt0)

  # print(count)
  # print(newbox)
  # print(newtxt)

  return newbox, newtxt
    
def bbox_first(image_file):
  folder = os.path.dirname(image_file) + '/'
  filename, _ = os.path.splitext(os.path.basename(image_file))  
  txt_file = folder + filename + '.txt'

  resfolder = folder + 'res1/'
  if not os.path.isdir(resfolder):
    os.mkdir(resfolder)

  first_box_image = resfolder + filename + '_res1.jpg'

  box, txt = read_bbox(image_file, txt_file)
  draw_bbox(image_file, box, first_box_image, True)

def bbox_second(image_file):
  folder = os.path.dirname(image_file) + '/'
  filename, _ = os.path.splitext(os.path.basename(image_file))  

  txt_file = folder + filename + '.txt'
  newtxt_file = folder + filename + '_.txt'  
  
  box, txt = read_bbox(image_file, txt_file)
  newbox, newtxt = combine_txt(box, txt)
  write_bbox(newbox, newtxt, newtxt_file)

  resfolder = folder + 'res2/'
  if not os.path.isdir(resfolder):
    os.mkdir(resfolder)

  second_box_image = resfolder + filename + '_res2.jpg'
  draw_bbox(image_file, newbox, second_box_image, True)

# bbox_first('/home/jw/data/test/4/e2.jpg')


def run_bbox(folder, option):
  files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

  for file in files:
    filename, ext = os.path.splitext(file)
    ext = str.lower(ext)
    if ext == '.jpg' or ext == '.jpeg' or ext == '.gif' or ext == '.png' or ext == '.bmp':
      if( option == 1 ):
        bbox_first(folder + '/' + file)
      elif ( option == 2):
        bbox_second(folder + '/' + file)


def cropimage(image_file):
  folder = os.path.dirname(image_file) + '/'
  filename, _ = os.path.splitext(os.path.basename(image_file))  

  newtxt_file = folder + filename + '_.txt'  
  boxes, txts = read_bbox(image_file, newtxt_file)

  boxfolder = folder + 'box/'
  if not os.path.isdir(boxfolder):
    os.mkdir(boxfolder)
  
  cropfolder = folder + 'box/' + filename
  if not os.path.isdir(cropfolder):
    os.mkdir(cropfolder)

  try:
    im = Image.open(image_file)
  except IOError:
    print("IO Error", image_file)
  else:
    width, height = im.size 
    for i, box in enumerate(boxes):
      id = int(box[8])
      xmin = int(box[0])
      xmax = int(box[2]) 
      ymin = int(box[1])
      ymax = int(box[5])
      im2 = im.crop((xmin,ymin,xmax,ymax))
      crop_image = cropfolder + '/' + filename + "_" + str(id) + ".jpg"  
      im2.save(crop_image)   

# cropimage('/home/jw/data/test/4/e2.jpg')

def run_cropimage(folder):
  files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

  for file in files:
    filename, ext = os.path.splitext(file)
    ext = str.lower(ext)
    if ext == '.jpg' or ext == '.jpeg' or ext == '.gif' or ext == '.png' or ext == '.bmp':
      cropimage(folder + '/' + file)


imagefolder = '/home/jw/data/test/4'

''' Step 1. Generate initial textbox images first '''
# run_bbox(imagefolder,1)

''' Step 2. Manually edit txt file based on the images in res folder '''

''' Step 3. Generate second textbox images '''
run_bbox(imagefolder,2)

''' Step 4. Crop textbox '''
# run_cropimage(imagefolder)