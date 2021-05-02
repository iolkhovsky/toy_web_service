import cv2
from glob import glob
import numpy as np
from os.path import isdir, join, basename, splitext, getmtime
from os import makedirs, remove
from pathlib import Path
import yaml


DEFAULT_REPO_ROOT = "repo"
DEFAULT_IMGS_FOLDER = "images"
DEFAULT_YMLS_FOLDER = "reports"
DEFAULT_MAX_SAMPLES_TO_STORE = 3


def decode_image(content):
    return cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)


def encode_image(image):
    res, encoded = cv2.imencode(".jpg", image)
    return encoded


def write_yaml(data, path):
    with open(path, "w") as f:
        yaml.dump(data, f)


def read_yaml(path):
    with open(path, "r") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def init_repo():
    for target in [DEFAULT_REPO_ROOT,
                   join(DEFAULT_REPO_ROOT, DEFAULT_IMGS_FOLDER),
                   join(DEFAULT_REPO_ROOT, DEFAULT_YMLS_FOLDER)]:
        if not isdir(target):
            makedirs(target)


def save_sample(name, img, report):
    samples = get_processed_samples_list()

    while len(samples) >= DEFAULT_MAX_SAMPLES_TO_STORE:
        oldest_sample = samples[0]
        remove(join(DEFAULT_REPO_ROOT, DEFAULT_IMGS_FOLDER, oldest_sample + ".jpg"))
        remove(join(DEFAULT_REPO_ROOT, DEFAULT_YMLS_FOLDER, oldest_sample + ".yml"))
        samples.pop(0)

    name = basename(splitext(name)[0])
    cv2.imwrite(join(DEFAULT_REPO_ROOT, DEFAULT_IMGS_FOLDER, name + ".jpg"), img)
    write_yaml(report, join(DEFAULT_REPO_ROOT, DEFAULT_YMLS_FOLDER, name + ".yml"))


def read_sample(name):
    return cv2.imread(join(DEFAULT_REPO_ROOT, DEFAULT_IMGS_FOLDER, name + ".jpg")), \
           read_yaml(join(DEFAULT_REPO_ROOT, DEFAULT_YMLS_FOLDER, name + ".yml"))


def get_processed_samples_list():
    image_files = {splitext(basename(x))[0] for x in glob(join(DEFAULT_REPO_ROOT, DEFAULT_IMGS_FOLDER, "*.jpg"))}
    yaml_files = {splitext(basename(x))[0] for x in glob(join(DEFAULT_REPO_ROOT, DEFAULT_YMLS_FOLDER, "*.yml"))}
    valid_samples = image_files.intersection(yaml_files)
    for path in image_files:
        if path not in valid_samples:
            remove(join(DEFAULT_REPO_ROOT, DEFAULT_IMGS_FOLDER, path + ".jpg"))
    for path in yaml_files:
        if path not in valid_samples:
            remove(join(DEFAULT_REPO_ROOT, DEFAULT_YMLS_FOLDER, path + ".yml"))
    samples = [splitext(x.name)[0] for x in
               sorted(Path(join(DEFAULT_REPO_ROOT, DEFAULT_IMGS_FOLDER)).iterdir(), key=getmtime)]
    return samples
