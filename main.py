import streamlit as st
import os
import subprocess
from PIL import Image
from stegano import lsb

# Tool selection radio button
genre = st.radio(
    "Select your tool - ",
    [":rainbow[nmap]", "***Steganography***", "Hashcat"],
    key='tool_selection',
    help="Choose the tool you want to use."
)

# Button to initiate the selected tool
button1 = st.button('Let\'s Go!', key='run_button')

# Check if the button has been pressed
if st.session_state.get('button') != True:
    st.session_state['button'] = button1

# Execute the chosen tool when the button is pressed
if st.session_state['button'] == True:
    if genre == ":rainbow[nmap]":
        # Nmap tool section
        options = ["-sS"]
        host = st.text_input('Host', '127.0.0.1')
        command = ['nmap'] + options + [host]
        if st.button('Run Nmap!'):
            result = subprocess.run(command, capture_output=True, text=True)
            st.text(result.stdout)

    elif genre == "***Steganography***":
        # Steganography tool section
        st.info("Steganography code goes here.")
        image = st.file_uploader("Upload an image for steganography", type=["jpg", "png", "bmp"])
        text_to_hide = st.text_area("Enter text to hide")

        if st.button('Hide Text!'):
            if image is not None and text_to_hide:
                # Open the image
                img = Image.open(image)
                steganographic_image = lsb.hide(img, text_to_hide)

                # Save the steganographic image
                steganographic_image_path = "steganographic_image.png"
                steganographic_image.save(steganographic_image_path)

                # Display the steganographic image
                st.image(steganographic_image_path, caption="Steganographic Image", use_column_width=True)
            elif image is not None:
                img = Image.open(image)
                revealed_text = lsb.reveal(img)

                st.text_area("Revealed Text", revealed_text)

    elif genre == "Hashcat":
        # Hashcat tool section
        hash_to_crack = st.text_input('Enter Hash to Crack', '')
        wordlist = st.text_input('Enter Wordlist', 'wordlist.txt')
        command = f'hashcat -m 0 {hash_to_crack} {wordlist}'
        if st.button('Run Hashcat!'):
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            st.text(result.stdout)
