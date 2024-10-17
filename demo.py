import os, io
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/jw/.config/gcloud/application_default_credentials.json'
client = vision.ImageAnnotatorClient()


file = '/home/jw/data/sign.png'
otxt = '/home/jw/data/sign.txt'
file = '/home/jw/data/test/4/e2.jpg'
otxt = '/home/jw/data/test/4/e2.txt'
file = '/home/jw/data/test/5/k2.jpg'
otxt = '/home/jw/data/test/5/k2.txt'
with open(file, "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
index = 0
with open(otxt, 'w', encoding='utf-8') as fo:
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
          

    

      # print("{}".format("\t".join(vertices)))

if response.error.message:
    raise Exception(
        "{}\nFor more info on error messages, check: "
        "https://cloud.google.com/apis/design/errors".format(response.error.message)
    )
