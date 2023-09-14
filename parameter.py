# Parameters used in the feature extraction, neural network model, and training the SELDnet can be changed here.
#
# Ideally, do not change the values of the default parameters. Create separate cases with unique <task-id> as seen in
# the code below (if-else loop) and use them. This way you can easily reproduce a configuration on a later time.
import os


class Parameters:
    def __init__(self):
        super(Parameters, self).__init__()
        self.params = dict(
            quick_test=False,  # To do quick test. Trains/test on small subset of dataset, and # of epochs

            # INPUT PATH
            dataset_dir='/Datasets/',  # Base folder containing the foa/mic and metadata folders

            # OUTPUT PATH
            feat_label_dir='/Datasets/feat_label/',  # Directory to dump extracted features and labels
            model_dir='models/',  # Dumps the trained models and training curves in this folder
            dcase_output=True,  # If true, dumps the results recording-wise in 'dcase_dir' path.
            # Set this true after you have finalized your model, save the output, and submit
            dcase_dir='results/',  # Dumps the recording-wise network output in this folder

            # DATASET LOADING PARAMETERS
            mode='dev',  # 'dev' - development or 'eval' - evaluation dataset
            dataset='foa',  # 'foa' - ambisonic or 'mic' - microphone signals

            # FEATURE PARAMS
            fs=24000,
            hop_len_s=0.02,
            label_hop_len_s=0.1,
            max_audio_len_s=60,
            nb_mel_bins=64,

            # DNN MODEL PARAMETERS
            label_sequence_length=60,  # Feature sequence length
            batch_size=32,  # Batch size
            dropout_rate=0,  # Dropout rate, constant for all layers
            nb_cnn2d_filt=64,  # Number of CNN nodes, constant for each layer
            f_pool_size=[4, 4, 2],
            # CNN frequency pooling, length of list = number of CNN layers, list value = pooling per layer

            rnn_size=[128, 128],  # RNN contents, length of list = number of layers, list value = number of nodes
            fnn_size=[128],  # FNN contents, length of list = number of layers, list value = number of nodes
            loss_weights=[1., 1000.],  # [sed, doa] weight for scaling the DNN outputs
            nb_epochs=50,  # Train for maximum epochs
            epochs_per_fit=5,  # Number of epochs per fit
            doa_objective='masked_mse',
            # supports: mse, masked_mse. mse- original seld approach; masked_mse - dcase 2020 approach

            # METRIC PARAMETERS
            lad_doa_thresh=20,

            # 新加
            do_baseline=True,
            model_name='default_name',
            am='scSE',
            ratio=4,
            res='main',  # 'main' - 主干   'shortcut' - 分支     'post' - Conv-ResidualPOST
            process_str='dev,eval'  # 'dev' or 'eval' will extract features for the respective set accordingly

        )
        feature_label_resolution = int(self.params['label_hop_len_s'] // self.params['hop_len_s'])
        self.params['feature_sequence_length'] = self.params['label_sequence_length'] * feature_label_resolution
        self.params['t_pool_size'] = [feature_label_resolution, 1, 1]  # CNN time pooling
        self.params['patience'] = int(self.params['nb_epochs'])  # Stop training if patience is reached

        self.params['unique_classes'] = {
            'alarm': 0,
            'baby': 1,
            'crash': 2,
            'dog': 3,
            'engine': 4,
            'female_scream': 5,
            'female_speech': 6,
            'fire': 7,
            'footsteps': 8,
            'knock': 9,
            'male_scream': 10,
            'male_speech': 11,
            'phone': 12,
            'piano': 13
        }

    def set_dataset_dir(self, model_dataset_dir):
        self.params['dataset_dir'] = model_dataset_dir

    def get_dataset_dir(self):
        return self.params['dataset_dir']

    def set_feat_label_dir(self, model_feat_label_dir):
        self.params['feat_label_dir'] = model_feat_label_dir

    def set_model_dir(self, model_model_dir):
        self.params['model_dir'] = model_model_dir

    def get_model_dir(self):
        return  self.params['model_dir']

    def set_dcase_dir(self, model_dcase_dir):
        self.params['dcase_dir'] = model_dcase_dir

    def get_dcase_dir(self):
        return self.params['dcase_dir']

    def set_mode(self, model_mode):
        self.params['mode'] = model_mode

    def set_dataset(self, model_format):
        self.params['dataset'] = model_format

    def set_dcase_output(self, model_dcase_output):
        self.params['dcase_output'] = model_dcase_output

    def set_quick_test(self, model_quick_test):
        self.params['quick_test'] = model_quick_test

    def set_model_name(self, model_model_name):
        self.params['model_name'] = model_model_name

    def set_dir(self, model_dataset_dir, model_feat_label_dir,
                model_model_dir, model_dcase_dir,
                model_mode, model_format, model_dcase_output,
                model_quick_test, model_model_name):
        self.set_dataset_dir(model_dataset_dir)
        self.set_feat_label_dir(model_feat_label_dir)
        self.set_model_dir(model_model_dir)
        self.set_dcase_dir(model_dcase_dir)
        self.set_mode(model_mode)
        self.set_dataset(model_format)
        self.set_dcase_output(model_dcase_output)
        self.set_quick_test(model_quick_test)
        self.set_model_name(model_model_name)

    def set_batch_size(self, model_batch_size):
        self.params['batch_size'] = model_batch_size

    def set_do_baseline(self, model_do_baseline):
        self.params['do_baseline'] = model_do_baseline

    def set_am(self, model_am):
        self.params['am'] = model_am

    def set_ratio(self, model_ratio):
        self.params['ratio'] = model_ratio

    def set_res(self, model_res):
        self.params['res'] = model_res

    def set_model(self, model_batch_size, model_do_baseline, model_am, model_ratio, model_res):
        self.set_batch_size(model_batch_size)
        self.set_do_baseline(model_do_baseline)
        self.set_am(model_am)
        self.set_ratio(model_ratio)
        self.set_res(model_res)

    def set_extraction(self, model_feature_extraction='dev,eval'):
        self.params['process_str'] = model_feature_extraction

    def get_params(self):
        return self.params
