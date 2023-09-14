import tkinter as tk
from PIL import Image, ImageTk

class ShowResultImage(tk.Toplevel):
    def __init__(self, root, path, use_polar_format, do_plot_3d):
        super(ShowResultImage, self).__init__(root)
        img_open = Image.open(path)
        img_width = img_open.size[0]
        img_height = img_open.size[1]

        resized_width = img_width // 8
        resized_height = img_height // 8

        self.title('显示结果图片')

        self.canvas = tk.Canvas(self, width=resized_width, height=resized_height)
        self.canvas.pack()

        self.canvas.update()
        if self.canvas.find_withtag('canvas_image'):
            self.canvas.delete('canvas_image')
        resized = img_open.resize((self.canvas.winfo_width(),self.canvas.winfo_height()), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        # widget.config(image=img)
        self.canvas.create_image(0, 0, image=img, anchor='nw', tags='canvas_image')
        self.canvas.image = img  # keep a reference


