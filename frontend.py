import subprocess
import threading
from tkinter import *
from PIL import ImageTk, Image
import sys
import cv2
import os
# Constants
APP_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(APP_DIR, "sign_language_photo.jpg")
app_path=os.path.join(APP_DIR, "app.py")
SCREEN_WIDTH = None  # Will be updated later
SCREEN_HEIGHT = None  # Will be updated later

# Function to open a new window for capturing an image
def capture_video():
    window.destroy()
    threading.Thread(target=run_app).start()

def run_app():
    subprocess.run(["python", app_path])  
def load_images():
    img = Image.open(IMAGE_PATH)
    img = img.resize((450, 450), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    return img

# Create Tkinter window
window = Tk()
window.title("Sign Language")

# Get the screen width and height
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()

# Set the window size to fullscreen
window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

# Header
header_label = Label(window, text="Sign Language", font=("Arial", 20))
header_label.pack(pady=20)

# Frame for history and images
main_frame = Frame(window)
main_frame.pack(expand=True, fill="both")

# History of Sign Language section
history_frame = Frame(main_frame,bd=5,relief="groove")
history_frame.pack(side=LEFT, padx=10,pady=50, fill="both")

history_label = Label(history_frame, text="Introduction of Sign Language", font=("Arial", 16))
history_label.pack(pady=10)

# Sample text for history
history_text = [
    "Sign language has a long history dating back centuries.",
    "One of the earliest recorded references to sign language dates back to the 5th century BC in Greece, where philosopher Socrates discussed the use of sign language by the deaf.",
    "In the 18th century, the first school for the deaf was established in Paris by Abbé Charles-Michel de l'Épée, marking a significant milestone in the formal education of deaf individuals and the development of sign language.",
    "American Sign Language (ASL) evolved from French Sign Language (LSF) and indigenous sign languages used by deaf communities in the United States during the 19th century.",
    "William Stokoe, a linguist, played a crucial role in recognizing ASL as a legitimate language with its own grammar and syntax in the 1960s, challenging the prevailing view that sign languages were merely 'broken' versions of spoken languages.",
    "Today, sign languages are recognized as fully-fledged languages with their own linguistic structures and cultural significance, used by millions of deaf and hard-of-hearing individuals around the world."
]

for text in history_text:
    bullet_point = Label(history_frame, text="\u2022 " + text, wraplength=600, justify=LEFT)
    bullet_point.pack(anchor="w", padx=20, pady=5)

# Images of Sign Language section
images_frame = Frame(main_frame)
images_frame.pack(side=RIGHT, padx=80, pady=20,fill='both')

# Load and display images
sign_language_image = load_images()
image_label = Label(images_frame, image=sign_language_image)
image_label.pack(pady=5)

# Button to capture an image
capture_button = Button(window, text="Capture Symbol", command=capture_video)
capture_button.pack(pady=100)

# Set both sections to have equal width
window.update_idletasks()
max_width = max(history_frame.winfo_reqwidth(), images_frame.winfo_reqwidth())
history_frame.config(width=SCREEN_WIDTH/2)
images_frame.config(width=SCREEN_WIDTH/2)

 # Break gracefully
if cv2.waitKey(10) & 0xFF == ord('q'):
    sys.exit()

# Run the Tkinter event loop
window.mainloop()
