import os
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/jw/.config/gcloud/application_default_credentials.json'

""" Get text from image using google vision ocr API
    Write extracted text on a txt file """
def ocr_image(image_file):
  client = vision.ImageAnnotatorClient()

  folder = os.path.dirname(image_file)
  filename, _ = os.path.splitext(os.path.basename(image_file))
  txt_file = folder + '/' + filename + '.txt'

  with open(image_file, "rb") as img:
    content = img.read()

  image = vision.Image(content=content)
  response = client.text_detection(image=image)
  texts = response.text_annotations

  if response.error.message:
    raise Exception(
        "{}\nFor more info on error messages, check: "
        "https://cloud.google.com/apis/design/errors".format(response.error.message)
    )

  index = 0
  with open(txt_file, 'w', encoding='utf-8') as fo:
    for text in texts:
      vertices = [
          f"{vertex.x}\t{vertex.y}" for vertex in text.bounding_poly.vertices
      ]

      if (index == 0):
        print(f'{text.description}')
      else:
        fo.write("{}\t".format(index))
        fo.write("{}".format("\t".join(vertices)))
        fo.write("\t{}\n".format(text.description))
      index += 1
            

""" Run ocr_image for every image in a folder """
def run_ocr_image(image_folder):

  for file in os.listdir(image_folder):
    if file.endswith(('.jpeg','.jpg','.png')):
      image_file = os.path.join(image_folder,file)
      print(f"Processing {file}...") 
      ocr_image(image_file)


""" This is where to run googleVision OCR
"""
image_folder = '/home/jw/data/test/5/'
run_ocr_image(image_folder)
