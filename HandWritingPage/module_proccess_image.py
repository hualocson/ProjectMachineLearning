import cv2
import numpy as np
import streamlit as st
from PIL import Image

def proccessImg(path):
  img = cv2.imread(path)
  # Chuyển sang ảnh nhị phân
  _, imgBi = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
  # Chuyển ảnh sang gray image
  imgGrayBi = cv2.cvtColor(imgBi, cv2.COLOR_BGR2GRAY)

  pick = showContour(img, imgGrayBi)
  return getCropImge(img, pick)

def convertImage(img_data):
  im = Image.fromarray(img_data.astype("uint8"), mode="RGBA")
  image = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
  _, imgBi = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
  gray = cv2.cvtColor(imgBi, cv2.COLOR_RGB2GRAY)

  newImg = []
  for row in gray:
    arr = []
    for col in row:
      if col == 255:
        arr.append([255, 0, 0])
      else:
        arr.append([0, 0, 0])
    newImg.append(arr)

  newImg = np.array(newImg)
  return newImg

def resizeImg(img, width=12, height=28):
  dim = (width, height)
  resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
  return resized

def non_max_suppression(boxes, overlapThresh):
  '''
  boxes: List các bounding box
  overlapThresh: Ngưỡng overlapping giữa các hình ảnh
  '''
  # Nếu không có bounding boxes thì trả về empty list
  if len(boxes)==0:
    return []
  # Nếu bounding boxes nguyên thì chuyển sang float.
  if boxes.dtype.kind == "i":
    boxes = boxes.astype("float")

  # Khởi tạo list của index được lựa chọn
  pick = []

  # Lấy ra tọa độ của các bounding boxes
  x1 = boxes[:,0]
  y1 = boxes[:,1]
  x2 = boxes[:,2]
  y2 = boxes[:,3]

  # Tính toàn diện tích của các bounding boxes và sắp xếp chúng theo thứ tự từ bottom-right, chính là tọa độ theo y của bounding box
  area = (x2 - x1 + 1) * (y2 - y1 + 1)
  idxs = np.argsort(y2)
  # Khởi tạo một vòng while loop qua các index xuất hiện trong indexes
  while len(idxs) > 0:
    # Lấy ra index cuối cùng của list các indexes và thêm giá trị index vào danh sách các indexes được lựa chọn
    last = len(idxs) - 1
    i = idxs[last]
    pick.append(i)

    # Tìm cặp tọa độ lớn nhất (x, y) là điểm bắt đầu của bounding box và tọa độ nhỏ nhất (x, y) là điểm kết thúc của bounding box
    xx1 = np.maximum(x1[i], x1[idxs[:last]])
    yy1 = np.maximum(y1[i], y1[idxs[:last]])
    xx2 = np.minimum(x2[i], x2[idxs[:last]])
    yy2 = np.minimum(y2[i], y2[idxs[:last]])

    # Tính toán width và height của bounding box
    w = np.maximum(0, xx2 - xx1 + 1)
    h = np.maximum(0, yy2 - yy1 + 1)

    # Tính toán tỷ lệ diện tích overlap
    overlap = (w * h) / area[idxs[:last]]

    # Xóa index cuối cùng và index của bounding box mà tỷ lệ diện tích overlap > overlapThreshold
    idxs = np.delete(idxs, np.concatenate(([last],
      np.where(overlap > overlapThresh)[0])))
  # Trả ra list các index được lựa chọn
  return boxes[pick].astype("int")

def _drawBoudingBox(img, pick):
  imgOrigin = img.copy()

  for (startX, startY, endX, endY) in pick:
      imgOrigin = cv2.rectangle(imgOrigin, (startX, startY), (endX, endY), (0, 255, 0), 2)
  st.image(imgOrigin)

def showContour(img, imgGrayBi):
  contours, hierarchy = cv2.findContours(imgGrayBi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  # Sắp xếp các contour theo diện tích giảm dần:
  area_cnt = [cv2.contourArea(cnt) for cnt in contours]
  area_cnt = np.array(area_cnt)
  # area_sort = np.argsort(area_cnt)[::-1]

  boundingBoxes = []
  for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    x1, y1, x2, y2 = x, y, x+w, y+h
    boundingBoxes.append((x1, y1, x2, y2))

  boundingBoxes = [box for box in boundingBoxes if box[:2] != (0, 0)]
  boundingBoxes = np.array(boundingBoxes)
  pick = non_max_suppression(boundingBoxes, 0.5)
  arr = pick[pick[:, 0].argsort()]
  # _drawBoudingBox(img, pick)
  return arr

def getCropImge(img, pick):
  crop_images = [_cropImage(x1, y1, x2, y2, img) for (x1, y1, x2, y2) in pick]
  return crop_images

def _cropImage(x1, y1, x2, y2, img):
  if np.ndim(img) == 3:
    crop = img[y1:y2, x1:x2, :]
  else:
    crop = img[y1:y2, x1:x2]
  return crop
