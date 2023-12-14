import json
import os
import shutil
from tqdm import tqdm


def merge_coco_datasets(output_path, *dataset_info, copy=False):
    # Initialize merged dataset
    merged_dataset = {"images": [], "annotations": [], "categories": []}

    # Initialize offsets for image_id and annotation_id
    image_id_offset = 0
    annotation_id_offset = 0

    # Create a merged image folder
    output_image_folder = os.path.join(os.path.dirname(output_path), "images")
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)

    for label, dataset_path, dataset_json in dataset_info:
        # Load each dataset
        with open(dataset_json, "r") as dataset_file:
            dataset = json.load(dataset_file)

        # Append data to merged dataset
        for image in dataset["images"]:
            image["id"] += image_id_offset
            image["file_name"] = label + "_" + image["file_name"]
            merged_dataset["images"].append(image)

        for annotation in dataset["annotations"]:
            annotation["id"] += annotation_id_offset
            annotation["image_id"] += image_id_offset
            merged_dataset["annotations"].append(annotation)

        merged_dataset["categories"] += dataset["categories"]

        # Copy images to the merged image folder
        if copy:
            for image_info in tqdm(dataset["images"]):
                image_path = os.path.join(
                    dataset_path, image_info["file_name"].split("_")[1]
                )
                new_image_path = os.path.join(
                    output_image_folder, image_info["file_name"]
                )
                shutil.copyfile(image_path, new_image_path)

        # Update image_id and annotation_id offsets
        image_id_offset += max(image["id"] for image in dataset["images"]) + 1
        annotation_id_offset += (
            max(annotation["id"] for annotation in dataset["annotations"]) + 1
        )
    # Save the merged dataset to a new COCO JSON file
    with open(output_path, "w") as output_file:
        json.dump(merged_dataset, output_file)


def main():
    dataset1_json = "/CV/gaobiaoli/dataset/worker-Dataset/CIS-worker.json"
    dataset2_json = "/CV/gaobiaoli/dataset/worker-Dataset/MOCS-worker.json"
    dataset1_path = "/CV/gaobiaoli/dataset/worker-Dataset/CIS"
    dataset2_path = "/CV/gaobiaoli/dataset/worker-Dataset/MOCS"
    output_path = "/CV/gaobiaoli/project/mmdetection/data/worker/full.json"
    label1 = "CIS"
    label2 = "MOCS"

    merge_coco_datasets(
        output_path,
        (label1, dataset1_path, dataset1_json),
        (label2, dataset2_path, dataset2_json),
    )


if __name__ == "__main__":
    main()
