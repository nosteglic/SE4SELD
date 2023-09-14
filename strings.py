software_introduction = '''
语言：python 3.6.9\n
IDE：Pycharm\n
模型框架：keras\n
GUI界面开发工具：tkinter\n
硬件支持：GPU NVIDIA GeForce RTX 2060 with Max-Q Design
'''
references = '''
[1]	MESAROS A, ADAVANNE S, POLITIS A, 等. Joint Measurement of Localization and Detection of Sound Events[C]//2019 IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA). 2019: 333–337.\n
[2]	赵路. 复杂背景下的声源定位和识别[D]. 电子科技大学, 2020.\n
[3]	ADAVANNE S, POLITIS A, VIRTANEN T. A multi-room reverberant dataset for sound event localization and detection[J]. arXiv:1905.08546 [cs, eess], 2019.\n
[4]	POLITIS A, ADAVANNE S, VIRTANEN T. A Dataset of Reverberant Spatial Sound Scenes with Moving Sources for Sound Event Localization and Detection[J]. arXiv:2006.01919 [cs, eess], 2020.\n
[5]	HIRVONEN  toni. classification of spatial audio location and content using convolutional neural networks[J]. journal of the audio engineering society, 2015.\n
[6]	ADAVANNE S, POLITIS A, NIKUNEN J, 等. Sound Event Localization and Detection of Overlapping Sources Using Convolutional Recurrent Neural Networks[J]. IEEE Journal of Selected Topics in Signal Processing, 2019, 13(1): 34–48.\n
[7]	CAO Y, KONG Q, IQBAL T, 等. Polyphonic Sound Event Detection and Localization using a Two-Stage Strategy[J]. Proceedings of the Detection and Classification of Acoustic Scenes and Events 2019 Workshop (DCASE2019), 2019: 30–34.\n
[8]	NARANJO-ALCAZAR J, PEREZ-CASTANOS S, FERRANDIS J, 等. Sound Event Localization and Detection using Squeeze-Excitation Residual CNNs[J]. arXiv:2006.14436 [cs, eess], 2020.\n
[9]	HU J, SHEN L, SUN G. Squeeze-and-Excitation Networks[C]//2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2018: 7132–7141.\n
[10] ROY A G, NAVAB N, WACHINGER C. Concurrent Spatial and Channel ‘Squeeze & Excitation’ in Fully Convolutional Networks[C]//FRANGI A F, SCHNABEL J A, DAVATZIKOS C, 等. Medical Image Computing and Computer Assisted Intervention – MICCAI 2018. Cham: Springer International Publishing, 2018: 421–429\n
[11] NARANJO-ALCAZAR J, PEREZ-CASTANOS S, ZUCCARELLO P, 等. Acoustic Scene Classification With Squeeze-Excitation Residual Networks[J]. IEEE Access, 2020, 8: 112287–112296.\n
[12] NARANJO-ALCAZAR J, PEREZ-CASTANOS S, FERRANDIS J, 等. Sound Event Localization and Detection using Squeeze-Excitation Residual CNNs[J]. arXiv:2006.14436 [cs, eess], 2020.\n
[13] MESAROS A, HEITTOLA T, VIRTANEN T. Metrics for Polyphonic Sound Event Detection[J]. Applied Sciences, Multidisciplinary Digital Publishing Institute, 2016, 6(6): 162.\n
[14] HE K, ZHANG X, REN S, 等. Deep Residual Learning for Image Recognition[J]. arXiv:1512.03385 [cs], 2015.\n
'''
my_infomation = '作者：沈雅馨\n' \
                '学校：江苏大学\n' \
                '学院：计算机科学与通信工程学院\n' \
                '专业：计算机科学与技术\n' \
                '班级：计算机1701\n' \
                '学号：3170602003\n' \
                '毕业设计题目：基于双域注意力机制的声音事件定位与检测系统设计与实现\n' \
                '指导老师：毛启容老师\n' \
                '特别感谢：高利剑师兄\n' \
                '手机：18852890233\n' \
                '邮箱：nosteglic@163.com'
# contact = '手机：18852890233\n' \
#           '邮箱：nosteglic@163.com\n'

resultTableIntroduction = '''这个模块用于显示系统在数据集的两种格式foa和mic下使用2019独立指标和2020联合指标的表现，数据以csv格式保存和加载。现对毕设训练完成的数据进行解释：
（1）csv/analysis_1.csv：探究在baseline的CNN层分别直接加入cSE、sSE和scSE后对整体结果的影响
（2）csv/analysis_2.csv：探究使用残差结构（Conv-Residual）和在残差结构中加入scSE（Conv-StandardPOST）后对整体结果的影响
（3）csv/analysis_3.csv：探究将scSE分别加在Conv-Residual的主干（master）和分支（shortcut）上对残差模型结果的影响
（4）csv/analysis_4.csv：探究不同的降维比例ratio对整体结果的影响（基准模型：scSE加在master上）
'''

modelInfo='''-------预设模型名称及对应的模型结构------

0_baseline	     baseline
10_baseline	    baseline + scSE
20_baseline	    baseline + cSE
30_baseline	    baseline + sSE
1_4		residual + scSE	standardPOST
2_4		residual + cSE	standardPOST
3_4		residual + sSE	standardPOST
4_0		residual
5_4		residual + scSE4	主干
6_4		residual + scSE4	分支
'''