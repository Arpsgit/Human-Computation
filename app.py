import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_image_select import image_select
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from image_db import img_db, Base

engine = create_engine(os.environ.get("DATABASE_URL"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
sess = Session()

st.set_page_config(
    page_title = "image annotation",
    page_icon = ":frame_with_picture:",
    layout = "wide",
)


def text_region(coord, text, size):
    text_length = len(text)
    num_word = len(text.split(sep=" "))
    num_char = len(text.replace(" ", ""))
    x1 = coord['x']
    y1 = coord['y']
    x2 = x1 + (size * (text_length+1) / 2)
    y2 = y1 + size
    return [x1, y1, x2, y2], num_char, num_word


with st.container():
    st.title("An Application for taking Annotated Pictorial data from Users")
    st.header("How to :green[USE] :star:")
    st.write(
        """
        upload an image of any object then annotate it in suitable position
        - First select an image
        - Then click on any position in the image where you want to add the text
        - Add some funny text to show your sense of humour.
        - Also don't forget to enter appropriate font colour and size of text :cat: 
        - You can edit those above mentioned things. So, change them again and again.
        - Finally submit the image for the betterment of human civilization :frog: 
        """
    )
    user_name_input = st.text_input(
            "So what is your name ? :clown_face:",
            value = ""
        )
with st.container():
    st.write("---")
    image_choice = image_select(label='Select an image',
                                images=["actual_image/1.jpg",
                                        "actual_image/2.jpg",
                                        "actual_image/3.jpg",
                                        "actual_image/4.jpg",
                                        "actual_image/5.jpg",
                                        "actual_image/6.jpg"],
                                captions=['Will Smith',
                                          'Salt Bae',
                                          'Listening',
                                          'Disgusting',
                                          'Dabbing',
                                          'Memestine Chapel'])

    if image_choice:
        image = Image.open(image_choice)
        rgb_image = image.convert('RGB')
        st.text("click on any position Where you want to place the text.")
        coords = streamlit_image_coordinates(
            rgb_image,
            key = "pil",
        )
        if coords is not None:
            list_val = [coords["x"], coords["y"]]
            tuple_val = tuple(float(val) for val in list_val)
    else:
        pass

with st.container():
    st.write("---")
    col1, col2 = st.columns(2)

    with col1:
        text_input = st.text_input(
            "Enter the text you want to enter in image 👇",
            value = ""
        )
        text_colour = st.radio(
            "select the colour of text",
            ("Red", "Green", "Blue", "White")
        )
        if text_colour == 'Red':
            txt_clr = (255, 0, 0)
        elif text_colour == "Green":
            txt_clr = (0, 128, 0)
        elif text_colour == "Blue":
            txt_clr = (0, 0, 255)
        elif text_colour == "White":
            txt_clr = (255, 255, 255)

        font_size = st.number_input(
            "Enter the font size of text 👇",
            key = int,
            min_value = 10,
            step = 1
        )

    with col2:
        if image_choice and coords is not None:
            I1 = ImageDraw.Draw(rgb_image)

            font = ImageFont.truetype('font/arial.ttf', font_size)    
            I1.text(tuple_val, text_input, font = font, fill = txt_clr, stroke_width=1, stroke_fill='black')
            st.image(rgb_image, caption = 'uploaded_image')
            region, num_chars, num_words = text_region(coords, text_input, font_size)
            buf = BytesIO()
            rgb_image.save(buf, format = "JPEG")
            byte_im = buf.getvalue()
            btn = st.download_button(
                label = "Download Image",
                data = byte_im,
                file_name = "image.jpg",
                mime = "image/jpg",
            )

            submit = st.button("submit image")
            if submit:
                try:
                    entry = img_db(
                        user_name = user_name_input,
                        file_name = image_choice,
                        coord_x1 = region[0],
                        coord_y1 = region[1],
                        coord_x2 = region[2],
                        coord_y2 = region[3],
                        number_of_letters = num_chars,
                        number_of_words = num_words,
                        font_size=font_size,
                        img = byte_im
                    )
                    sess.add(entry)
                    sess.commit()
                    st.success("Successful Submission :cow:")
                    st.snow()
                except Exception as e:
                    st.error(f"Error Occurred {e}")
        else:
            pass
