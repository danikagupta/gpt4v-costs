import streamlit as st
from PIL import Image
import math
#
#
#
st.set_page_config(
    page_title="GPT4V Cost Computation",
    page_icon="👋",
)
#
#
#
def round_up(numerator, denominator):
  return math.ceil(numerator/denominator)
#
#
#
def compute_tokens(image,level):
  image=Image.open(image)
  width, height = image.size
  st.image(uploaded_file, caption=f'Uploaded Image: {width}x{height}')
  if(level=="low"):
    return 85
  else:
    max_size=max(width,height)
    if(max_size>2048):
      new_width=round(width*2048/max_size)
      new_height=round(height*2048/max_size)
      image2=image.resize((new_width,new_height))
      st.image(image2, caption=f'MAX 2048: Image resized. {width}x{height}')
    else:
      image2=image
      st.image(image2, caption=f'MAX 2048: Image not resized. {width}x{height}')
    width, height = image2.size
    min_size=min(width,height)
    if(min_size>768):
      new_width=round(width*768/min_size)
      new_height=round(height*768/min_size)
      image3=image2.resize((new_width,new_height))
      st.image(image3, caption=f'MIN 768: Image resized. {new_width}x{new_height}')
    else:
      image3=image2
      st.image(image3, caption=f'MIN 768: Image not resized. {width}x{height}')
    width, height = image2.size
    squares=round_up(width,512)*round_up(height,512)
    tokens=squares*170+85
    return tokens
#
#
#
level=st.sidebar.select_slider("## Select detail level",["low","high"])

uploaded_file = st.file_uploader("Upload your image file", type=["png", "jpg", "jpeg"])
final_answer=st.empty()
if uploaded_file is not None:
  #st.image(uploaded_file, caption='Uploaded Image.')
  tokens=compute_tokens(uploaded_file,level)
  final_answer.markdown(f"## Tokens: {tokens}")
else:
  st.write("Please upload an image file")
#
#
#
