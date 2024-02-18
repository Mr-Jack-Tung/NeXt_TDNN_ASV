
BATCHSIZE= 128
BASE_LR = 1e-6
LR = BASE_LR * BATCHSIZE

NUMWORKER = 20

CHANNEL_SIZE = 256 # ⚡⚡⚡
EMBEDING_SIZE = 192

NUM_EVAL = 2
EVAL_FRAMES = 300
MAX_FRAMES = 300 # ✨ 2s -> 3s
SAMPLING_RATE = 16000

# ?? 1. Set 'Dataset', 'DataLoader' 
TRAIN_DATASET = 'train_dataset_classification'
TRAIN_DATASET_CONFIG={
  'train_list': './data/train_list.txt',
  'train_path' : '/home/hhj/speaker_verification/voxceleb2',
  'max_frames': MAX_FRAMES,
  'augment': True,
  'musan_path': '/home/hhj/speaker_verification/musan_split',
  'rir_path': '/home/hhj/speaker_verification/RIRS_NOISES/simulated_rirs',  
}

TEST_LIST = './data/veri_test2.txt'
TEST_LIST_E = './data/list_test_all2.txt'
TEST_LIST_H = './data/list_test_hard2.txt'
TEST_DATASET = 'test_dataset'
TEST_DATASET_CONFIG={
  'test_list': TEST_LIST,
  'test_path': '/home/hhj/speaker_verification/voxceleb1',
}

# ?? 2. Set 'feature_extractor', 'spec_aug', 'Model', 'Loss', 'Optimizer', 'Scheduler'
FEATURE_EXTRACTOR = 'mel_transform'
FEATURE_EXTRACTOR_CONFIG = {
    'sample_rate': 16000,
    'n_fft': 512,
    'win_length': 400,
    'hop_length': 160,
    'n_mels': 80,
    'coef': 0.97,
}

SPEC_AUG = 'spec_aug'
SPEC_AUG_CONFIG = {
    'freq_mask_param': 8,
    'time_mask_param': 10,
}

MODEL = 'NeXt_TDNN'
MODEL_CONFIG = {
    'depths':[3, 3, 3], 
    'dims':[CHANNEL_SIZE, CHANNEL_SIZE, CHANNEL_SIZE],
    'kernel_size': [7, 65], # ⚡⚡⚡⚡⚡
    'block': 'TSConvNeXt',
}

AGGREGATION = 'vap_bn_tanh_fc_bn'
AGGREGATION_CONFIG = {
    'channel_size': int(3*CHANNEL_SIZE),
    'intermediate_size': int(3*CHANNEL_SIZE/8),
    'embeding_size': EMBEDING_SIZE,
}


LOSS = 'aamsoftmax'
LOSS_CONFIG = {
    'embeding_size' : EMBEDING_SIZE,
    'num_classes' : 5994,
    'margin': 0.3,
    'scale': 40,    
}

OPTIMIZER = 'adamw'
OPTIMIZER_CONFIG = {
  'lr': LR,
  'weight_decay': 0.01,
}

MAX_EPOCHS = 200
SCHEDULER = 'cyclical_lr'
SCHEDULER_CONFIG = {
    'base_lr' : 1e-8,
    'max_lr': 1e-3, 
    'step_size_up': 130000/2, 
    'mode': 'triangular2', 
    'cycle_momentum': False
}

# ??  3. Set 'engine' for training/validation and 'Trainer' 
ENGINE_CONFIG = {
    'eval_config': {'method': 'num_seg',
                    'test_list': TEST_LIST,
                    'num_eval': NUM_EVAL,
                    'eval_frames': EVAL_FRAMES,
                    'c_miss': 1,
                    'p_target': 0.05,
                    'c_fa': 1,
                    }
}

# ?? 4. Init ModelCheckpoint callback, monitoring "eer"    
CHECKPOINT_CONFIG = {
    'save_top_k': 10, # if save_top_k == -1, all models are saved. https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.callbacks.ModelCheckpoint.html#pytorch_lightning.callbacks.ModelCheckpoint
    'monitor': 'min_eer',
    'mode': 'min',
    'filename': 's-{epoch}-{loss:.2f}-{min_eer:.2f}',
}


# ?? 5. LightningModule
TRAINER_CONFIG = {
    'default_root_dir': './experiments/NeXt_TDNN_C256_B3_K65_7_cyclical_lr_step',
    'val_check_interval': 1.0,
    'max_epochs': MAX_EPOCHS,
    'accelerator': 'gpu',
    'devices': 1,
    'num_sanity_val_steps': -1,
    'gradient_clip_val': 5.0, # 1.0 -> 5.0
}

# ?? 6. Resume training
RESUME_CHECKPOINT = None
PRETRAINED_CHECKPOINT = None
RESTORE_LOSS_FUNCTION = True

# ======================== Test & onnx ======================== #

# 😀😀 for test 
# TEST_CHECKPOINT = './exp_paper/T1_08_TS_ConvNeXt_TDNN_S2_C256_B3_K65_7_cyclical_lr_ecapa/lightning_logs/version_0/checkpoints/s-epoch=115-loss=1.42-full_minimum=0.83-min_eer_seg=1.08.ckpt'
# TEST_CHECKPOINT = './experiments/NeXt_TDNN_C256_B3_K65_7_cyclical_lr_step/lightning_logs/version_0/checkpoints/s-epoch=115-loss=1.42-full_minimum=0.83-min_eer_seg=1.08.ckpt'
TEST_CHECKPOINT = './experiments/NeXt_TDNN_C256_B3_K65_7_cyclical_lr_step/model.pt'

TEST_RESULT_PATH = f"{TRAINER_CONFIG.get('default_root_dir')}_test"

# ⌛⌛ for onnx inference
ONNX_PATH = f"{TEST_RESULT_PATH}/onnx/model.onnx"

# ======================== for score normalization ======================== #
# 😀😀 for score normalization
TOP_K = 300 # 100, 200, 300, 400, 500
COHORT_LIST_PATH = './data/cohort_vox2_6000_EfficientTDNN.csv' # './data/cohort_fixed_speaker_5994_0.csv'
TEST_DATASET_LIST = ['VoxCeleb1_O', 'VoxCeleb1_E', 'VoxCeleb1_H'] # ['VoxCeleb1_O']

COHORT_SAVE_PATH = '/home/hhj/embedding' # extracted embedding of cohort will be saved in this path