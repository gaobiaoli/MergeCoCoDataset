import cv2
import json
import random
import argparse
class COCOVisualizer:
    def __init__(self, folder_path, coco_json_path):
        self.folder_path = folder_path
        self.coco_json_path = coco_json_path
        self.image_index = 0
        self.load_coco_data()

    def load_coco_data(self):
        with open(self.coco_json_path, 'r') as json_file:
            self.coco_data = json.load(json_file)

    def visualize_annotations(self, image_path, annotations):
        image = cv2.imread(image_path)

        for annotation in annotations:
            bbox = annotation['bbox']
            cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), 
                          (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), 
                          (255, 0, 0), 2)

        cv2.imshow('COCO Visualizer', image)

    def show_random_image(self):
        image_info = random.choice(self.coco_data['images'])
        image_id = image_info['id']
        image_path = f"{self.folder_path}/{image_info['file_name']}"
        annotations = [anno for anno in self.coco_data['annotations'] if anno['image_id'] == image_id]
        self.visualize_annotations(image_path, annotations)

    def run(self):
        cv2.namedWindow('COCO Visualizer', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('COCO Visualizer', 800, 600)

        while True:
            self.show_random_image()
            key = cv2.waitKey(0)

            if key == 27:  # ESC key
                break
            elif key == 32:  # Space key (next image)
                self.image_index = (self.image_index + 1) % len(self.coco_data['images'])

        cv2.destroyAllWindows()

# 示例用法
parser = argparse.ArgumentParser(description='COCO Visualizer')
parser.add_argument('--folder_path', type=str,default='/CV/gaobiaoli/dataset/worker-Dataset/MOCS' ,help='Path to the image folder')
parser.add_argument('--coco_json_path', type=str,default='/CV/gaobiaoli/dataset/worker-Dataset/MOCS-worker.json', help='Path to the COCO JSON file')

args = parser.parse_args()


visualizer = COCOVisualizer(args.folder_path, args.coco_json_path)
visualizer.run()