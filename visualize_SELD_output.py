# Script for visualising the SELD output.
#
# NOTE: Make sure to use the appropriate backend for the matplotlib based on your OS
import os
import numpy as np
import librosa.display

import cls_feature_class
import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plot
from matplotlib.pyplot import MultipleLocator

import parameter

plot.switch_backend('agg')
plot.rcParams.update({'font.size': 22})

fig = plot.figure(figsize=(40, 30))

'''分类'''
def collect_classwise_data(_in_dict, use_polar_format=False):
    _out_dict = {}
    for _key in _in_dict.keys():
        for _seld in _in_dict[_key]:
            if _seld[0] not in _out_dict:
                _out_dict[_seld[0]] = []
            if use_polar_format:
                _out_dict[_seld[0]].append([_key, _seld[0], _seld[1], _seld[2]])
            else:
                _out_dict[_seld[0]].append([_key, _seld[0], _seld[1], _seld[2], _seld[3]])
    return _out_dict

'''显示3d图'''
def plot_func3d(plot_data, xlim=[-1, 1], ylim=[-1, 1], zlim=[-1, 1]):
    cmap = ['Magenta', 'Crimson', 'YellowGreen', 'Gold', 'Blue', 'DarkTurquoise', 'LightSalmon', 'Green',
            'Orchid', 'LimeGreen', 'Yellow', 'DodgerBlue', 'Orange', 'DimGray']  # 颜色

    ax = fig.gca(projection='3d')
    for class_ind in plot_data.keys():
        x_ax = np.array(plot_data[class_ind])[:, 2]
        y_ax = np.array(plot_data[class_ind])[:, 3]
        z_ax = np.array(plot_data[class_ind])[:, 4]
        ax.plot(x_ax, y_ax, z_ax, c=cmap[class_ind], label='class{}'.format(class_ind))
        ax.legend() # 右上角图例
        ax.set_xlim3d(xlim), ax.set_ylim3d(ylim), ax.set_zlim3d(zlim)
        ax.set_xlabel('x-axis', labelpad=20), ax.set_ylabel('y-axis', labelpad=20), ax.set_zlabel('z-axis', labelpad=20)

'''显示2d图'''
def plot_func(plot_data, hop_len_s=60, ind=2, plot_x_ax=False, plot_y_ax=False):
    # cmap = ['Crimson', 'Orchid', 'Magenta', 'Blue', 'DodgerBlue', 'DarkTurquoise',
    #         'Green', 'LimeGreen', 'YellowGreen', 'Yellow', 'Gold', 'Orange',
    #         'LightSalmon', 'DimGray']  # 颜色
    cmap = ['Magenta', 'Crimson', 'YellowGreen', 'Gold', 'Blue', 'DarkTurquoise', 'LightSalmon', 'Green',
            'Orchid', 'LimeGreen', 'Yellow', 'DodgerBlue', 'Orange', 'DimGray']

    for class_ind in plot_data.keys():
        time_ax = np.array(plot_data[class_ind])[:, 0] * hop_len_s
        y_ax = np.array(plot_data[class_ind])[:, ind]
        if ind == 1:
            ax = fig.gca()
            ax.add_patch(
                plot.Rectangle(
                    (int(np.array(plot_data[class_ind])[:, 0][0]), (class_ind-1)*4+4),
                    len(time_ax),
                    4, color=cmap[class_ind],
                    label='class{}'.format(class_ind)
                )
            )
            ax.legend()  # 右上角图例
            plot.xlim([0, 600])
        else:
            plot.plot(time_ax, y_ax, marker='.', color=cmap[class_ind],
                      linestyle='None', markersize=4, label='class{}'.format(class_ind))
            plot.legend()
    plot.grid()
    if not plot_x_ax:
        plot.gca().axes.set_xticklabels([])
    if not plot_y_ax:
        plot.gca().axes.set_yticklabels([])

# --------------------------------- MAIN SCRIPT STARTS HERE -----------------------------------------


# params = parameter.Parameters()
# params_dict = params.get_params()

'''显示图像'''
def visidualize_output(params_dict, path, mode, dataset, is_sed=False, use_polar_format=False, do_plot_3d=True):

    # output format file to visualize
    pred = os.path.join(params_dict['dcase_dir'], path)

    # path of reference audio directory for visualizing the spectrogram and description directory for
    # visualizing the reference
    # Note: The code finds out the audio filename from the predicted filename automatically

    ref_dir = os.path.join(params_dict['dataset_dir'], 'metadata_{}'.format(mode))
    aud_dir = os.path.join(params_dict['dataset_dir'], '{}_{}'.format(dataset, mode))

    # load the predicted / reference output format
    feat_cls = cls_feature_class.FeatureClass(params_dict)
    pred_dict = feat_cls.load_output_format_file(pred)
    ref_filename = os.path.basename(pred)
    ref_dict_polar = feat_cls.load_output_format_file(os.path.join(ref_dir, ref_filename))

    if use_polar_format:
        pred_dict_polar = feat_cls.convert_output_format_cartesian_to_polar(pred_dict)
        pred_data = collect_classwise_data(pred_dict_polar, use_polar_format=use_polar_format)
        ref_data = collect_classwise_data(ref_dict_polar, use_polar_format=use_polar_format)
    else:
        ref_dict = feat_cls.convert_output_format_polar_to_cartesian(ref_dict_polar)
        pred_data = collect_classwise_data(pred_dict, use_polar_format=use_polar_format)
        ref_data = collect_classwise_data(ref_dict, use_polar_format=use_polar_format)

    nb_classes = len(feat_cls.get_classes())

    # load the audio and extract spectrogram

    ref_filename = os.path.basename(pred).replace('.csv', '.wav')
    audio, fs = feat_cls._load_audio(os.path.join(aud_dir, ref_filename))
    stft = np.abs(np.squeeze(feat_cls._spectrogram(audio[:, :1])))
    stft = librosa.amplitude_to_db(stft, ref=np.max)

    if is_sed:
        gs = gridspec.GridSpec(3, 3)
        (fig.add_subplot(gs[0, :]), librosa.display.specshow(stft.T, sr=fs, x_axis='s', y_axis='linear'),
         plot.xlim([0, 60]), plot.xticks([]), plot.xlabel(''), plot.title('Spectrogram'))

        (fig.add_subplot(gs[1, :]),
         plot_func(ref_data, params_dict['label_hop_len_s'], ind=1, plot_y_ax=False),
         plot.ylim([-1, (nb_classes + 1) * 4]), plot.title('SED reference'))
        (fig.add_subplot(gs[2, :]),
         plot_func(pred_data, params_dict['label_hop_len_s'], ind=1),
         plot.ylim([-1, (nb_classes + 1) * 4]), plot.title('SED predicted'))
    else:
        if use_polar_format: # 极坐标
            if do_plot_3d:
                gs = gridspec.GridSpec(3, 4)
                (fig.add_subplot(gs[0, 1:3]), librosa.display.specshow(stft.T, sr=fs, x_axis='s', y_axis='linear'),
                 plot.xlim([0, 60]), plot.xticks([]), plot.xlabel(''), plot.title('Spectrogram'))

                (fig.add_subplot(gs[1, :2], projection='polar'),
                 plot_func(ref_data, params_dict['label_hop_len_s'], ind=2, plot_y_ax=True),
                 plot.ylim([-180, 180]), plot.title('Azimuth reference'))
                (fig.add_subplot(gs[1, 2:], projection='polar'),
                 plot_func(pred_data, params_dict['label_hop_len_s'], ind=2),
                 plot.ylim([-180, 180]), plot.title('Azimuth predicted'))

                (fig.add_subplot(gs[2, :2], projection='polar'),
                 plot_func(ref_data, params_dict['label_hop_len_s'], ind=3, plot_y_ax=True),
                 plot.ylim([-90, 90]), plot.title('Elevation reference'))
                (fig.add_subplot(gs[2, 2:], projection='polar'),
                 plot_func(pred_data, params_dict['label_hop_len_s'], ind=3),
                 plot.ylim([-90, 90]), plot.title('Elevation predicted'))
            else:
                gs = gridspec.GridSpec(3, 4)
                (fig.add_subplot(gs[0, 1:3]), librosa.display.specshow(stft.T, sr=fs, x_axis='s', y_axis='linear'),
                 plot.xlim([0, 60]), plot.xticks([]), plot.xlabel(''), plot.title('Spectrogram'))

                (fig.add_subplot(gs[1, :2]),
                 plot_func(ref_data, params_dict['label_hop_len_s'], ind=2, plot_y_ax=True),
                 plot.ylim([-180, 180]), plot.title('Azimuth reference'))
                (fig.add_subplot(gs[1, 2:]),
                 plot_func(pred_data, params_dict['label_hop_len_s'], ind=2),
                 plot.ylim([-180, 180]), plot.title('Azimuth predicted'))
                (fig.add_subplot(gs[2, :2]),
                 plot_func(ref_data, params_dict['label_hop_len_s'], ind=3, plot_y_ax=True),
                 plot.ylim([-90, 90]), plot.title('Elevation reference'))
                (fig.add_subplot(gs[2, 2:]),
                 plot_func(pred_data, params_dict['label_hop_len_s'], ind=3),
                 plot.ylim([-90, 90]), plot.title('Elevation predicted'))
        else:
            if do_plot_3d:
                gs = gridspec.GridSpec(1, 2)
                fig.add_subplot(gs[:, 0], projection='3d'), plot_func3d(ref_data), plot.title('3D DOA reference')
                fig.add_subplot(gs[:, 1], projection='3d'), plot_func3d(pred_data), plot.title('3D DOA predicted')
            else:
                gs = gridspec.GridSpec(4, 6)
                (fig.add_subplot(gs[0, 2:4]), librosa.display.specshow(stft.T, sr=fs, x_axis='s', y_axis='linear'),
                 plot.xlim([0, 60]), plot.xticks([]), plot.xlabel(''), plot.title('Spectrogram'))

                (fig.add_subplot(gs[1, :3]),
                 plot_func(ref_data, params_dict['label_hop_len_s'], ind=2, plot_y_ax=False),
                 plot.ylim([-1, 1]), plot.title('x-axis DOA reference'))
                (fig.add_subplot(gs[1, 3:]),
                 plot_func(pred_data, params_dict['label_hop_len_s'], ind=2),
                 plot.ylim([-1, 1]), plot.title('x-axis DOA predicted'))
                (fig.add_subplot(gs[2, :3]),
                 plot_func(ref_data, params_dict['label_hop_len_s'], ind=3, plot_y_ax=True),
                 plot.ylim([-1, 1]), plot.title('y-axis DOA reference'))
                (fig.add_subplot(gs[2, 3:]),
                 plot_func(pred_data, params_dict['label_hop_len_s'], ind=3),
                 plot.ylim([-1, 1]), plot.title('y-axis DOA predicted'))
                (fig.add_subplot(gs[3, :3]),
                 plot_func(ref_data, params_dict['label_hop_len_s'], ind=4,plot_y_ax=True, plot_x_ax=True),
                 plot.ylim([-1, 1]), plot.title('z-axis DOA reference'))
                (fig.add_subplot(gs[3, 3:]),
                 plot_func(pred_data, params_dict['label_hop_len_s'], ind=4, plot_x_ax=True),
                 plot.ylim([-1, 1]), plot.title('z-axis DOA predicted'))

    if is_sed:
        image_format='sed'
    else:
        if use_polar_format:
            coordinate = 'polar'
        else:
            coordinate = 'cartesian'
        if do_plot_3d:
            dimension = '3d'
        else:
            dimension = '2d'

        image_format = '{}_{}'.format(coordinate, dimension)

    name = '{}_{}'.format(image_format, ref_filename.replace('.wav', '.jpg'))

    path = os.path.join(params_dict['dcase_dir'], name)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    fig.clf()
    return path

if __name__ == '__main__':
    params = parameter.Parameters()
    params.set_model_name('1')
    params_dict = params.get_params()
    dir = '{}_{}_{}'.format(params_dict['model_name'], params_dict['dataset'], params_dict['mode'])
    path = '{}/fold1_room1_mix006_ov1.csv'.format(dir)
    path_=visidualize_output(params_dict=params_dict, path=path, is_sed=False, dataset=params_dict['dataset'],
                       mode=params_dict['mode'], use_polar_format=False, do_plot_3d=True)
    print(path_)