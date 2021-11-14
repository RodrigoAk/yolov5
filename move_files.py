"""
    Script to move the files you want to your "custom" dataset. The COCO dataset
    contains 80 classes, and this scripts lets you move the images and their
    respective label file that you want to use for training to a different dir.
    For example in our case we wanted to train only using 8 classes, so we moved
    the files that contained at least one of the wanted classes to use for
    training.

    Author: Rodrigo Heira Akamine
    Last modified: November 14, 2021
"""
import os
from tqdm import tqdm
from pycocotools.coco import COCO
import requests
import argparse


def main():
    src_dir = './coco/data/'  # INSERT YOUR SOURCE DIR HERE
    dest_dir = './custom/coco/data/'  # INSERT YOUR TARGET DIR HERE
    # Instantiate COCO specifying the annotations json path
    coco = COCO('./coco/annotations/COCO_ann_file.json')
    # Specify a list of category names of interest
    catIds = coco.getCatIds(catNms=[
        "person",
        "truck",
        "bus",
        "motorcycle",
        "bicycle",
        "car",
        "traffic light",
        "stop sign"
    ])
    # Get the corresponding image ids and images using loadImgs
    # Need to pass each category id individually because if it is passed
    # lets say categories [1,2,3,4,5], it will return only images ids that
    # have all these categories in a single image.
    # Using set() we eliminate the possibility of duplicates
    imgIds = set()
    for catId in catIds:
        imgsIdsList = coco.getImgIds(catIds=catId)
        imgIds.update(imgsIdsList)
    imgIds = list(imgIds)
    images = coco.loadImgs(imgIds)
    print(len(images))

    # Move images to dest_dir
    i = 0
    total = len(images)
    for img in tqdm(images):
        img_src_path = os.path.join(src_dir, img["file_name"])
        img_dest_path = os.path.join(dest_dir, img["file_name"])
        label_src_path = os.path.join(
            src_dir,
            "labels/val2014/",
            img["file_name"].replace("jpg", "txt")
        )
        label_dest_path = os.path.join(
            dest_dir,
            "labels/val2014/",
            img["file_name"].replace("jpg", "txt")
        )
        if(os.path.isfile(img_src_path)):
            os.rename(img_src_path, img_dest_path)
            os.rename(label_src_path, label_dest_path)
            i += 1
    print("Transfered {}/{} files".format(i, total))

    return 0


if __name__ == "__main__":
    main()
