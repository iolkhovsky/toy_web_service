import cv2
from glob import glob
import numpy as np
from os.path import isdir, join, basename, splitext, getmtime
from os import makedirs, remove
from pathlib import Path
import yaml


IMGS_SUBFOLDER = "images"
YMLS_FOLDER = "reports"


class SamplesRepository:

    def __init__(self, root, max_size=1):
        self.root = root
        self.max_size = max_size

        for target in [self.root ,
                       join(self.root , IMGS_SUBFOLDER),
                       join(self.root , YMLS_FOLDER)]:
            if not isdir(target):
                makedirs(target)

    def save_sample(self, name, img, report):
        samples = self.get_processed_samples_list()

        while len(samples) >= self.max_size:
            oldest_sample = samples[0]
            remove(join(self.root, IMGS_SUBFOLDER, oldest_sample + ".jpg"))
            remove(join(self.root, YMLS_FOLDER, oldest_sample + ".yml"))
            samples.pop(0)

        name = basename(splitext(name)[0])
        cv2.imwrite(join(self.root, IMGS_SUBFOLDER, name + ".jpg"), img)
        write_yaml(report, join(self.root, YMLS_FOLDER, name + ".yml"))

    def read_sample(self, name):
        return cv2.imread(join(self.root, IMGS_SUBFOLDER, name + ".jpg")), \
               read_yaml(join(self.root, YMLS_FOLDER, name + ".yml"))

    def get_processed_samples_list(self):
        image_files = {splitext(basename(x))[0] for x in glob(join(self.root, IMGS_SUBFOLDER, "*.jpg"))}
        yaml_files = {splitext(basename(x))[0] for x in glob(join(self.root, YMLS_FOLDER, "*.yml"))}
        valid_samples = image_files.intersection(yaml_files)
        for path in image_files:
            if path not in valid_samples:
                remove(join(self.root, IMGS_SUBFOLDER, path + ".jpg"))
        for path in yaml_files:
            if path not in valid_samples:
                remove(join(self.root, YMLS_FOLDER, path + ".yml"))
        samples = [splitext(x.name)[0] for x in
                   sorted(Path(join(self.root, IMGS_SUBFOLDER)).iterdir(), key=getmtime)]
        return samples


def decode_image(content):
    return cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)


def encode_image(image):
    res, encoded = cv2.imencode(".jpg", image)
    return encoded


def write_yaml(data, path):
    with open(path, "w") as f:
        yaml.dump(data, f)


def read_yaml(path):
    try:
        with open(path, "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)
    except Exception as e:
        return {}
