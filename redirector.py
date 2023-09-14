# 自定义ReText,用于将stdout映射到Queue
class ReText:
    def __init__(self, queue, tag_queue, tag):
        self.queue = queue
        self.tag_queue = tag_queue
        self.tag = tag

    def write(self, content):
        self.queue.put(content)
        self.tag_queue.put(self.tag)

    def flush(self):
        pass
