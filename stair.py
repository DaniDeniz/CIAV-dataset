import os
import pandas as pd
import utils
import shutil


def start_with(x: str):
    return x.startswith("a")


def download_stair_x_y(tmp_dir):
    utils.download_file_from_google_drive("1ccnENWbD_I3-HpuKoXWPoASPtcEoW9ti",
                                          os.path.join(tmp_dir, "stair_x_y.zip"))
    utils.extract_zip("stair_x_y.zip", tmp_dir)


def download_class(stair_class, tmp_dir):
    url = "https://data.airc.aist.go.jp/stair-actions-v1.1/train/{}.zip".format(stair_class)
    utils.download_extract(url, "{}.zip".format(stair_class), tmp_dir)


def process_stair(filename, root_dir, tmp_dir):
    utils.create_dir(root_dir)
    dataset_stair = pd.read_csv(filename)
    dataset_stair = dataset_stair[dataset_stair["dataset"] == "STAIR"]
    dataset_stair = dataset_stair[dataset_stair["video_name"].transform(start_with)]
    ciav_to_stair = {"walk": "walking_with_stick",
                     "sit": "sitting_down",
                     "stand up": "standing_up",
                     "Lying on the floor": "lying_on_floor"}

    for ciav_k, stair_v in ciav_to_stair.items():
        download_class(stair_v, tmp_dir)
        stair_concrete_class = dataset_stair[dataset_stair["class_name"] == ciav_k]
        class_dir = os.path.join(tmp_dir, stair_v)
        for i, row in stair_concrete_class.iterrows():
            original_file = os.path.join(tmp_dir, class_dir, row["video_name"])
            dest_file = os.path.join(root_dir, row["split"], row["class_name"], row["video_name"])
            utils.create_class_dir(root_dir, row["split"], row["class_name"])
            utils.resize_move(original_file,
                              dest_file,
                              shortside=256)
        shutil.rmtree(class_dir)

    download_stair_x_y(tmp_dir)
    stair_x_y_dir = os.path.join(tmp_dir, "stair_x_y")
    for split in os.listdir(stair_x_y_dir):
        for action_class in os.listdir(os.path.join(stair_x_y_dir, split)):
            for video in os.listdir(os.path.join(stair_x_y_dir, split, action_class)):
                original_file = os.path.join(stair_x_y_dir, split, action_class, video)
                dest_file = os.path.join(root_dir, split, action_class, video)
                shutil.move(original_file, dest_file)
    shutil.rmtree(stair_x_y_dir)


