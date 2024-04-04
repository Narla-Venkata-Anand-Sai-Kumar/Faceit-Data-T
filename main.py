import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import os
from PIL import Image, ImageTk

class LiveStreamCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Stream Capture")

        self.video_source = 0  # Default webcam

        # Create a frame for the UI elements
        self.ui_frame = tk.Frame(root, bg='#f0f0f0')
        self.ui_frame.pack(padx=10, pady=10)

        # Create a label for the name entry
        self.name_label = tk.Label(self.ui_frame, text="Enter Name:", bg='#f0f0f0', font=('Helvetica', 12))
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        # Create an entry widget for entering the name
        self.name_entry = tk.Entry(self.ui_frame, bg='white', bd=2, relief=tk.FLAT, font=('Helvetica', 12))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        # Create a button for capturing images
        self.capture_button = tk.Button(self.ui_frame, text="Capture", command=self.capture_image, bg='#4CAF50', fg='white', bd=2, relief=tk.FLAT, font=('Helvetica', 12, 'bold'))
        self.capture_button.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        # Create a button for selecting the save location
        self.select_folder_button = tk.Button(self.ui_frame, text="Select Save Location", command=self.select_save_location, bg='#007bff', fg='white', bd=2, relief=tk.FLAT, font=('Helvetica', 12, 'bold'))
        self.select_folder_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='we')

        # Create a label for displaying the live stream
        self.stream_label = tk.Label(root, bg='black')
        self.stream_label.pack(padx=10, pady=10)

        self.save_location = None
        self.start_stream()

    def start_stream(self):
        # Open webcam
        self.cap = cv2.VideoCapture(self.video_source)

        # Check if the webcam is opened successfully
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open webcam")
            return

        self.show_stream()

    def show_stream(self):
        _, frame = self.cap.read()

        # Convert the frame to a format that can be displayed by Tkinter
        photo = cv2_to_tkinter_photo(frame)

        # Display the frame in the Tkinter window
        self.stream_label.config(image=photo)
        self.stream_label.image = photo

        # Continue to display the stream by calling this method recursively
        self.root.after(10, self.show_stream)

    def capture_image(self):
        if not hasattr(self, 'cap') or not self.cap.isOpened():
            messagebox.showerror("Error", "Webcam not available")
            return

        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name")
            return

        if not self.save_location:
            messagebox.showerror("Error", "Please select a save location")
            return

        # Read the current frame from the webcam
        ret, frame = self.cap.read()

        # If frame is read correctly, save it
        if ret:
            # Save the captured image with the entered name to the selected location
            image_path = os.path.join(self.save_location, f"{name}.jpg")
            cv2.imwrite(image_path, frame)
            messagebox.showinfo("Success", f"Image saved as {image_path}")
        else:
            messagebox.showerror("Error", "Failed to capture image")

    def select_save_location(self):
        self.save_location = filedialog.askdirectory(title="Select Save Location")

def cv2_to_tkinter_photo(image):
    '''Convert an image from OpenCV format to tkinter format.'''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
    image = Image.fromarray(image)
    photo = ImageTk.PhotoImage(image=image)
    return photo

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveStreamCaptureApp(root)
    root.mainloop()

