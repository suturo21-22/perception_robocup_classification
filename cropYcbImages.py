import os
import cv2
import glob

# path to folder where all the downloaded ycb object_data models are
pathToYcbModelsFolder = os.path.join("models", "ycb")

# path to folder where the cropped images get saved to
pathToGoalFolder = os.path.join("robocup_dataset")


def calculateCropCoordinatesUsingMask(imageMask) -> []:
    # invert mask
    imageMask = cv2.bitwise_not(imageMask)

    # calculate contour
    imgray = cv2.cvtColor(imageMask, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(imageMask, contours, -1, (0,255,0), 3)

    try:
        hierarchy = hierarchy[0]
    except:
        hierarchy = []

    height, width = imageMask.shape[:2]
    min_x, min_y = width, height
    max_x = max_y = 0

    # computes the bounding box for the contour, and draws it on the frame
    for contour, hier in zip(contours, hierarchy):
        (x, y, w, h) = cv2.boundingRect(contour)
        min_x, max_x = min(x, min_x), max(x + w, max_x)
        min_y, max_y = min(y, min_y), max(y + h, max_y)
        #if w > 80 and h > 80:
        #    cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # if max_x - min_x > 0 and max_y - min_y > 0:
    #     cv2.rectangle(imageMask, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

    return [min_y - 10, max_y + 10, min_x -10, max_x + 10]


def cropImage(image, coordinates):
    imageCropped = image[coordinates[0]:coordinates[1], coordinates[2]:coordinates[3]]
    return imageCropped


def saveImageToFolder(image, path, fileName):
    os.makedirs(path, exist_ok=True)
    cv2.imwrite(os.path.join(path, fileName), image)


def main():
    print(f"Cropping all images in base folder {pathToYcbModelsFolder}:\n========================================================\n")

    for filePath in sorted(glob.iglob(f'{pathToYcbModelsFolder}/**', recursive=True)):
        if os.path.isfile(filePath) and filePath.endswith(
                ".jpg") and not "masks" in filePath and not "poses" in filePath:

            # extract metadata
            fileName = os.path.basename(filePath)
            pathToFile = os.path.split(filePath)[0]
            subfolder = pathToFile.split("/")[-1]
            position = fileName[:3]
            fileNumber = fileName.split("_")[1].split(".")[0]
            # rename file according to the specifications in featureExtractor.cpp
            newFileName = f"{fileName[:-4]}_crop.png"

            print(f"cropping and saving {subfolder} {fileName}")

            image = cv2.imread(rf"{filePath}")
            imageMask = cv2.imread(f"{pathToFile}/masks/{position}_{fileNumber}_mask.pbm")

            cropCoordinates = calculateCropCoordinatesUsingMask(imageMask)

            imageCropped = cropImage(image, cropCoordinates)
            saveImageToFolder(imageCropped, os.path.join(pathToGoalFolder, subfolder), newFileName)

    print(f"\n========================================================\nCropped all images and saved them to {pathToGoalFolder}")


if __name__ == '__main__':
    main()