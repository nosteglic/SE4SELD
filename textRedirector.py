class TextRedirector(object):
    def __init__(self, widget, tag='stdout'):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert('end', str, (self.tag,))    # (self.tag,) 是设置配置
        self.widget.configure(state='disabled')

    def flush(self):
        pass