import json
import os
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from sklearn.model_selection import train_test_split

def split_coco_dataset(coco_json_path, output_dir, train_ratio, val_ratio, test_ratio):
    # Load the COCO annotations
    coco = COCO(coco_json_path)

    # Get image ids
    image_ids = list(coco.imgs.keys())

    # Split the dataset into train, val, and test sets
    train_ids, test_val_ids = train_test_split(image_ids, test_size=(val_ratio + test_ratio), random_state=42)
    val_ids, test_ids = train_test_split(test_val_ids, test_size=(test_ratio / (val_ratio + test_ratio)), random_state=42)

    # Create output directories
    os.makedirs(output_dir, exist_ok=True)

    # Save the annotations for each split
    for split, ids in zip(['train', 'val', 'test'], [train_ids, val_ids, test_ids]):
        output_json = f'{split}_annotations.json'
        split_json = {
        'images': [],
        'annotations': [],
        'categories': []
        }
        for new_id,image_id in enumerate(ids):
            img_info = coco.loadImgs(image_id)[0]
            annotations = coco.loadAnns(coco.getAnnIds(imgIds=image_id))

            # Save the annotations
            for annotation in annotations:
                new_annotation = annotation.copy()
                new_annotation['image_id'] = new_id  # Reset image_id
                split_json['categories'].append(new_annotation)
            # Save the image
            split_json['images'].append(img_info)
        
        with open(os.path.join(output_dir, output_json), 'w') as outfile:
            json.dump(split_json, outfile,indent=4)
        print(os.path.join(output_dir, output_json))
if __name__ == '__main__':
    coco_json_path = '/CV/gaobiaoli/dataset/worker-Dataset/merged_coco.json'
    output_dir = '/CV/gaobiaoli/project/mmdetection/data/worker/annotations'
    train_ratio = 0.8
    val_ratio = 0.1
    test_ratio = 0.1

    split_coco_dataset(coco_json_path, output_dir, train_ratio, val_ratio, test_ratio)


