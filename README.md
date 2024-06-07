# Thesis

## Extracting features
### Build image
``
docker build -t extract_features/lastest -f Dockerfile.feature_extraction .
``
### Run

```
docker run -v /absolutepath_to_images:/app/data/high_renaissance -v /absolute_path_temp_folder:/app/temp extract_features/lastest

```