from ast import arg
import cv2 as cv
import numpy as np
import argparse
from PIL import Image, ImageDraw, ImageOps, ImageFont
from pkgutil import get_data

char_set = {
  "standard": "@%#*+=-:. ",
  "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}

def get_data(mode):
  font = ImageFont.truetype("fonts\DejaVuSansMono.ttf", size = 10)
  scale = 2
  char_list = char_set[mode]
  return char_list, font, scale

def arguments():
  parser = argparse.ArgumentParser("")
  parser.add_argument("--fps", type=int, default=0, help="frames per second")
  parser.add_argument("--input", type=str, default="vidoes/input2.mp4", help="Input video")
  parser.add_argument("--output", type=str, default="videos/output.mp4", help="Ouput video")
  args = parser.parse_args()
  return args

def main(object):
  bg = 'black'
  if bg == 'white':
    bg_code = 255
  else:
    bg_code = 0

  char_list, font, scale = get_data("complex")
  char_count = len(char_list)
  col = 300

  frames = cv.VideoCapture(object.input)
  if object.fps == 0:
    fps = int(frames.get(cv.CAP_PROP_FPS))
  else:
    fps = object.fps

  while frames.isOpened():
    flag, frame = frames.read()
    if flag:
      gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    else:
      break

    height, width = gray_img.shape
    base_w = width / col
    base_h = scale * base_w
    row = int(height / base_h)

    if col > width or row > height:
      print("Choosing default dimensions since out of range")
      base_h = 12
      base_w = 6
      col = int(width / base_w)
      row = int(height / base_h)

    char_w, char_h = font.getsize("A")
    res_w = char_w * col
    res_h = scale * char_h * row
    res1 = Image.new("L", (res_w, res_h), bg_code) 
    draw = ImageDraw.Draw(res1)

    for i in range(row):
      min_h = min(int((i+1)*base_h), height)
      pixeli = int(i*base_h)
      line = "".join([char_list[min(int(np.mean(gray_img[pixeli:min_h, int(j*base_w):min(int((j+1)*base_w), width)]) / 255*char_count), char_count-1)] for j in range(col)]) + "\n"
      draw.text((0, i*char_h), line, fill = 255 - bg_code, font = font)

    if bg == "white":
      partial_img = ImageOps.invert(res1).getbbox()
    else:
      partial_img = res1.getbbox()
    
    res1 = res1.crop(partial_img)
    res1 = cv.cvtColor(np.array(res1), cv.COLOR_GRAY2BGR)
    res1 = np.array(res1)
    try:
      out
    except:
      out = cv.VideoWriter(object.output, cv.VideoWriter_fourcc(*"XVID"), object.fps, ((res1.shape[1], res1.shape[0])))
    
    frames.release()
    out.release()

if __name__ == '__main__':
  object = arguments()
  main(object)