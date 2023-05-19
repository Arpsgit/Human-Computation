import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_image_select import image_select
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from image_db import img_db, Base

st.set_page_config(
    page_title = "image annotation",
    page_icon = ":frame_with_picture:",
    layout = "wide",
)

'''engine = create_engine(os.environ.get("DATABASE_URL"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
sess = Session()'''

'''st.set_page_config(
    page_title = "image annotation",
    page_icon = ":frame_with_picture:",
    layout = "wide",
)'''


def text_region(coord, text, size):
    text_length = len(text)
    num_words = len(text.split(sep=" "))
    x0 = coord['x']
    y0 = coord['y']
    x1 = x0 + (size * (text_length+1) / 2)
    y1 = y0 + size
    return [(x0, y0), (x1, y1)]


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
                                images=["image/Ancient-Aliens.jpg",
                                        "image/Disaster-Girl.jpg",
                                        "image/Distracted-Boyfriend.jpg",
                                        "image/Laughing-Leo.png",
                                        "image/Mocking-Spongebob.jpg",
                                        "image/Roll-Safe-Think-About-It.jpg",
                                        "image/Success-Kid.jpg"],
                                captions=['Ancient-Aliens',
                                          'Disaster-Girl',
                                          'Distracted-Boyfriend',
                                          'Laughing-Leo',
                                          'Mocking-Spongebob',
                                          'Roll-Safe-Think-About-It',
                                          'Success-Kid'])

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
            ("Red", "Green", "Blue", "White", "Black")
        )
        if text_colour == 'Red':
            txt_clr = (255, 0, 0)
        elif text_colour == "Green":
            txt_clr = (0, 128, 0)
        elif text_colour == "Blue":
            txt_clr = (0, 0, 255)
        elif text_colour == "White":
            txt_clr = (255, 255, 255)
        elif text_colour == "Black":
            txt_clr = (0, 0, 0)

        font_size = st.number_input(
            "Enter the font size of text 👇",
            key = int,
            min_value = 5, 
            step = 1
        )

    with col2:
        if image_choice and coords is not None:
            I1 = ImageDraw.Draw(rgb_image)

            font = ImageFont.truetype('font/arial.ttf', font_size)    
            I1.text(tuple_val, text_input, font = font, fill = txt_clr, stroke_width=3, stroke_fill='black')
            I1.rectangle(xy=text_region(coords, text_input, font_size), fill=None, outline='green', width= 3)
            st.image(rgb_image, caption = 'uploaded_image')

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
                '''try:
                    entry = img_db(
                        user_name = user_name_input,
                        file_name = uploaded_image.name,
                        img = byte_im
                    )
                    sess.add(entry)
                    sess.commit()
                    st.success("Successful Submission :cow:")
                    st.snow()
                except Exception as e:
                    st.error(f"Error Occured {e}")'''
        else:
            pass
