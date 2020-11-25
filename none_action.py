import utils
import os
import shutil


def download_extract(tmp_dir):
    utils.download_file_from_google_drive("1Qgu18wY08DmTjBK4d5tTJBExXkXCww3h",
                                          os.path.join(tmp_dir, "none_ciav.zip"))
    utils.extract_zip("none_ciav.zip", tmp_dir)


def process_none_action(root_dir, tmp_dir):
    utils.create_dir(root_dir)
    download_extract(tmp_dir)
    no_action_dir = os.path.join(tmp_dir, "none_ciav")
    for split in os.listdir(no_action_dir):
        shutil.move(os.path.join(no_action_dir, split),
                    os.path.join(root_dir, split))

    shutil.rmtree(no_action_dir)
