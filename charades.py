import os
import pandas as pd
import logging
import utils
import shutil
logger = logging.getLogger(__name__)


def download_extract(tmp_dir):
    charades_url = "http://ai2-website.s3.amazonaws.com/data/Charades_v1_480.zip"
    utils.download_extract(charades_url, "Charades_v1_480.zip", tmp_dir)


def process_charades(filename, root_dir="CIAV-dataset", tmp_dir="/tmp"):
    download_extract(tmp_dir)
    charades_dir = os.path.join(tmp_dir, "Charades_v1_480")
    dataset_charades = pd.read_csv(filename)
    utils.create_dir(root_dir)

    for i, row in dataset_charades.iterrows():
        utils.create_class_dir(root_dir, row["split"], row["class_name"])
        video_name = row["video_name"]
        video_name = "{}.mp4".format(video_name.split("_")[0])
        utils.resize_move(os.path.join(charades_dir, video_name),
                          os.path.join(root_dir, row["split"], row["class_name"], row["video_name"]),
                          row["start_time"], row["end_time"],
                          shortside=256)
    shutil.rmtree(charades_dir)

