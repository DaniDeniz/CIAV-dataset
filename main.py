from dataset_processing.youtube_videos import process_yt_videos
from dataset_processing.charades import process_charades
from dataset_processing.hmdb import process_hmdb
from dataset_processing.ucf101 import process_ucf101
from dataset_processing.stair import process_stair
from dataset_processing.none_action import process_none_action
from dataset_processing.falldataset import process_fall_dataset
from utils import utils
import argparse


def main(args):
    ROOT_DIR = args.ROOR_DIR
    TMP_DIR = args.TMP_DIR
    utils.create_dir(ROOT_DIR)
    utils.create_dir(TMP_DIR)
    process_none_action(root_dir=ROOT_DIR, tmp_dir=TMP_DIR)
    process_stair("res/ciav_videos.csv", root_dir=ROOT_DIR, tmp_dir=TMP_DIR)
    process_ucf101("res/ciav_videos.csv", root_dir=ROOT_DIR, tmp_dir=TMP_DIR)
    process_hmdb("res/ciav_videos.csv", root_dir=ROOT_DIR, tmp_dir=TMP_DIR)
    process_yt_videos("res/dataset_yt.csv", root_dir=ROOT_DIR, tmp_dir=TMP_DIR)
    process_fall_dataset("res/fall_dataset.csv", root_dir=ROOT_DIR, tmp_dir=TMP_DIR)
    process_charades(filename="res/charades_videos.csv", root_dir=ROOT_DIR,
                     tmp_dir=TMP_DIR)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and create the CIAV Dataset')
    parser.add_argument('--root_dir', dest='ROOT_DIR', type=str, default="CIAV-dataset/",
                        help='Path to where the CIAV Dataset will be Downloaded. '
                             'An example could be: /home/user/CIAV-dataset')
    parser.add_argument('--tmp_dir', dest='TMP_DIR', type=str,
                        default="tmp/",
                        help='Directory where temporally files and original datasets will be downloaded.')
    args = parser.parse_args()
    main(args)




