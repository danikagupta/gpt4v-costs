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
model_prices={"gpt-4-turbo":0.01,"gpt-5":1.00}
#
#
#
def round_up(numerator, denominator):
  return math.ceil(numerator/denominator)
#
#
#
def compute_tokens(image,level,use_column_width=False):
  image=Image.open(image)
  width, height = image.size
  caption=f'## Uploaded Image: Size starts as {width}x{height}'
  with st.expander(caption):
    st.image(uploaded_file, caption=f'Uploaded Image: Size starts as {width}x{height}',use_column_width=use_column_width)
  if(level=="low"):
    return 85,0,0,0
  else:
    max_size=max(width,height)
    if(max_size>2048):
      new_width=round(width*2048/max_size)
      new_height=round(height*2048/max_size)
      image2=image.resize((new_width,new_height))
      caption=f'Step 1: Image resized as higher dimension {max_size} > 2048. Size becomes {new_width}x{new_height}'
      with st.expander(caption):
        st.image(image2,use_column_width=use_column_width)
    else:
      image2=image
      caption=f'Step 1: Image not resized as higher dimension {max_size} <= 2048. Size remains{width}x{height}'
      with st.expander(caption):
        st.image(image2,use_column_width=use_column_width)
    width, height = image2.size
    min_size=min(width,height)
    if(min_size>768):
      new_width=round(width*768/min_size)
      new_height=round(height*768/min_size)
      image3=image2.resize((new_width,new_height))
      caption=f'Step 2: Image resized as lower dimension {min_size} > 768. Size becomes{new_width}x{new_height}'
      with st.expander(caption):
        st.image(image3,use_column_width=use_column_width)
    else:
      image3=image2
      caption=f'Step 2: Image not resized as lower dimension {min_size} <= 768. Size remains {width}x{height}'
      with st.expander(caption):
        st.image(image3,use_column_width=use_column_width)
    width, height = image3.size
    square_width=round_up(width,512)
    square_height=round_up(height,512)
    squares=square_width*square_height
    tokens=squares*170+85
    return tokens,squares,square_width,square_height
#
#
#
uploaded_file = st.sidebar.file_uploader("Upload your image file", type=["png", "jpg", "jpeg"])
level=st.sidebar.select_slider("Select detail level",["low","high"])
final_answer=st.empty()
if uploaded_file is not None:
  #st.image(uploaded_file, caption='Uploaded Image.')
  tokens,squares,square_width,square_height=compute_tokens(uploaded_file,level)
  cost=tokens*model_prices["gpt-4-turbo"]
  if(level=="low"):
    final_answer.markdown(f"## Cost is ${cost} for 1000 such images at low detail. \n ### Every image is 85 tokens, regardless of size.")
  else:
    final_answer.markdown(f"## Cost is ${cost} for 1000 such images at high detail. \n ### Tiles: {square_width}x{square_height}={squares}, Tokens: {170*squares}+85={tokens}")
else:
  st.write("Please upload an image file")
#
#
#
