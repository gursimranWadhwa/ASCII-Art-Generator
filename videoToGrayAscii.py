import imp
import sys
from time import time
from tkinter import Frame
from typing import overload
import cv2 as cv
import numpy as np
import argparse
# import time
# import sys
# import os
# import json
# import random
from PIL import Image, ImageDraw, ImageOps, ImageFont
# from pkgutil import get_data

char_set = {
  "standard": "@%#*+=-:. ",
  "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}

def get_data(mode):
  font = ImageFont.truetype("fonts\DejaVuSansMono.ttf", size = 10)
  scale = 2
  char_list = char_set[mode]
  return char_list, font, scale

# def get_frames(frame):
#   image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
#   out = Image.fromarray(image)
#   return out

# def take_input(cap, resolution):
#   set_of_frames = []
#   duration = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
#   it = 0
#   while (True):
#     it += 1
#     ret, frame = cap.read()
#     if ret:
#       curr_frame = get_frames(frame)
#       resized = 


def create_object():
  parser = argparse.ArgumentParser()
  parser.add_argument("--input", type=str, default="videos/input.mp4", help="Input video")
  parser.add_argument("--output", type=str, default="videos/output.mp4", help="Output video")
  parser.add_argument("--col", type=int, default=100, help="Characters count in output width")
  parser.add_argument("--fps", type=int, default=0, help="Number of frames per second")
  parser.add_argument("--overlay_ratio", type=float, default=0.2, help="Overlay width ratio")
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
  col = object.col

  cap = cv.VideoCapture(object.input)
  if object.fps == 0:
    fps = int(cap.get(cv.CAP_PROP_FPS))
  else:
    fps = object.fps

  while cap.isOpened():
    flag, frame = cap.read()
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
      out = cv.VideoWriter(object.output, cv.VideoWriter_fourcc(*'MP4V4'), fps, ((res1.shape[1], res1.shape[0])))
    
    cap.release()
    out.release()

def display(set_of_frames, fps):
  while (True):
    for i in set_of_frames:
      sys.stdout.write(i)
      time.sleep(1 / fps)

if __name__ == '__main__':
  object = create_object()
  main(object)