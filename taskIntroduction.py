from tkhtmlview import HTMLScrolledText

class TaskIntroduction(HTMLScrolledText):
    def __init__(self, root, html):
        super(TaskIntroduction, self).__init__(root)
        self.config(state='disabled', width=1000)
        self.fit_height()
        self.get_html(html)

    def get_html(self, html):
        with open(html, 'r', encoding='utf-8') as f:
            content = f.read()
        self.set_html(html=content)