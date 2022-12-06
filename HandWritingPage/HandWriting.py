CONTEXT = "HandWritingPage"
MODEL_PATH = "./HandWritingPage/mymodel.h5"
# Specify canvas parameters in application
def run():
  import pandas as pd
  import matplotlib.pyplot as plt
  import streamlit as st
  from streamlit_drawable_canvas import st_canvas
  import HandWritingPage.CNNmodel as cn
  import HandWritingPage.module_proccess_image as imProccess
  import numpy as np
  import cv2
  from PIL import Image
  stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 25)
  stroke_color = st.sidebar.color_picker("Stroke color hex: ", "#EFD4D6")
  realtime_update = st.sidebar.checkbox("Update in realtime", True)

  container_large = st.container()

  # Create a canvas component
  with container_large:
    canvas_result2 = st_canvas(
        fill_color="rgb(255, 165, 0)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#000",
        update_streamlit=realtime_update,
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="canvas2",
    )


  container_crop = st.container()
  with container_crop:
    if canvas_result2.image_data is not None:
      if st.button("Show Result"):
        file_path = f"./{CONTEXT}/img/large_img.jpg"
        img_data = canvas_result2.image_data
        newImg = imProccess.convertImage(img_data)
        cv2.imwrite(file_path, newImg)


        arr = imProccess.proccessImg(file_path)
        path = f"./{CONTEXT}/img/pic.png"
        stx = ""
        for i in arr:
          container_result = container_crop.container()
          col1, col2 = container_result.columns(2)
          img = imProccess.resizeImg(i, 60, 140)
          with container_result and col1:
            st.image(img)
          image = imProccess.resizeImg(i)
          image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
          cv2.imwrite(path, image)
          img = []
          img.append(cv2.imread(path))

          img = np.array(img, dtype = 'float32')

          model_demo = cn.CNN_Model(False)
          model_demo.load(MODEL_PATH)
          res = model_demo.test_pic(img)

          with container_result and col2:
            stx += res
            st.write("predict: ", res)

        st.info(stx)

