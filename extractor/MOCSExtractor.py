import json
import os
import shutil
from tqdm import tqdm
from utils.utils import getIdMap, getImageId

if __name__ == "__main__":
    mapping = {"Worker": "worker"}
    annoJson = ["dataset/mocs/instances_train.json", "dataset/mocs/instances_val.json"]
    newJsonPath = "dataset/worker-Dataset/MOCS-worker.json"
    oldImgPaths = [
        "/CV/gaobiaoli/dataset/mocs/images/train",
        "/CV/gaobiaoli/dataset/mocs/images/val",
    ]
    newImgPath = "./MOCS"
    if not os.path.exists(newImgPath):
        os.mkdir(newImgPath)
    newJson = {"images": [], "categories": [], "annotations": []}
    with open(annoJson[0], "r") as fp:
        trainAnno = json.load(fp)

    # 提取需要的categories，并重置Id(从0开始)
    categoryIdMap = getIdMap(trainAnno=trainAnno, labelmap=mapping, newJson=newJson)

    # 提取需要的annotations，记录imageId
    imageId = getImageId(
        trainAnno=trainAnno, categoryIdMap=categoryIdMap, newJson=newJson
    )

    for i in range(1, len(annoJson)):
        with open(annoJson[i], "r") as fp:
            trainAnno = json.load(fp)
        tempImageId = getImageId(
            trainAnno=trainAnno, categoryIdMap=categoryIdMap, newJson=newJson
        )
        imageId = tempImageId | imageId

    fileList = []
    for path in oldImgPaths:
        fileList.append(os.listdir(path))
    for img in tqdm(newJson["images"]):
        copied = False
        for i in range(len(fileList)):
            if img["file_name"] in fileList[i]:
                shutil.copyfile(
                    os.path.join(oldImgPaths[i], img["file_name"]),
                    os.path.join(newImgPath, img["file_name"]),
                )
                copied = True
                break
        if not copied:
            print("Not Found Image: ", img["file_name"])

    with open(newJsonPath, "w") as fp:
        json_str = json.dumps(newJson, indent=4)
        fp.write(json_str)

    print("提取前：", len(trainAnno["images"]))
    print("提取后：", len(newJson["images"]))
    # print(trainAnno['annotations'][0])
