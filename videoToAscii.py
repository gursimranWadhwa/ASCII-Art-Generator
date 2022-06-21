import os
import sys
from time import time
from tkinter import Frame
import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont

char_set = {
  "standard": "@%#*+=-:. ",
  "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}

def get_data(mode):
  font = ImageFont.truetype("fonts\DejaVuSansMono.ttf", size = 10)
  scale = 2
  char_list = char_set[mode]
  return char_list, font, scale

# def display_video(frame_list, fps):
#   while (True):
#     for i in frame_list:
#       sys.stdout.write(i)
#       time.sleep(1 / fps)

def main():
  bg = 'black'
  if bg == 'white':
    bg_code = 255
  else:
    bg_code = 0
  
  char_list, font, scale = get_data("complex")
  char_count = len(char_list)
  col = 120
                                                                 
  cam = cv.VideoCapture("./videos/input.mp4")
  frames_count = 0
  # frame_list = []
  fps = cam.get(cv.CAP_PROP_FPS)
  # height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))
  # width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
  # video_writer = cv.VideoWriter('./videos/output.avi', cv.VideoWriter_fourcc('P','I','M','1'), fps, (width, height), isColor=False)
  if fps > 60:
    fps = 30

  while (True):
    ret, frame = cam.read()
    if ret:
      curr_frame = cv.cvtColor(cv.UMat(frame), cv.COLOR_BGR2GRAY)
      frames_count += 1
    else:
      break
    height, width = curr_frame.shape
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
      line = "".join([char_list[min(int(np.mean(curr_frame[pixeli:min_h, int(j*base_w):min(int((j+1)*base_w), width)]) / 255*char_count), char_count-1)] for j in range(col)]) + "\n"
      draw.text((0, i*char_h), line, fill = 255 - bg_code, font = font)

    if bg == "white":
      partial_img = ImageOps.invert(res1).getbbox()
    else:
      partial_img = res1.getbbox()

    res1 = res1.crop(partial_img)
    cv.imwrite("Frame.jpg", res1)
      # video_writer.write(res1)
      # frame_list.append("/n".join(res1))
    
  cam.release()
  cv.destroyAllWindows()
  # video_writer.release()
  # display_video(frame_list, fps)

if __name__ == '__main__':
  main()