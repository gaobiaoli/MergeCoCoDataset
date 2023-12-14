def getIdMap(trainAnno, labelmap, newJson):
    """获取category的ID映射，并在newJson中添加category标签"""
    categoryIdMap = {}
    newCategory = []
    for category in trainAnno["categories"]:
        if category["name"] in labelmap.keys():
            newJson["categories"].append(category)
            category["name"] = labelmap[category["name"]]

            if category["name"] not in newCategory:
                categoryIdMap[category["id"]] = len(newCategory)
                category["id"] = len(newCategory)
                newCategory.append(category["name"])
            else:
                categoryIdMap[category["id"]] = newCategory.index(category["name"])
                category["id"] = newCategory.index(category["name"])
    return categoryIdMap


def getImageId(trainAnno, categoryIdMap, newJson):
    """
    获取需要的ImageID，并添加进newJson的images中
    imageid应重新根据当前状态设置
    """
    imageId = set()
    oldImageId = newJson["images"][-1]["id"] if newJson["images"] else 0
    oldAnnotationId = newJson["annotations"][-1]["id"] if newJson["annotations"] else 0
    for anno in trainAnno["annotations"]:
        if anno["category_id"] in categoryIdMap.keys():
            newJson["annotations"].append(anno)
            anno["image_id"] += oldImageId
            anno["id"] += oldAnnotationId
            imageId.add(anno["image_id"])
            anno["category_id"] = categoryIdMap[anno["category_id"]]
    for img in trainAnno["images"]:
        if img["id"] + oldImageId in imageId:
            newJson["images"].append(img)
            img["id"] += oldImageId
    return imageId
