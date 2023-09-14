import ctypes
import inspect
import os
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msg

import batch_feature_extraction
import resultTable
import seld
import showResultImage
import strings
import parameter
import showInformation
import redirector

import queue
import sys

import taskIntroduction
import threadMethod
import visualize_SELD_output

'''==================================================
窗口window
=================================================='''
count = 0

class MainWindow(tk.Tk):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.last_callback_time = time.time()

        # new 一个Quue用于保存输出内容
        self.msg_queue = queue.Queue()
        self.tag_queue = queue.Queue()

        self.params = parameter.Parameters()

        '''==================================================
        窗口
        =================================================='''
        '''定义窗口标题'''
        self.title('本科毕业设计-沈雅馨-基于双域注意力机制的声音事件定位与检测系统设计与实现')
        '''定义窗口尺寸'''
        # 屏幕宽高
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # 窗口宽高
        self.win_width = screen_width // 2 + 100
        self.win_height = screen_height // 2 + 350
        # 窗口居中位移偏差
        bias_x = (screen_width - self.win_width) // 2
        bias_y = (screen_height - self.win_height) // 2 - 50
        # 弹窗位置和大小
        self.geometry(f'{int(self.win_width)}x{int(self.win_height)}+{int(bias_x)}+{int(bias_y)}')
        # self.resizable(False,False)
        self.bind('<Configure>', self.update_current_size)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        '''==================================================
        菜单栏
        =================================================='''
        self.menuBar = tk.Menu(self)
        # 子菜单
        # self.menuTest = tk.Menu(self.menuBar, tearoff=0)
        self.menuInfo = tk.Menu(self.menuBar, tearoff=0)
        self.menuInfo.add_command(label='软件介绍', command=self.show_software_introduction)
        self.menuInfo.add_command(label='参考文献', command=self.show_references)
        self.menuInfo.add_command(label='作者信息', command=self.show_my_infomation)
        # self.menuInfo.add_command(label='问题反馈', command=self.submit_questions)
        # 往主菜单添加子菜单
        # self.menuBar.add_cascade(label='仅做界面测试', menu=self.menuTest)
        self.menuBar.add_cascade(label='更多信息', menu=self.menuInfo)
        self.menuBar.add_command(label='显示预设模型信息', command=self.show_modelInfo)
        self.config(menu=self.menuBar)

        '''==================================================
        notebook
        =================================================='''
        self.win_flag = 0
        self.start_flag = 0
        self.temp_width = self.win_width
        self.temp_height = self.win_height
        self.current_height = 0
        self.current_width = 0
        self.noteBook = ttk.Notebook(self)
        self.SED_tab = tk.Frame(self.noteBook)
        self.DOA_tab = tk.Frame(self.noteBook)
        self.SELD_tab = tk.Frame(self.noteBook)
        self.scSE_tab  =tk.Frame(self.noteBook)
        self.modelTrain_tab = tk.Frame(self.noteBook)
        self.resultTable_tab = tk.Frame(self.noteBook)

        self.noteBook.add(self.SED_tab, text='SED介绍')
        self.noteBook.add(self.DOA_tab, text='DOA介绍')
        self.noteBook.add(self.SELD_tab, text='SELD介绍')
        self.noteBook.add(self.scSE_tab, text='scSE介绍')
        self.noteBook.add(self.modelTrain_tab, text='模型训练与预测')
        self.noteBook.add(self.resultTable_tab, text='结果表格')
        self.noteBook.pack(fill=tk.BOTH, expand=1)
        self.noteBook.select(self.modelTrain_tab)

        '''==================================================
        SED_tab DOA_tab SELD_tab scSE_tab
        =================================================='''
        self.SED_introduction = taskIntroduction.TaskIntroduction(self.SED_tab, 'htmls\SED.html')
        self.SED_introduction.pack(fill=tk.BOTH)

        self.DOA_introduction = taskIntroduction.TaskIntroduction(self.DOA_tab, 'htmls\DOA.html')
        self.DOA_introduction.pack(fill=tk.BOTH)

        self.SELD_introduction = taskIntroduction.TaskIntroduction(self.SELD_tab, 'htmls\SELD.html')
        self.SELD_introduction.pack(fill=tk.BOTH)

        self.scSE_introduction = taskIntroduction.TaskIntroduction(self.scSE_tab, 'htmls\scSE.html')
        self.scSE_introduction.pack(fill=tk.BOTH)

        '''==================================================
        resultTable_tab
        =================================================='''
        self.table_path = tk.StringVar(value='csv/default_name.csv')
        self.result_tables = resultTable.ResultTable(self.resultTable_tab, path=self.table_path.get())

        '''==================================================
        modelTrain_tab
        =================================================='''
        '''定义框架'''
        self.model_left_frame = tk.Frame(self.modelTrain_tab, width=self.win_width // 2)
        self.model_right_frame = tk.Frame(self.modelTrain_tab, width=self.win_width // 2)
        self.model_left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.model_right_frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        '''
        self.model_left_frame中的内容
        '''
        self.model_left_frame_sub1 = tk.Frame(self.model_left_frame)
        self.model_left_frame_sub1.pack()
        self.model_left_frame_sub2 = tk.Frame(self.model_left_frame)
        self.model_left_frame_sub2.pack()
        self.model_left_frame_sub3 = tk.Frame(self.model_left_frame)
        self.model_left_frame_sub3.pack()

        '''路径/数据集相关'''
        i = 0
        self.model_dir_label = tk.Label(self.model_left_frame_sub1,
                                        text='--------------------【路径相关设置】-------------------------')
        self.model_dir_label.grid(row=i, column=0, columnspan=5, pady=5)
        # dataset_dir
        i += 1
        self.model_dataset_dir = tk.StringVar(value='/Datasets/')
        self.model_datasetDir_label = tk.Label(self.model_left_frame_sub1, text='数据集根目录：')
        self.model_datasetDir_entry = tk.Entry(self.model_left_frame_sub1, textvar=self.model_dataset_dir)
        self.model_datasetDir_button = tk.Button(self.model_left_frame_sub1, text='选择路径',
                                                 command=lambda: self.select_path(self.model_dataset_dir))
        self.model_datasetDir_default_button = tk.Button(self.model_left_frame_sub1, text='恢复默认',
                                                         command=lambda:
                                                         self.set_string_var(self.model_dataset_dir, '/Datasets/')
                                                         )
        self.model_datasetDir_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_datasetDir_entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_datasetDir_button.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.model_datasetDir_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')
        # feat_label_dir
        i += 1
        self.model_feat_label_dir = tk.StringVar(value='/Datasets/feat_label/')
        self.model_featExtraction_label = tk.Label(self.model_left_frame_sub1, text='特征标签路径：')
        self.model_featExtraction_entry = tk.Entry(self.model_left_frame_sub1, textvar=self.model_feat_label_dir)
        self.model_featExtraction_button = tk.Button(self.model_left_frame_sub1, text='选择路径',
                                                     command=lambda: self.select_path(self.model_feat_label_dir))
        self.model_featExtraction_default_button = tk.Button(self.model_left_frame_sub1, text='恢复默认',
                                                             command=lambda:
                                                             self.set_string_var(self.model_feat_label_dir,
                                                                                 '/Datasets/feat_label/'))
        self.model_featExtraction_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_featExtraction_entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_featExtraction_button.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.model_featExtraction_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        # model_dir
        i += 1
        self.model_model_dir = tk.StringVar(value='models/')
        self.model_modelDir_label = tk.Label(self.model_left_frame_sub1, text='模型保存路径：')
        self.model_modelDir_entry = tk.Entry(self.model_left_frame_sub1, textvar=self.model_model_dir)
        self.model_modelDir_button = tk.Button(self.model_left_frame_sub1, text='选择路径',
                                               command=lambda: self.select_path(self.model_model_dir))
        self.model_modelDir_default_button = tk.Button(self.model_left_frame_sub1, text='恢复默认',
                                                       command=lambda:
                                                       self.set_string_var(self.model_model_dir, 'models/'))
        self.model_modelDir_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_modelDir_entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_modelDir_button.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.model_modelDir_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        # model_name
        i += 1
        self.model_model_name = tk.StringVar(value='default_name')
        self.model_modelName_label = tk.Label(self.model_left_frame_sub1, text='定义模型名称：')
        self.model_modelName_entry = tk.Entry(self.model_left_frame_sub1, textvar=self.model_model_name)
        self.model_modelName_default_button = tk.Button(self.model_left_frame_sub1, text='恢复默认',
                                                        command=lambda:
                                                        self.set_string_var(self.model_model_name, 'default_name'))
        self.model_modelName_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_modelName_entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_modelName_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        # dcase_output
        i += 1
        self.model_dcase_output = tk.BooleanVar(value=True)
        self.model_dcaseOutput_label = tk.Label(self.model_left_frame_sub1, text='是否保存结果：')
        self.model_true_ratioButton = ttk.Radiobutton(self.model_left_frame_sub1, text='是',
                                                      variable=self.model_dcase_output, value=True)
        self.model_false_ratioButton = ttk.Radiobutton(self.model_left_frame_sub1, text='否',
                                                       variable=self.model_dcase_output, value=False)
        self.model_dcaseOutput_default_button = tk.Button(self.model_left_frame_sub1, text='恢复默认',
                                                          command=lambda:
                                                          self.set_string_var(self.model_dcase_output, True))
        self.model_dcaseOutput_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_true_ratioButton.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_false_ratioButton.grid(row=i, column=2, padx=5, pady=5, sticky='w')
        self.model_dcaseOutput_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')
        # dcase_dir
        i += 1
        self.model_dcase_dir = tk.StringVar(value='results/')
        self.model_dcaseDir_label = tk.Label(self.model_left_frame_sub1, text='结果保存路径：')
        self.model_dcaseDir_entry = tk.Entry(self.model_left_frame_sub1, textvar=self.model_dcase_dir)
        self.model_dcaseDir_button = tk.Button(self.model_left_frame_sub1, text='选择路径',
                                               command=lambda: self.select_path(self.model_dcase_dir))
        self.model_dcaseDir_default_button = tk.Button(self.model_left_frame_sub1, text='恢复默认',
                                                       command=lambda:
                                                       self.set_string_var(self.model_dcase_dir, 'results/'))
        self.model_dcaseDir_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_dcaseDir_entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_dcaseDir_button.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.model_dcaseDir_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        '''正式训练相关'''
        i = 0
        self.model_train_Label = tk.Label(self.model_left_frame_sub2,
                                          text='--------------------【训练相关设置】-------------------------')
        self.model_train_Label.grid(row=i, column=0, columnspan=5, pady=5)

        # mode
        i += 1
        self.model_mode = tk.StringVar(value='dev')
        self.model_mode_label = tk.Label(self.model_left_frame_sub2, text='选择训练模式：')
        self.model_dev_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='dev',
                                                     variable=self.model_mode, value='dev')
        self.model_eval_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='eval',
                                                      variable=self.model_mode, value='eval')
        self.model_mode_default_button = tk.Button(self.model_left_frame_sub2, text='恢复默认',
                                                   command=lambda: self.set_string_var(self.model_mode, 'dev'))
        self.model_mode_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_dev_ratioButton.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_eval_ratioButton.grid(row=i, column=2, padx=5, pady=5, sticky='w')
        self.model_mode_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')
        # dataset
        i += 1
        self.model_format = tk.StringVar(value='foa')
        self.model_dataset_label = tk.Label(self.model_left_frame_sub2, text='选择数据格式：')
        self.model_foa_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='foa',
                                                     variable=self.model_format, value='foa')
        self.model_mic_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='mic',
                                                     variable=self.model_format, value='mic')
        self.model_format_default_button = tk.Button(self.model_left_frame_sub2, text='恢复默认',
                                                     command=lambda: self.set_string_var(self.model_format, 'foa'))
        self.model_dataset_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_foa_ratioButton.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_mic_ratioButton.grid(row=i, column=2, padx=5, pady=5, sticky='w')
        self.model_format_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        # batch_size
        i += 1
        self.model_batch_size = tk.IntVar(value=32)
        self.model_batchSize_label = tk.Label(self.model_left_frame_sub2, text='batch size ：')
        self.model_batchSize_combo = ttk.Combobox(self.model_left_frame_sub2)
        self.model_batchSize_combo['value'] = (16, 32, 128, 256)
        self.model_batchSize_combo.current(1)
        self.model_batchSize_combo.bind('<<ComboboxSelected>>', self.get_combo_batch)
        self.model_batchSize_default_button = tk.Button(self.model_left_frame_sub2, text='恢复默认',
                                                        command=self.set_combo_batch)
        self.model_batchSize_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_batchSize_combo.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_batchSize_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        # do_baseline
        i += 1
        self.model_do_baseline = tk.BooleanVar(value=False)
        self.model_baseline_label = tk.Label(self.model_left_frame_sub2, text='是否baseline：')
        self.model_do_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='baseline',
                                                    variable=self.model_do_baseline, value=True,
                                                    command=self.baseline_am)
        self.model_not_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='residual',
                                                     variable=self.model_do_baseline, value=False,
                                                     command=self.baseline_am)
        self.model_baseline_default_button = tk.Button(self.model_left_frame_sub2, text='恢复默认',
                                                       command=lambda:
                                                       self.set_string_var(self.model_do_baseline, True))
        self.model_baseline_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_do_ratioButton.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_not_ratioButton.grid(row=i, column=2, padx=5, pady=5, sticky='w')
        self.model_baseline_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')
        # am
        i += 1
        self.model_am = tk.StringVar(value='scSE')
        self.model_am_label = tk.Label(self.model_left_frame_sub2, text='注意力机制：')
        self.model_scSE_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='scSE',
                                                      variable=self.model_am, value='scSE',
                                                      command=self.baseline_am)
        self.model_cSE_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='cSE',
                                                     variable=self.model_am, value='cSE',
                                                     command=self.baseline_am)
        self.model_sSE_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='sSE',
                                                     variable=self.model_am, value='sSE',
                                                     command=self.baseline_am)
        self.model_noAm_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='无',
                                                     variable=self.model_am, value='FFF',
                                                      command=self.baseline_am)
        self.model_am_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_scSE_ratioButton.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_cSE_ratioButton.grid(row=i, column=2, padx=5, pady=5, sticky='w')
        self.model_sSE_ratioButton.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.model_noAm_ratioButton.grid(row=i, column=4, padx=5, pady=5, sticky='w')
        # res
        i += 1
        self.model_res = tk.StringVar(value='post')
        self.model_res_label = tk.Label(self.model_left_frame_sub2, text='am的位置：')
        self.model_main_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='主干',
                                                      variable=self.model_res, value='main')
        self.model_shortcut_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='分支',
                                                          variable=self.model_res, value='shorcut')
        self.model_post_ratioButton = ttk.Radiobutton(self.model_left_frame_sub2, text='POST',
                                                      variable=self.model_res, value='post')
        self.model_res_default_button = tk.Button(self.model_left_frame_sub2, text='恢复默认',
                                                  command=lambda: self.set_string_var(self.model_res, 'post'))
        self.model_res_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_post_ratioButton.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_shortcut_ratioButton.grid(row=i, column=2, padx=5, pady=5, sticky='w')
        self.model_main_ratioButton.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.model_res_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')
        # ratio
        i += 1
        self.model_ratio = tk.IntVar(value=4)
        self.model_ratio_label = tk.Label(self.model_left_frame_sub2, text='降维比例ratio：')
        self.model_ratio_combo = ttk.Combobox(self.model_left_frame_sub2)
        self.model_ratio_combo['value'] = (1, 2, 4, 8, 16)
        self.model_ratio_combo.current(2)
        self.model_ratio_combo.bind('<<ComboboxSelected>>', self.get_combo_ratio)
        self.model_ratio_default_button = tk.Button(self.model_left_frame_sub2, text='恢复默认',
                                                    command=self.set_combo_ratio)
        self.model_ratio_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_ratio_combo.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_ratio_default_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        # 结果图示模式
        i = 0
        self.model_resultView_label = tk.Label(self.model_left_frame_sub3,
                                               text='--------------------【显示训练结果】-------------------------')
        self.model_resultView_label.grid(row=i, column=0, columnspan=5, pady=5)
        i += 1
        self.model_result_left_frame = tk.Frame(self.model_left_frame_sub3)
        self.model_result_right_frame = tk.Frame(self.model_left_frame_sub3)
        self.model_result_left_frame.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_result_right_frame.grid(row=i, column=1, columnspan=4, padx=5, pady=5, sticky='w')

        self.result_sed = tk.BooleanVar(value=True)
        self.model_sed_ratioButton = ttk.Radiobutton(self.model_result_left_frame, text='SED',
                                                     variable=self.result_sed, value=True,
                                                     command=self.sed_doa)
        self.model_doa_ratioButton = ttk.Radiobutton(self.model_result_left_frame, text='DOA',
                                                     variable=self.result_sed, value=False,
                                                     command=self.sed_doa)
        self.model_sed_ratioButton.grid(row=0, padx=15, pady=5)
        self.model_doa_ratioButton.grid(row=1, padx=16, pady=5)

        i = 0
        self.model_dimension = tk.BooleanVar(value=True)
        self.model_dimension_label = tk.Label(self.model_result_right_frame, text='选择图片维度：')
        self.model_2d_radio = tk.Radiobutton(self.model_result_right_frame, text='2d',
                                              variable=self.model_dimension, value=False, state='disabled')
        self.model_3d_radio = tk.Radiobutton(self.model_result_right_frame, text='3d',
                                              variable=self.model_dimension, value=True, state='disabled')
        self.model_dimension_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_2d_radio.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_3d_radio.grid(row=i, column=2, padx=5, pady=5, sticky='w')
        i += 1
        self.model_coordinate = tk.BooleanVar(value=False)
        self.model_coordinate_label = tk.Label(self.model_result_right_frame, text='选择坐标模式：')
        self.model_polar_radio = tk.Radiobutton(self.model_result_right_frame, text='polar',
                                              variable=self.model_coordinate, value=True, state='disabled')
        self.model_cartesian_radio = tk.Radiobutton(self.model_result_right_frame, text='cartesian',
                                              variable=self.model_coordinate, value=False, state='disabled')
        self.model_coordinate_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_polar_radio.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_cartesian_radio.grid(row=i, column=2, padx=5, pady=5, sticky='w')

        i += 1
        self.result_path = tk.StringVar()
        self.result_path.set('default_name_foa_dev/fold1_room1_mix002_ov1.csv')
        self.model_resultPath_label = tk.Label(self.model_left_frame_sub3, text='结果图的文件：')
        self.model_resultPath_entry = tk.Entry(self.model_left_frame_sub3, textvar=self.result_path)
        self.model_resultPath_button = tk.Button(self.model_left_frame_sub3, text='选择文件',
                                                 command=self.get_result_file)
        self.model_resultShow_button = tk.Button(self.model_left_frame_sub3, text='显示结果',
                                                 command=self.show_result)
        self.model_resultPath_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_resultPath_entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_resultPath_button.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.model_resultShow_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        '''
        self.right_frame
        '''
        # tk.Text update()
        # tk.Label

        self.model_right_frame_sub1 = tk.Frame(self.model_right_frame)
        self.model_right_frame_sub2 = tk.Frame(self.model_right_frame)
        self.model_right_frame_sub3 = tk.Frame(self.model_right_frame)
        self.model_right_frame_sub4 = tk.Frame(self.model_right_frame)
        self.model_right_frame_sub1.pack()
        self.model_right_frame_sub2.pack()
        self.model_right_frame_sub3.pack()
        self.model_right_frame_sub4.pack()

        # start training
        i = 0
        self.model_start_Label = tk.Label(self.model_right_frame_sub1,
                                          text='--------------------【启动模型运行】-------------------------')
        self.model_start_Label.grid(row=i, column=0, columnspan=5, padx=(40, 0), pady=5)
        # process_str
        i += 1
        self.model_process_str = tk.StringVar(value='dev,eval')
        self.model_processStr_label = tk.Label(self.model_right_frame_sub1, text='若还未进行特征提取（dev + eval），请点击这个按钮：')
        self.model_processStr_button = tk.Button(self.model_right_frame_sub1, text='特征提取',
                                                 command=self.confirm_extraction)
        self.model_processStr_label.grid(row=i, column=0, columnspan=4, padx=5, pady=5, sticky='w')
        self.model_processStr_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')
        i += 1
        self.model_start_mode = tk.BooleanVar()
        self.model_start_mode.set(False)
        self.model_startMode_label = tk.Label(self.model_right_frame_sub1, text='选择启动模式：')
        self.model_test_ratiobutton = ttk.Radiobutton(self.model_right_frame_sub1, text='测试',
                                                      variable=self.model_start_mode, value=True)
        self.model_normal_ratioButton = ttk.Radiobutton(self.model_right_frame_sub1, text='正常',
                                                        variable=self.model_start_mode, value=False)
        self.model_startMode_label.grid(row=i, column=0, padx=(5, 25), pady=5, sticky='w')
        self.model_normal_ratioButton.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        self.model_test_ratiobutton.grid(row=i, column=2, padx=5, pady=5, sticky='w')

        self.model_start_button = tk.Button(self.model_right_frame_sub1, text='启动/停止', command=self.start_stop)
        self.model_start_button.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.thread_pool = []

        self.model_clipboard_button = tk.Button(self.model_right_frame_sub1, text='复制记录',
                                                command=self.copy_to_clipboard)
        self.model_clipboard_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        # loss_image
        self.model_lossImage_path = tk.StringVar()
        self.model_lossImage_canvas = tk.Canvas(self.model_right_frame_sub2, bg='lightgrey',
                                                width=self.win_width // 2, height=self.win_height // 2 - 90)
        self.model_lossImage_canvas.create_text(0, self.win_height // 4 - 45,
                                                text='此处显示loss训练图像', anchor=tk.NW, tags='canvas_text')
        self.model_lossImage_canvas.pack()
        # text
        self.model_TrainProcess_text = tk.Text(self.model_right_frame_sub3, bg='white', wrap='word',
                                               width=self.win_width // 2, height=16)

        self.model_TrainProcess_text.tag_configure('stderr', foreground='#b22222')
        self.model_text_scrollbar = tk.Scrollbar(self.model_right_frame_sub3)
        self.model_text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.model_text_scrollbar.config(command=self.model_TrainProcess_text.yview)
        self.model_TrainProcess_text.config(yscrollcommand=self.model_text_scrollbar.set)
        self.model_TrainProcess_text.pack()
        # predict
        # 结果图示模式
        i = 0
        self.model_predict_label = tk.Label(self.model_right_frame_sub4,
                                               text='--------------------【直接预测结果】-------------------------')
        self.model_predict_label.grid(row=i, column=0, columnspan=5, pady=5)

        i += 1
        self.model_path = tk.StringVar()
        self.model_path.set('models\default_name_foa_dev_split1_model.h5')
        self.model_modelPath_label = tk.Label(self.model_right_frame_sub4, text='模型.h5文件：')
        self.model_modelPath_entry = tk.Entry(self.model_right_frame_sub4, textvar=self.model_path)
        self.model_modelPath_button = tk.Button(self.model_right_frame_sub4, text='选择文件',
                                                 command=self.get_model_file)
        self.model_predict_button = tk.Button(self.model_right_frame_sub4, text='进行预测',
                                                 command=self.predict_result)
        self.model_modelPath_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        self.model_modelPath_entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.model_modelPath_button.grid(row=i, column=3, padx=5, pady=5, sticky='w')
        self.model_predict_button.grid(row=i, column=4, padx=5, pady=5, sticky='w')

        # 启动after方法
        self.after(100, self.show_msg)

        # 将stdout映射到re_Text
        sys.stdout = redirector.ReText(self.msg_queue, self.tag_queue, 'stdout')
        sys.stderr = redirector.ReText(self.msg_queue, self.tag_queue, 'stderr')

    '''关闭主窗口，同时结束子线程'''
    def close_window(self):
        flag = msg.askokcancel('关闭窗口确认', '是否确认关闭整个窗口？')
        if flag:
            if self.thread_pool:
                for i in self.thread_pool:
                    threadMethod.stop_thread(i)
                    time.sleep(1)
                    self.thread_pool.remove(i)
            self.destroy()

    '''获取需要显示结果图的文件'''
    def get_result_file(self):
        self.params.set_dcase_dir(self.model_dcase_dir.get())
        dcase_dir = self.params.get_dcase_dir()
        path_ = filedialog.askopenfilename(initialdir=dcase_dir)
        if path_:
            if '.csv' not in path_:
                flag = msg.askretrycancel('文件打开出错', '请选择csv文件格式的数据')
                if flag:
                    self.get_result_file()
                else:
                    msg.showinfo('确认', '请确认现在待显示结果的文件为{}'.format(self.result_path.get()))
            else:
                self.result_path.set(path_)
                msg.showinfo('确认', '请确认现在待显示结果的文件为{}'.format(self.result_path.get()))
                self.show_result()

    '''获取需要的模型文件'''
    def get_model_file(self):
        self.params.set_model_dir(self.model_model_dir.get())
        model_dir = self.params.get_model_dir()
        path_ = filedialog.askopenfilename(initialdir=model_dir)
        if path_:
            if '.h5' not in path_:
                flag = msg.askretrycancel('文件打开出错', '请选择h5文件格式的数据')
                if flag:
                    self.get_model_file()
                else:
                    msg.showinfo('确认', '请确认现在选择的模型为{}'.format(self.model_path.get()))
            else:
                self.model_path.set(path_)
                msg.showinfo('确认', '请确认现在选择的模型为{}'.format(self.model_path.get()))
                self.model_start_button.config(state='disabled')

    ''' 模型预测'''
    def predict_result(self):
        self.set_thread(flag='predict')

    ''' 确认特征提取'''
    def confirm_extraction(self):
        path = self.params.get_model_dir()
        flag = msg.askokcancel('确认信息', '确认进行特征提取？将保存在{}，请确保该目录下有zip文件'.format(path))
        if flag:
            self.set_thread(flag='extraction')

    '''创建并启动子线程'''
    def set_thread(self, flag=None):
        self.model_TrainProcess_text.delete(1.0, tk.END)
        self.model_lossImage_canvas.update()
        if self.model_lossImage_canvas.find_withtag('canvas_image'):
            self.model_lossImage_canvas.delete('canvas_image')
        if not self.thread_pool:
            T = None
            if flag=='predict':
                T = threading.Thread(target=self.__predict)
            elif flag=='extraction':
                T = threading.Thread(target=self.__extraction)
            else:
                T = threading.Thread(target=self.__show)
            self.thread_pool.append(T)
        for i in self.thread_pool:
            i.start()

    '''启动训练'''
    def start_stop(self):
        self.model_TrainProcess_text.delete(1.0, tk.END)
        self.model_lossImage_canvas.update()
        if self.model_lossImage_canvas.find_withtag('canvas_image'):
            self.model_lossImage_canvas.delete('canvas_image')
        self.start_flag = not self.start_flag
        if self.start_flag:
            self.set_thread()
        else:
            if self.thread_pool:
                for i in self.thread_pool:
                    threadMethod.stop_thread(i)
                    time.sleep(1)
                    self.thread_pool.remove(i)
                    msg.showinfo('终止训练', '模型训练已终止')
                    self.model_predict_button.config(state='normal')
                    self.model_processStr_button.config(state='normal')

    '''训练模块显示信息'''
    def __show(self):
        self.model_predict_button.config(state='disabled')
        self.model_processStr_button.config(state='disabled')
        params_dict = self.get_params_dict()
        # 显示参数信息
        for key, value in params_dict.items():
            textvar = "{}: {}".format(key, value)
            self.model_TrainProcess_text.insert('insert', textvar + '\n')
            self.model_TrainProcess_text.update()
        path_ = 'csv/{}.csv'.format(params_dict['model_name'])
        self.table_path.set(path_)
        model_name = seld.train(params_dict=params_dict, widget=self.model_lossImage_canvas)
        for i in self.thread_pool:
            self.thread_pool.remove(i)
        self.start_flag = not self.start_flag
        self.model_predict_button.config(state='normal')
        self.model_processStr_button.config(state='normal')
        msg.showinfo('训练完成', '训练已成功完成')
        self.result_path.set('{}_{}_{}/fold1_room1_mix002_ov1.csv'.format(params_dict['model_name'],
                                                                          params_dict['dataset'],
                                                                          params_dict['mode']))
        self.model_path.set(model_name)

    '''特征提取子线程'''
    def __extraction(self):
        self.model_start_button.config(state='disabled')
        self.model_predict_button.config(state='disabled')
        params_dict = self.get_params_dict()
        batch_feature_extraction.FeatureExtraction(params_dict=params_dict)
        for i in self.thread_pool:
            self.thread_pool.remove(i)
        msg.showinfo('特征提取','特征提取已完成')
        self.model_start_button.config(state='normal')
        self.model_predict_button.config(state='normal')

    '''模型预测子线程'''
    def __predict(self):
        params_dict = self.get_params_dict()
        self.model_modelPath_button.config(state='disabled')
        self.model_processStr_button.config(state='disabled')
        self.model_start_button.config(state='disabled')
        seld.predict(params_dict=params_dict, path=self.model_path.get())
        for i in self.thread_pool:
            self.thread_pool.remove(i)
        msg.showinfo('预测完成','模型预测已完成')
        self.model_start_button.config(state='normal')
        self.model_processStr_button.config(state='normal')
        self.model_modelPath_button.config(state='normal')

    '''获取参数'''
    def get_params_dict(self):
        self.params.set_dir(model_dataset_dir=self.model_dataset_dir.get(),
                            model_feat_label_dir=self.model_feat_label_dir.get(),
                            model_model_dir=self.model_model_dir.get(),
                            model_dcase_dir=self.model_dcase_dir.get(),
                            model_mode=self.model_mode.get(),
                            model_format=self.model_format.get(),
                            model_dcase_output=self.model_dcase_output.get(),
                            model_quick_test=self.model_start_mode.get(),
                            model_model_name=self.model_model_name.get())
        self.params.set_model(model_batch_size=self.model_batch_size.get(),
                              model_do_baseline=self.model_do_baseline.get(),
                              model_am=self.model_am.get(),
                              model_ratio=self.model_ratio.get(),
                              model_res=self.model_res.get())
        params_dict = self.params.get_params()
        return params_dict

    '''显示结果图'''
    def show_result(self):
        params_dict = self.get_params_dict()
        path = self.result_path.get()
        mode = 'dev'
        dataset = 'foa'
        if 'eval' in path:
            mode = 'eval'
        if 'mic' in path:
            dataset = 'mic'
        path = visualize_SELD_output.visidualize_output(params_dict=params_dict, is_sed=self.result_sed.get(),
                                                        path=path, mode=mode, dataset=dataset,
                                                        use_polar_format=self.model_coordinate.get(),
                                                        do_plot_3d=self.model_dimension.get())
        showResultImage.ShowResultImage(self, path=path, use_polar_format=self.model_coordinate.get(),
                                        do_plot_3d=self.model_dimension.get())

    '''自适应窗口'''
    def update_current_size(self, event=None):
        cur_time = time.time()
        if (cur_time - self.last_callback_time) > 0.6:
            self.current_width = self.winfo_width()
            self.current_height = self.winfo_height()
            if self.temp_width != self.current_width:
                self.win_flag = not self.win_flag
                # print(self.win_flag)
                self.temp_width = self.current_width
                self.temp_height = self.current_height
                if self.model_lossImage_canvas:
                    if self.win_flag:
                        self.model_lossImage_canvas.config(width=self.current_width // 2, height=self.current_height // 2 - 110)
                        self.model_TrainProcess_text.config(width=self.win_width // 2, height=21)
                    else:
                        self.model_lossImage_canvas.config(width=self.current_width // 2, height=self.current_height // 2 - 110)
                        self.model_TrainProcess_text.config(width=self.win_width // 2, height=16)
                self.last_callback_time = time.time()

    '''
    设置和获取combo值
    '''
    def get_combo_batch(self, event):
        self.model_batch_size.set(self.model_batchSize_combo.get())

    def set_combo_batch(self, event=None):
        self.model_batchSize_combo.current(1)
        self.model_batch_size.set(32)

    def get_combo_ratio(self, event):
        self.model_ratio.set(self.model_ratio_combo.get())

    def set_combo_ratio(self, event=None):
        self.model_ratio_combo.current(2)
        self.model_ratio.set(4)

    '''选择文件夹'''
    def select_path(self, path):
        path_ = filedialog.askdirectory()
        path.set(path_)

    '''设置字符串变量值'''
    @staticmethod
    def set_string_var(stringvar, value):
        stringvar.set(value)

    '''在show_msg方法里，从Queue取出元素，输出到Text'''
    def show_msg(self):
        while not self.msg_queue.empty():
            content = self.msg_queue.get()
            tag = self.tag_queue.get()
            self.model_TrainProcess_text.insert(tk.INSERT, content, (tag,))
            self.model_TrainProcess_text.see(tk.END)

        # after方法再次调用show_msg
        self.after(100, self.show_msg)

    '''
    radiobutton状态调整
    '''
    def sed_doa(self):
        if self.result_sed.get():
            self.model_2d_radio.config(state='disabled')
            self.model_3d_radio.config(state='disabled')
            self.model_cartesian_radio.config(state='disabled')
            self.model_polar_radio.config(state='disabled')
        else:
            self.model_2d_radio.config(state='normal')
            self.model_3d_radio.config(state='normal')
            self.model_cartesian_radio.config(state='normal')
            self.model_polar_radio.config(state='normal')

    def baseline_am(self):
        if self.model_do_baseline.get() or self.model_am.get()=='FFF':
            self.model_main_ratioButton.config(state='disabled')
            self.model_post_ratioButton.config(state='disabled')
            self.model_shortcut_ratioButton.config(state='disabled')
        else:
            self.model_main_ratioButton.config(state='normal')
            self.model_post_ratioButton.config(state='normal')
            self.model_shortcut_ratioButton.config(state='normal')

    '''剪贴板'''
    def copy_to_clipboard(self):
        root = self.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(self.model_TrainProcess_text.get(1.0, tk.END))
        msg.showinfo("Copied Successfully", "Text copied to clipboard")

    '''
    其他信息模块显示
    '''
    @staticmethod
    def show_software_introduction():
        showInformation.ShowInfomation('软件介绍', strings.software_introduction)

    @staticmethod
    def show_references():
        showInformation.ShowInfomation('参考文献', strings.references)

    @staticmethod
    def show_my_infomation():
        showInformation.ShowInfomation('作者信息', strings.my_infomation)

    # @staticmethod
    # def submit_questions():
    #     showInformation.ShowInfomation('问题反馈', strings.contact)

    @staticmethod
    def show_modelInfo():
        showInformation.ShowInfomation('预设模型信息', strings.modelInfo)

'''==================================================
Start GUI
=================================================='''
if __name__ == "__main__":
    mainwindow = MainWindow()
    mainwindow.mainloop()
