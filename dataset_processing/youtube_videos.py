import pandas as pd
import os
from utils import utils
import logging
from functools import partial
import multiprocessing
import numpy as np

logger = logging.getLogger(__name__)


def process_df(root_dir, tmp_dir, dataset):
    for i, row in dataset.iterrows():
        destination_file = os.path.join(root_dir, row["split"],
                                        row["class_name"],
                                        row["video_name"])
        temporal_file = os.path.join(tmp_dir, "tmp_{}.mp4".format(row["youtube_id"]))
        if not os.path.isfile(destination_file):
            utils.download_to_tmp(row['youtube_id'], temporal_file)
            utils.create_class_dir(root_dir, row["split"], row["class_name"])
            if os.path.isfile(temporal_file):
                try:
                    utils.resize_move(temporal_file, destination_file,
                                      row["start_time"], row["end_time"],
                                      shortside=256)
                    logger.info("Video {} from {} downloaded".format(row["youtube_id"], row["dataset"]))
                except KeyError:
                    logger.info("Video {} from {} NOT downloaded".format(row["youtube_id"], row["dataset"]))
                    with open(root_dir + "notDownloaded_yt.txt", "a+") as f:
                        f.write(row["video_name"] + ", " + row["class_name"] + ", " + row['youtube_id'] + '\n')
                os.remove(temporal_file)
            else:
                logger.info("Video {} from {} NOT downloaded".format(row["youtube_id"], row["dataset"]))
                with open(root_dir + "notDownloaded_yt.txt", "a+") as f:
                    f.write(row["video_name"] + ", " + row["class_name"] + ", " + row['youtube_id'] + '\n')


def process_yt_videos(filename, root_dir="CIAV-Dataset", tmp_dir=""):
    utils.create_dir(root_dir)
    dataset = pd.read_csv(filename)
    partial_df_processing = partial(process_df, root_dir, tmp_dir)
    num_cores = multiprocessing.cpu_count() - 1  # leave one free to not freeze machine
    num_partitions = num_cores  # number of partitions to split dataframe
    df_split = np.array_split(dataset, num_partitions)
    pool = multiprocessing.Pool(num_cores)
    pool.map(partial_df_processing, df_split)
    pool.close()
    pool.join()







