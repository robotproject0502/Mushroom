import argparse
import os
import sys
root = os.getcwd()
class Config(object):
    params = {
        "root": root,
        "mode": "default",
        "keyword": "default",
        "epoch": 101,
        "learning_rate": 1.001,
        "batch_size": 9,
        "weight_decay": 1.0001,
        "driver_path": root + r"\chromedriver_win33\chromedriver.exe",
        "image_save_path": root + r"\result",
        "model_load_path": root + r"\8_class_model.tar",
        "model_save_path": root + r'\save_model',
        "image_folder": root + r"\trash",
        "test_image": r"G:\Dropbox\공모전\Shopping Lense_v3\trash\train\유리\glass104.jpg",
        "top4": [],
        "class_num": 6,
        "argumentation": False
    }
