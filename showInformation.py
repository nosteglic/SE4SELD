import time
import tkinter as tk

'''==================================================
软件介绍/参考文献/作者信息
=================================================='''


class ShowInfomation(tk.Toplevel):
    def __init__(self, info_title=None, info_contents=None):
        super(ShowInfomation, self).__init__()

        self.last_callback_time = time.time()

        self.title(info_title)
        # 屏幕宽高
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # 弹窗宽高
        top_width = screen_width / 4
        top_height = screen_height / 4
        # 弹窗居中位移偏差
        bias_x = (screen_width - top_width) / 2
        bias_y = (screen_height - top_height) / 2
        # 弹窗位置和大小
        self.geometry(f'{int(top_width)}x{int(top_height)}+{int(bias_x)}+{int(bias_y)}')
        self.resizable(False, False)

        self.text = tk.Text(self, wrap='word')
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.text.insert(tk.END, info_contents)
        self.text.configure(state='disabled')

    #     self.canvas = tk.Canvas(self)
    #     self.info_frame = tk.Frame(self.canvas)
    #     self.scrollBar = tk.Scrollbar(self.canvas, orient='vertical', command=self.canvas.yview)
    #     self.canvas.configure(yscrollcommand=self.scrollBar.set)
    #
    #     self.canvas.pack(fill=tk.BOTH, expand=1)
    #     self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
    #
    #     self.canvas_frame = self.canvas.create_window((0, 0), window=self.info_frame, anchor="n")
    #     # self.info_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
    #     self.info_label = tk.Label(self.info_frame, text=info_contents, anchor='nw')
    #     self.info_label.pack(expand=1)
    #     self.bind("<Configure>", self.on_frame_configure)
    #     self.bind_all('<MouseWheel>', self.mouse_scroll)
    #     self.bind_all('<Button-4>', self.mouse_scroll)
    #     self.bind_all('<Button-5>', self.mouse_scroll)
    #
    # def mouse_scroll(self, event):
    #     if event.delta:
    #         self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    #         self.canvas.xview_scroll(int(-1 * (event.delta / 120)), 'units')
    #     else:
    #         if event.num == 5:
    #             move = 1
    #         else:
    #             move = -1
    #
    #         self.canvas.yview_scroll(move, 'units')
    #         self.canvas.xview_scroll(move, 'units')
    #
    # def on_frame_configure(self, event=None):
    #     self.canvas.configure(scrollregion=self.canvas.bbox("all"))
