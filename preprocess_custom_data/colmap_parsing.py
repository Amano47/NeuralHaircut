import numpy as np
import matplotlib.pyplot as plt
import shutil
import os
from tqdm import tqdm
import trimesh
import argparse

from scipy.spatial.transform import Rotation as R

    
def main(args):
    
    images_file = f'{args.input}/colmap/sparse_txt/images.txt'
    points_file = f'{args.input}/colmap/sparse_txt/points3D.txt'
    camera_file = f'{args.input}/colmap/sparse_txt/cameras.txt'
    
    # Parse colmap cameras and used images
    with open(camera_file) as f:
        lines = f.readlines()

        u = float(lines[3].split()[4])
        h, w = [round(float(x)) for x in lines[3].split()[5: 7]]

        intrinsic_matrix = np.array([
            [u, 0, h, 0],
            [0, u, w, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
    with open(images_file) as f:
        images_file_lines = f.readlines()

    n_images = len(images_file_lines[4:]) // 2

    data = {}

    image_names = []
    for i in range(n_images):

        line_split = images_file_lines[4 + i * 2].split()
        image_id = int(line_split[0])


        q = np.array([float(x) for x in line_split[1: 5]]) # w, x, y, z
        t = np.array([float(x) for x in line_split[5: 8]])

        image_name = line_split[-1]
        image_names.append(image_name)

        extrinsic_matrix = np.eye(4)
        extrinsic_matrix[:3, :3] = R.from_quat(np.roll(q, -1)).as_matrix()
        extrinsic_matrix[:3, 3] = t

        data[image_name] = intrinsic_matrix @ extrinsic_matrix    


    with open(points_file) as f:
        points_3d_lines = f.readlines()

    points = []
    colors = []

    for line in points_3d_lines[3:]:
        split_line = line.split()
        point = np.array([float(v) for v in split_line[1: 4]])
        color = np.array([int(v) for v in split_line[4: 7]])
        points.append(point)
        colors.append(color)

    # print(points)

    if len(points) == 0 and len(colors) == 0:
        print("points3D.txt is empty")
        points.append(0)
        colors.append(0)
    
    points = np.stack(points)
    colors = np.stack(colors)
    
    output_folder = args.output
    images_folder = os.path.join(args.input, 'image') # modified from video_frames/  to image/
    
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'full_res_image'), exist_ok=True)
    
    cameras = []
    debug = False
    
    i = 0

    for i, k in enumerate(data.keys()):
        
        if not os.path.exists(os.path.join(images_folder, k)):
            print(f'Warning: File {k} not found. Skipping')
            continue
        
        filename = f'img_{i:04}.png'     
        
        T = data[k]
        cameras.append(T)
        shutil.copyfile(os.path.join(images_folder, k), os.path.join(output_folder, 'full_res_image', filename))

    np.savez(os.path.join(output_folder, 'cameras.npz'), np.stack(cameras))
    trimesh.points.PointCloud(points).export(os.path.join(output_folder, 'point_cloud.ply'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(conflict_handler='resolve')

    parser.add_argument('--input', default='./implicit-hair-data/data/monocular/person_1', type=str, help='path to /SCENE_TYPE/CASE/')
    parser.add_argument('--output', default='./implicit-hair-data/data/monocular/person_1/colmap', type=str, help='path to colmap directory in CASE')

    
    args, _ = parser.parse_known_args()
    args = parser.parse_args()

    main(args)