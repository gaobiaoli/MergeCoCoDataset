import json
import os
import shutil
from tqdm import tqdm
from utils.utils import getIdMap,getImageId

if __name__ == "__main__":
    mapping = {"people-no-helmet": "worker", "people-helmet": "worker"}
    annoJson = "dataset/CIS-Dataset/dataset/annotations/All-50000.json"
    newJsonPath = "dataset/worker-Dataset/CIS-worker.json"
    oldImgPaths = [
        "dataset/CIS-Dataset/val",
        "dataset/CIS-Dataset/train",
        "dataset/CIS-Dataset/test",
    ]
    newImgPath = "./CIS"

    if not os.path.exists(newImgPath):
        os.mkdir(newImgPath)

    newJson = {"images": [], "categories": [], "annotations": []}
    with open(annoJson, "r") as fp:
        trainAnno = json.load(fp)
    # 提取需要的categories，并重置Id(从0开始)
    categoryIdMap = getIdMap(trainAnno=trainAnno, labelmap=mapping, newJson=newJson)

    # 提取需要的annotations，记录imageId
    imageId = getImageId(
        trainAnno=trainAnno, categoryIdMap=categoryIdMap, newJson=newJson
    )

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
