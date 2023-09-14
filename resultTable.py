import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import csv
import tkinter.messagebox as msg

import strings

class ResultTable():
    def __init__(self, root, path):
        self.result_button_frame = tk.Frame(root)
        self.result_frame_2019 = tk.Frame(root)
        self.result_frame_2020 = tk.Frame(root)
        self.result_button_frame.pack(fill=tk.X, pady=(5,5), padx=(10,10))
        self.result_frame_2019.pack(fill=tk.BOTH)
        self.result_frame_2020.pack(fill=tk.BOTH)

        self.result_button_subframe_left = tk.Frame(self.result_button_frame)
        self.result_button_subframe_right = tk.Frame(self.result_button_frame)
        self.result_button_subframe_left.pack(side=tk.LEFT, fill=tk.BOTH,padx=(10,20))
        self.result_button_subframe_right.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0,10), expand=True)

        self.text = tk.Text(self.result_button_subframe_right, height=4)
        self.text.pack(expand=True, fill=tk.X)
        self.text.insert('end', strings.resultTableIntroduction)
        self.text.config(state='disabled', cursor='arrow', wrap='word')

        self.load_path = tk.StringVar(value=path)
        self.result_load_label = tk.Label(self.result_button_subframe_left, text='数据来源：')
        self.result_load_path = tk.Entry(self.result_button_subframe_left, width=20, textvar=self.load_path)
        self.result_load_choose = tk.Button(self.result_button_subframe_left,text='选择文件', command=self.select_path)
        self.result_load = tk.Button(self.result_button_subframe_left, text='导入数据', command=self.load_csv)

        self.save_path = tk.StringVar(value='default_name')
        self.result_save_label = tk.Label(self.result_button_subframe_left, text='导出到csv文件：')
        self.result_save_path = tk.Entry(self.result_button_subframe_left, width=20, textvar=self.save_path)
        self.result_save = tk.Button(self.result_button_subframe_left, text='导出数据', command=self.save_csv)

        self.result_load_label.grid(row=0, column=1, padx=5,sticky='w')
        self.result_load_path.grid(row=0, column=2, columnspan=2, padx=5)
        self.result_load_choose.grid(row=0, column=4, padx=5)
        self.result_load.grid(row=0, column=5, padx=5)
        self.result_save_label.grid(row=1, column=1, padx=5,sticky='w')
        self.result_save_path.grid(row=1, column=2, columnspan=2, padx=5)
        self.result_save.grid(row=1, column=4, padx=5)

        self.result_delete = tk.Button(self.result_button_subframe_left, text='清空数据', command=self.delete_all)
        self.result_delete.grid(row=1, column=5, padx=5)

        self.result_subframe_2019 = tk.Frame(self.result_frame_2019)
        self.result_label_2019 = tk.Label(self.result_frame_2019, text='2019年独立指标')

        self.result_table_dev_2019 = tk.Frame(self.result_frame_2019)
        self.result_foa_dev_2019 = ttk.Treeview(self.result_frame_2019, height=9)
        self.result_mic_dev_2019 = ttk.Treeview(self.result_frame_2019, height=9)

        self.result_table_eval_2019 = tk.Frame(self.result_frame_2019)
        self.result_foa_eval_2019 = ttk.Treeview(self.result_frame_2019, height=9)
        self.result_mic_eval_2019 = ttk.Treeview(self.result_frame_2019, height=9)

        self.result_subframe_2019.pack(fill=tk.X, pady=(5, 5))
        self.result_label_2019.pack(in_=self.result_subframe_2019, side=tk.LEFT, fill=tk.X, expand=True)

        self.result_table_dev_2019.pack(fill=tk.BOTH)
        self.result_foa_dev_2019.pack(in_=self.result_table_dev_2019, side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        self.result_mic_dev_2019.pack(in_=self.result_table_dev_2019, side=tk.LEFT, fill=tk.BOTH)

        self.result_table_eval_2019.pack(fill=tk.BOTH)
        self.result_foa_eval_2019.pack(in_=self.result_table_eval_2019, side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        self.result_mic_eval_2019.pack(in_=self.result_table_eval_2019, side=tk.LEFT, fill=tk.BOTH)

        self.result_subframe_2020 = tk.Frame(self.result_frame_2020)
        self.result_label_2020 = tk.Label(self.result_frame_2020, text='2020年联合指标')

        self.result_table_dev_2020 = tk.Frame(self.result_frame_2020)
        self.result_foa_dev_2020 = ttk.Treeview(self.result_frame_2020, height=9)
        self.result_mic_dev_2020 = ttk.Treeview(self.result_frame_2020, height=9)

        self.result_table_eval_2020 = tk.Frame(self.result_frame_2020)
        self.result_foa_eval_2020 = ttk.Treeview(self.result_frame_2020, height=9)
        self.result_mic_eval_2020 = ttk.Treeview(self.result_frame_2020, height=9)

        self.result_subframe_2020.pack(fill=tk.X, pady=(5, 5))
        self.result_label_2020.pack(in_=self.result_subframe_2020, side=tk.LEFT, fill=tk.X, expand=True)

        self.result_table_dev_2020.pack(fill=tk.BOTH)
        self.result_foa_dev_2020.pack(in_=self.result_table_dev_2020, side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        self.result_mic_dev_2020.pack(in_=self.result_table_dev_2020, side=tk.LEFT, fill=tk.BOTH)

        self.result_table_eval_2020.pack(fill=tk.BOTH)
        self.result_foa_eval_2020.pack(in_=self.result_table_eval_2020, side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        self.result_mic_eval_2020.pack(in_=self.result_table_eval_2020, side=tk.LEFT, fill=tk.BOTH)

        self.result_label_2019.config(bg='black', fg='white')
        self.result_label_2020.config(bg='black', fg='white')

        self.result_foa_dev_2019['columns'] = ('foa-dev', 'DE', 'FR', 'ER', 'F')
        self.result_mic_dev_2019['columns'] = ('mic-dev', 'DE', 'FR', 'ER', 'F')
        self.result_foa_eval_2019['columns'] = ('foa-eval', 'DE', 'FR', 'ER', 'F')
        self.result_mic_eval_2019['columns'] = ('mic-eval', 'DE', 'FR', 'ER', 'F')

        self.result_foa_dev_2020["columns"] = ('foa-dev', "LE_CD", "LR_CD", "ER_(20°)", "F_(20°)")
        self.result_mic_dev_2020["columns"] = ('mic-dev', "LE_CD", "LR_CD", "ER_(20°)", "F_(20°)")
        self.result_foa_eval_2020["columns"] = ('foa-eval', "LE_CD", "LR_CD", "ER_(20°)", "F_(20°)")
        self.result_mic_eval_2020["columns"] = ('mic-eval', "LE_CD", "LR_CD", "ER_(20°)", "F_(20°)")

        self.result_foa_dev_2019['show'] = 'headings'
        self.result_mic_dev_2019['show'] = 'headings'
        self.result_foa_eval_2019['show'] = 'headings'
        self.result_mic_eval_2019['show'] = 'headings'

        self.result_foa_dev_2020['show'] = 'headings'
        self.result_mic_dev_2020['show'] = 'headings'
        self.result_foa_eval_2020['show'] = 'headings'
        self.result_mic_eval_2020['show'] = 'headings'

        for widget in (self.result_foa_dev_2019, self.result_mic_dev_2019,
                       self.result_foa_eval_2019, self.result_mic_eval_2019,
                       self.result_foa_dev_2020, self.result_mic_dev_2020,
                       self.result_foa_eval_2020, self.result_mic_eval_2020):
            for column in widget["columns"]:
                widget.column(column, anchor='center', width='190')
                widget.heading(column, text=column)

    '''清空数据'''
    def delete_all(self):
        for widget in (self.result_foa_dev_2019, self.result_mic_dev_2019,
                       self.result_foa_eval_2019, self.result_mic_eval_2019,
                       self.result_foa_dev_2020, self.result_mic_dev_2020,
                       self.result_foa_eval_2020, self.result_mic_eval_2020):
            x = widget.get_children()
            for item in x:
                widget.delete(item)

    '''选择文件'''
    def select_path(self):
        path_ = filedialog.askopenfilename(initialdir='csv/')
        if path_:
            if '.csv' not in path_:
                flag = msg.askretrycancel('文件打开出错', '请选择csv格式文件')
                if flag:
                    self.select_path()
            else:
                self.load_path.set(path_)

    '''导入数据'''
    def load_csv(self):
        with open(self.load_path.get()) as myfile:
            csvread = csv.reader(myfile, delimiter=',')
            format = None
            date = None
            for row in csvread:
                # print('load row:', row)
                if len(row) == 2:
                    format = row[0]
                    date = row[1]
                    continue
                if format == 'dev-foa':
                    if date == '2019':
                        self.result_foa_dev_2019.insert("", 'end', values=row)
                    elif date == '2020':
                        self.result_foa_dev_2020.insert("", 'end', values=row)
                elif format == 'dev-mic':
                    if date == '2019':
                        self.result_mic_dev_2019.insert("", 'end', values=row)
                    elif date == '2020':
                        self.result_mic_dev_2020.insert("", 'end', values=row)
                elif format == 'eval-foa':
                    if date == '2019':
                        self.result_foa_eval_2019.insert("", 'end', values=row)
                    elif date == '2020':
                        self.result_foa_eval_2020.insert("", 'end', values=row)
                elif format == 'eval-mic':
                    if date == '2019':
                        self.result_mic_eval_2019.insert("", 'end', values=row)
                    elif date == '2020':
                        self.result_mic_eval_2020.insert("", 'end', values=row)

    '''导出数据'''
    def save_csv(self):
        path = 'csv/{}.csv'.format(self.save_path.get())
        try:
            with open(path, "w", newline='') as myfile:
                csvwriter = csv.writer(myfile, delimiter=',')
                for widget in (self.result_foa_dev_2019, self.result_foa_dev_2020,
                               self.result_mic_dev_2019, self.result_mic_dev_2020,
                               self.result_foa_eval_2019, self.result_foa_eval_2020,
                               self.result_mic_eval_2019, self.result_mic_eval_2020):
                    if widget == self.result_foa_dev_2019:csvwriter.writerow(['dev-foa','2019'])
                    elif widget == self.result_foa_dev_2020:csvwriter.writerow(['dev-foa','2020'])
                    elif widget == self.result_mic_dev_2019:csvwriter.writerow(['dev-mic','2019'])
                    elif widget == self.result_mic_dev_2020:csvwriter.writerow(['dev-mic','2020'])
                    elif widget == self.result_foa_eval_2019:csvwriter.writerow(['eval-foa','2019'])
                    elif widget == self.result_foa_eval_2020:csvwriter.writerow(['eval-foa','2020'])
                    elif widget == self.result_mic_eval_2019:csvwriter.writerow(['eval-mic','2019'])
                    elif widget == self.result_mic_eval_2020:csvwriter.writerow(['eval-mic','2020'])
                    for row_id in widget.get_children():
                        row = widget.item(row_id)['values']
                        # print('save row:', row)
                        csvwriter.writerow(row)
            msg.showinfo("数据保存成功", "数据已成功保存到{}".format(self.save_path.get()))
        except:
            msg.showerror('数据保存出错', '数据无法成功保存到{}'.format(self.save_path.get()))

# if __name__ == '__main__':
#     window=tk.Tk()
#     frame = tk.Frame(window)
#     test = ResultTable(frame, path='csv/default_name.csv')
#     frame.pack()
#     window.mainloop()
