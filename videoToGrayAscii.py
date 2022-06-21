# import required libraries
import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont

# character set to be taken into account for displaying ascii art
char_set = {
  "standard": "@%#*+=-:. ",
  "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}

# function to define the attributes of the data displayed
def get_data(mode):
  font = ImageFont.truetype("fonts\DejaVuSansMono.ttf", size = 10)
  scale = 2
  char_list = char_set[mode]
  return char_list, font, scale

# main funtion
def main():
  # path to be taken as input by the user
  path = input('Enter input video path: ')
  if path == '':
    path = '.\videos\input.jpg'     #default path

  bg = 'black'
  if bg == 'white':
    bg_code = 255
  else:
    bg_code = 0
  
  char_list, font, scale = get_data("complex")
  char_count = len(char_list)
  col = 120
                                                                 
  # capturing video from the given path                                                
  cam = cv.VideoCapture(path)

  # looping either until the last frame or pressing the key '0"
  for frame_idx in range(int(cam.get(cv.CAP_PROP_FRAME_COUNT))):
    # extracting current frame
    ret, frame = cam.read()
    curr_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # calculating height and width of current frame
    height, width = curr_frame.shape
    # calculating height and width of a pixel
    base_w = width / col
    base_h = scale * base_w
    row = int(height / base_h)

    if col > width or row > height:
      print("Choosing default dimensions since out of range")
      base_h = 12
      base_w = 6
      col = int(width / base_w)
      row = int(height / base_h)

    # calculating height and width of a character
    char_w, char_h = font.getsize("A")
    # calculating height and width of final image
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
    # converting image to a numpy array
    res1 = np.array(res1)
    # displaying current modified frame
    cv.imshow("Frame", res1)
    if cv.waitKey(25) & 0xFF == ord('0'):
      break
    
  # releasing all space and windows once done
  cam.release()
  cv.destroyAllWindows()

if __name__ == '__main__':
  main()