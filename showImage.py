from PIL import Image, ImageTk

def choosepic(path, widget):
    widget.update()
    if widget.find_withtag('canvas_image'):
        widget.delete('canvas_image')
    img_open = Image.open(path)
    resized = img_open.resize((widget.winfo_width(),widget.winfo_height()), Image.ANTIALIAS)
    # print(widget.winfo_width(),widget.winfo_height())
    img = ImageTk.PhotoImage(resized)
    # widget.config(image=img)
    widget.create_image(0, 0, image=img, anchor='nw', tags='canvas_image')
    widget.image = img  # keep a reference