import json
import subprocess
import os
import logging
import wget
import zipfile
import requests
import shutil
import sys

logger = logging.getLogger(__name__)


def create_dir(root_dir):
    os.makedirs(root_dir, exist_ok=True)


def create_class_dir(root_dir, split, class_name):
    os.makedirs(os.path.join(root_dir, split), exist_ok=True)
    os.makedirs(os.path.join(root_dir, split, class_name), exist_ok=True)


def extract_zip(filename, tmp_dir):
    logger.info("Start extracting {} Dataset (zip)".format(filename))
    with zipfile.ZipFile(os.path.join(tmp_dir, filename), "r") as zip_ref:
        zip_ref.extractall(tmp_dir)
    os.remove(os.path.join(tmp_dir, filename))
    logger.info("Finished extracting {} Dataset (zip)".format(filename))


def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def download_extract(url, filename, tmp_dir):
    logger.info("Start downloading {} dataset".format(filename))
    wget.download(url, tmp_dir, bar=bar_progress)
    logger.info("Finished downloading {} Dataset".format(filename))
    extract_zip(filename, tmp_dir)

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def move_videos_to_main_dir(dataset_dir):
    for classes_ in os.listdir(dataset_dir):
        for video in os.listdir(os.path.join(dataset_dir, classes_)):
            shutil.move(os.path.join(dataset_dir, classes_, video),
                        os.path.join(dataset_dir, video))
        os.rmdir(os.path.join(dataset_dir, classes_))


def resize_move(tmp_video, resized_video, start=None, end=None, shortside=256):
    wid, hei = probe_res(tmp_video)
    fps = "25"
    if (wid != shortside) and (hei != shortside):
        if wid >= hei:
            hei_new = shortside
            wid_new = int(1. * wid / hei * shortside)
            wid_new = int(wid_new/2)*2
        else:
            wid_new = shortside
            hei_new = int(1. * hei / wid * shortside)
            hei_new = int(hei_new/2)*2
    else:
        wid_new = wid
        hei_new = hei

    command = ["ffmpeg",
               "-y",
               "-loglevel",  "quiet",
               "-i", tmp_video,
               "-r", fps,
               "-vf", "scale={}x{}".format(wid_new, hei_new),
               "-c:a", "copy",
               resized_video]

    if start is not None and end is not None:
        time_restriction = ["-ss", str(start),
                            "-to", str(end)]
        command[6:4] = time_restriction

    subprocess.call(command)


def probe_res(video):
    # probe the resolution of video
    command = ["ffprobe",
               "-loglevel",  "quiet",
               "-select_streams", "v:0",
               "-show_entries", "stream=height,width",
               "-print_format", "json",
               "-show_format",
               video]
    pipe = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    out, err = pipe.communicate()
    vmeta = json.loads(out)
    wid = int(vmeta['streams'][0]['width'])
    hei = int(vmeta['streams'][0]['height'])
    return wid, hei


def download_to_tmp(vid, tmp_video):
    url = 'https://www.youtube.com/watch?v={}'.format(vid)
    cmd = ['youtube-dl','-f', 'mp4', '-o', tmp_video, url]
    subprocess.call(cmd)
