import pandas as pd
import os
import shutil
from utils import utils


def download_extract(tmp_dir):
    # url = "https://www.crcv.ucf.edu/data/UCF101/UCF101.rar"
    utils.download_file_from_google_drive("1GLTY3--oRv8wXTAVja3vGUHF-Ojc9kHc",
                                          os.path.join(tmp_dir, "UCF-101.zip"))
    utils.extract_zip("UCF-101.zip", tmp_dir)


def process_ucf101(filename, root_dir, tmp_dir):
    download_extract(tmp_dir)
    ucf_dir = os.path.join(tmp_dir, "UCF-101")
    utils.move_videos_to_main_dir(ucf_dir)

    dataset_ucf = pd.read_csv(filename)
    dataset_ucf = dataset_ucf[dataset_ucf["dataset"] == "UCF-101"]

    for i, row in dataset_ucf.iterrows():
        from_video = os.path.join(ucf_dir, row["video_name"])
        utils.create_class_dir(root_dir, row["split"], row["class_name"])
        to_video = os.path.join(root_dir, row["split"], row["class_name"], row["video_name"])
        utils.resize_move(from_video, to_video, shortside=256)
    shutil.rmtree(ucf_dir)
