import json

from utils.extract_features import extract_features

if __name__ == '__main__':
    index = extract_features("data/high_renaissance")
    with open('temp/high_renaissance.json', 'w') as f:
        json.dump(index, f)
