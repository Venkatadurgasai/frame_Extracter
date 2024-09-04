import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
from threading import Thread
from tkinter.ttk import Progressbar

class VideoFrameExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame Extractor")

        self.input_file = None
        self.output_dir = None
        self.stop_flag = False

        self.create_widgets()

    def create_widgets(self):
        self.input_button = tk.Button(self.root, text="Select Video", command=self.select_input_file)
        self.input_button.pack(pady=10)

        self.output_button = tk.Button(self.root, text="Select Output Directory", command=self.select_output_dir)
        self.output_button.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_extraction)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_extraction)
        self.stop_button.pack(pady=10)

        self.progress = Progressbar(self.root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=10)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.mpg *.mpeg *.m4v")]
        )
        if self.input_file:
            messagebox.showinfo("Selected File", f"Input File: {self.input_file}")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Select Output Directory")
        if self.output_dir:
            messagebox.showinfo("Selected Directory", f"Output Directory: {self.output_dir}")

    def start_extraction(self):
        if not self.input_file or not self.output_dir:
            messagebox.showerror("Error", "Please select both input file and output directory.")
            return

        self.stop_flag = False
        self.thread = Thread(target=self.extract_frames)
        self.thread.start()

    def stop_extraction(self):
        self.stop_flag = True

    def extract_frames(self):
        cap = cv2.VideoCapture(self.input_file)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open video file.")
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.progress['maximum'] = total_frames

        frame_count = 0
        while cap.isOpened():
            if self.stop_flag:
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            output_path = os.path.join(self.output_dir, f"frame_{frame_count:05d}.png")
            cv2.imwrite(output_path, frame)

            self.progress['value'] = frame_count
            self.root.update_idletasks()

        cap.release()
        messagebox.showinfo("Done", "Frame extraction completed." if not self.stop_flag else "Frame extraction stopped.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFrameExtractor(root)
    root.mainloop()
