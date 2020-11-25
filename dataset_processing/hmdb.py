from utils import utils
import os
import pandas as pd
import logging
import shutil
logger = logging.getLogger(__name__)


def download_extract(tmp_dir):
    # url = 'http://serre-lab.clps.brown.edu/wp-content/uploads/2013/10/hmdb51_org.rar'
    utils.download_file_from_google_drive("1NzKkad-D3lVBvQlyR_V2-Ge2RMMWgywM",
                                          os.path.join(tmp_dir, "hmdb.zip"))
    utils.extract_zip("hmdb.zip", tmp_dir)



def process_hmdb(filename, root_dir="CIAV-Dataset", tmp_dir="."):
    download_extract(tmp_dir)
    hmdb_dir = os.path.join(tmp_dir, "hmdb")
    utils.move_videos_to_main_dir(hmdb_dir)
    dataset_hmdb = pd.read_csv(filename)
    dataset_hmdb = dataset_hmdb[dataset_hmdb["dataset"] == "HMDB51"]

    for i, row in dataset_hmdb.iterrows():
        from_video = os.path.join(hmdb_dir, row["video_name"])
        utils.create_class_dir(root_dir, row["split"], row["class_name"])
        to_video = os.path.join(root_dir, row["split"], row["class_name"], row["video_name"])
        utils.resize_move(from_video, to_video, shortside=256)
    shutil.rmtree(hmdb_dir)
