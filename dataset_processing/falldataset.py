from utils import utils
import os
import pandas as pd
import logging
import shutil
logger = logging.getLogger(__name__)


def download_extract(tmp_dir):
    utils.download_file_from_google_drive("1vHl5oIwno45MOJRtem8LYFlUAAbi0SST",
                                          os.path.join(tmp_dir, "Fall_dataset_256.zip"))
    utils.extract_zip("Fall_dataset_256.zip", tmp_dir)


def process_fall_dataset(filename, root_dir="CIAV-Dataset", tmp_dir="."):
    download_extract(tmp_dir)
    fall_dir = os.path.join(tmp_dir, "Fall_dataset_256")
    dataset_fall = pd.read_csv(filename)
    dataset_fall = dataset_fall[dataset_fall["dataset"] == "Fall dataset"]

    for i, row in dataset_fall.iterrows():
        from_video = os.path.join(fall_dir, row["video_name"])
        utils.create_class_dir(root_dir, row["split"], row["class_name"])
        to_video = os.path.join(root_dir, row["split"], row["class_name"], row["video_name"])
        utils.resize_move(from_video, to_video, row["start_time"], row["end_time"], shortside=256)
    shutil.rmtree(fall_dir)
