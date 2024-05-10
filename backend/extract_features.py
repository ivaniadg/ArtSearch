import json

from utils.extract_features import extract_features
from utils import get_image_names

if __name__ == '__main__':
    get_image_names("data/high_renaissance")
    index = extract_features("data/high_renaissance")
    with open('temp/high_renaissance.json', 'w') as f:
        json.dump(index, f)