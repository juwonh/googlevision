import os

def read_bbox(image_file):
  folder = os.path.dirname(image_file)
  filename, _ = os.path.splitext(os.path.basename(image_file))
  txt_file = folder + '/' + filename + '.txt'
  
  with open(txt_file, 'r', encoding='utf-8') as f:
    lines = [l for l in f]   
  
  print(lines)

  for i, line in enumerate(lines):
    l = line.split('\t')
    



image_file = '/home/jw/data/sign.png'
read_bbox(image_file)