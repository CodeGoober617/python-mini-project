import qrcode
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os


# This Function is responsible to take the input -> Convert it to Image Code -> Convert Image code to png.
def get_code():
    data_var = data.get()
    qr = qrcode.make(str(data_var))
    
    # This will ask for the directory the user wants to store the code and save it there.
    base.loc = filedialog.askdirectory()
    os.chdir(base.loc)
    save_as = name_to_save.get()
    
    # Try to add logo to center of QR code
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "logo.png")
        logo = Image.open(logo_path)
        
        # Resize logo to about 1/6 of QR code size (smaller for scannability)
        logo_size = qr.size[0] // 6
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Create a black background for the logo to maintain QR code scannability
        logo_bg = Image.new('RGB', (logo_size + 10, logo_size + 10), 'black')
        logo_bg.paste(logo, (5, 5), logo if logo.mode == 'RGBA' else None)
        
        # Convert QR code to RGB if needed
        if qr.mode != 'RGB':
            qr = qr.convert('RGB')
        
        # Paste logo at center of QR code
        offset = ((qr.size[0] - logo_bg.size[0]) // 2, (qr.size[1] - logo_bg.size[1]) // 2)
        qr.paste(logo_bg, offset)
    except FileNotFoundError:
        print("Logo file not found. QR code will be saved without logo overlay.")
    
    label= Label(base, text="QR Code Generated Successfully!", bg="green")
    label.place(x=80, y=150)
    qr.save(f"{save_as}.png")

#Get a Tk window of 400 * 200
base = Tk()
base.geometry("600x250")
base.title("Goobers QR Code Generator")

# Load and display logo in top right corner
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "logo.png")
    logo = Image.open(logo_path)  # Replace with your logo file path
    logo.thumbnail((175, 175), Image.Resampling.LANCZOS)  # Resize logo to 80x80
    logo_photo = ImageTk.PhotoImage(logo)
    logo_label = Label(base, image=logo_photo) #bg="white" 
    logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
    logo_label.place(x=415, y=10)  # Top right corner (adjusted for 800x400 window)
except FileNotFoundError:
    print("Logo file not found. Place a 'logo.png' in the same directory as this script.")

# variable to store text for QR Code
data = StringVar()
name_to_save = StringVar()
# Field to input text
# Get the name to be saved as
label_1 = Label(base, text="Save QR Code As").place(x=80, y=20)
dataEntry = Entry(textvariable=name_to_save, width="30")
dataEntry.place(x=80,y=40)

# What is suppose to be in the qrcode when scanned
label_1 = Label(base, text="Text inside QR Code").place(x=80, y=80)
dataEntry = Entry(textvariable=data, width="30")
dataEntry.place(x=80,y=100)


# Call get_code() on click
button = Button(base,text="Generate Code",command=get_code,width="30",height="2",bg="grey")
button.place(x=80,y=175)

base.mainloop()
