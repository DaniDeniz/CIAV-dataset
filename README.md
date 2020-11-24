# CIAV-dataset
Combined Indoor Action Video (CIAV) Dataset. This dataset in created by the integration of several action video datasets such as: Kinetics [[1]](#1), Charades [[2]](#2), UCF101 [[3]](#3), HMDB51 [[4]](#4), STAIR [[5]](#5), Fall detection dataset [[6]](#6) and more.

We also included new clips downloading videos from Youtube. For example, retrieving videos of [House Virtual Tours](https://www.youtube.com/c/OpenHouse24/) to represent indoor scenes without people. Furthermore, we also used the Indoor Scene Recognition [[7]](#7) dataset to create videos in order to represent indoor scenes where no people appears.

Refer to original sources to download those mentioned datasets. However, we provide a script to download and create the CIAV dataset that we designed for performing indoor action recognition and lifestyle monitoring.

## Resources
Inside the **res** directory, you wil find several csv documents that include the necessary information to composed CIAV from the previously described dataset.
- **[ciav_videos.csv](res/ciav_videos)**: Include information such as: the name of each clip, the action (class), the split (train, validation or test) and to which dataset does that video belongs to.
- **[dataset_yt.csv](res/dataset_yt)**: This file provide information to download from Youtube and crop videos.(Eg. Kinetics dataset)
- **[charades_videos.csv](res/charades_videos.csv)**: Information necessary to move and crop the original Charades Videos into the CIAV actions.
- **[fall_dataset.csv](res/fall_dataset.csv)**: Temporal video cropping and selection from the Fall detection [[6]](#6) dataset to include in it in CIAV.

Note that every clip is spatially cropped to have a 256 pixels as its shortside. In addition, we set the frame-rate of every video to 25 FPS.

## Download guide
To download and create the described CIAV dataset you need to clone this repository into your system and run the **main.py** file.

`git clone https://github.com/DaniDeniz/CIAV-dataset.git`

`cd CIAV-dataset`

`pip install -U wget requests`

Start downloading the dataset running:
`python main.py --root_dir "/hdd/CIAV-dataset/" --tmp_dir "/hdd/tmp/"`

Run `python main.py --help` to decide which arguments use. If you have already pre-downloaded the original datasets (Eg. Kinetics, Charades, ...), you can compose the CIAV dataset following the csv files in the **[res](res/)** directory.

Finally, take into account that some videos maybe are not online anymore. In case you need videos that are not available, contact us at [danideniz@ugr.es](danideniz@ugr.es)

# References
<a id="1">[1]</a> Will Kay, Joao Carreira, Karen Simonyan, Brian Zhang, Chloe Hillier, Sudheendra Vijayanarasimhan, Fabio Viola, Tim Green, Trevor Back, Paul Natsev, et al. The kinetics human action video dataset. arXiv:1705.06950, 2017.

<a id="2">[2]</a> Gunnar A Sigurdsson, Gül Varol, Xiaolong Wang, Ali Farhadi, Ivan Laptev, and Abhinav Gupta. Hollywood in homes: Crowdsourcing data collection for activity understanding. In European Conference on Computer Vision, ages 510–526. Springer, 2016.

<a id="3">[3]</a> Khurram Soomro, Amir Roshan Zamir, and Mubarak Shah. Ucf101: A dataset of 101 human actions classes from videos in the wild. arXiv:1212.0402, 2012.

<a id="4">[4]</a> Hildegard Kuehne, Hueihan Jhuang, Estíbaliz Garrote, Tomaso Poggio, and Thomas Serre. Hmdb: a large video database for human motion recognition. In 2011 Int. Conference on Computer Vision, pages 2556–2563. IEEE,
2011.

<a id="5">[5]</a> Yuya Yoshikawa, Jiaqing Lin, and Akikazu Takeuchi. Stair actions: A video dataset of everyday home actions. arXiv:1804.04326, 2018.

<a id="6">[6]</a> Imen Charfi, Johel Miteran, Julien Dubois, Mohamed Atri, and Rached Tourki. Optimized spatio-temporal descriptors for real-time fall detection: comparison of support vector machine and adaboost-based classification. Journal of Electronic Imaging, 22(4):041106, 2013.

<a id="7">[7]</a> Quattoni, A., & Torralba, A. (2009, June). Recognizing indoor scenes. In 2009 IEEE Conference on Computer Vision and Pattern Recognition (pp. 413-420). IEEE.
