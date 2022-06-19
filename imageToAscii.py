import cv2 as cv
from cv2 import COLOR_BGR2RGB
import numpy as np
from cv2 import waitKey
from PIL import Image, ImageDraw, ImageOps, ImageFont
from pkgutil import get_data

char_set = {
  "standard": "@%#*+=-:. ",
  "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}

def get_data(mode):
  # font = ImageFont.truetype("fonts\DejaVuSansMono.ttf", size = 10)
  font = ImageFont.truetype("fonts\CourierPrime-Regular.ttf", size = 10)
  scale = 1
  char_list = char_set[mode]
  return char_list, font, scale

def main():
  bg = 'black'
  if bg == 'white':
    bg_code = (255, 255, 255)
  elif bg == 'black':
    bg_code = (0, 0, 0)

  char_list, font, scale = get_data("complex")
  char_count = len(char_list)
  col = 150
  input = cv.imread('./images/input5.jpg')
  input = cv.cvtColor(input, COLOR_BGR2RGB)

  height, width, _ = input.shape
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
  res1 = Image.new("RGB", (res_w, res_h), bg_code) 
  draw = ImageDraw.Draw(res1)

  for i in range(row):
    for j in range(col):
      min_h = min(int((i+1)*base_h), height)
      min_w = min(int((j+1)*base_w), width)
      pixeli = int(i*base_h)
      pixelj = int(j*base_w)
      partial_img = input[pixeli:min_h, pixelj:min_w, :]
      partial_avg_color = np.sum(np.sum(partial_img, axis = 0), axis = 0) / (base_h * base_w)
      partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
      c = char_list[min(int(np.mean(partial_img)*char_count / 255), char_count - 1)]
      draw.text((j*char_w, i*char_h), c, fill = partial_avg_color, font = font)

  if bg == "white":
    partial_img = ImageOps.invert(res1).getbbox()
  elif bg == "black":
    partial_img = res1.getbbox()
  res1 = res1.crop(partial_img)
  res1.save("./images/res2.jpg")

main()