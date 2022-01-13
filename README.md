# Feature Extraction for SUTURO Perception robocup YCB object models

## python script download

run the script with the following command:
```
python3 download_ycb_dataset.py
```

It will download all objects available on the [ycb website](http://ycb-benchmarks.s3-website-us-east-1.amazonaws.com/) and save them to `/models/ycb`.


## python script crop images

⚠️ You may need to remove some objects that have no `masks` subfolder from the dataset for the script to work

run the script with the following command:
```
python3 cropYcbImages.py
```

It will crop all Images for all objects found in `/models/ycb`, rename them and save them to `/robocup_dataset` for use in featureExtraction.


## rs_addons featureExtraction
Install [robosherlock](https://github.com/RoboSherlock/robosherlock) including rs_addons/rs_resources with the following instructions: 
> https://github.com/suturo21-22/suturo-installation

1. make a `robocup_dataset.yaml` with all object class names and the following structure:
```
%YAML:1.0
classes: 
  - "001_chips_can"
...
```
2. copy `robocup_dataset.yaml` file to `rs_ws/src/rs_resources/objects_dataset/splits/`


3. run the following command to extract the features
```
rosrun rs_addons featureExtractor -s robocup_dataset.yaml -i ~/suturo/perception_extract_objects/robocup_dataset -f BVLC_REF

# -s: name of the .yaml file in the splits folder
# -i: path to the dataset of cropped images
# -f: feature to extract
```