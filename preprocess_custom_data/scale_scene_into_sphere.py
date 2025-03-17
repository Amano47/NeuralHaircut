import trimesh
import numpy as np
import pickle
import argparse

import os



def main(args):
    
    # if there is no input
    if args.input is None:
        print('No directory! Need the path to point_cloud_cropped.ply')
        print('--input path/to/point_cloud_cropped.ply is needed as argument')
        return -1
    
    # if there is no point_cloud_cropped.ply file
    if os.path.isfile(os.path.join(args.input, 'point_cloud_cropped.ply')) is False:
        print('No point_cloud_cropped.ply found in directory.')
        print('--input path/to/point_cloud_cropped.ply is needed as argument')
        return -1
    
    path_to_scene = args.input

    pc = np.array(trimesh.load(os.path.join(path_to_scene, 'point_cloud_cropped.ply')).vertices)

    translation = (pc.min(0) + pc.max(0)) / 2
    scale = np.linalg.norm(pc - translation, axis=-1).max().item() / 1.1

    tr = (pc - translation) / scale
    
    print(f'Debug: tr.min: {tr.min()}; tr.max: {tr.max()}') # Debug
    
    assert tr.min() >= -1 and tr.max() <= 1

    print('Scaling into the sphere', tr.min(), tr.max())

    # original
    # d = {'scale': scale,
    #     'translation': list(translation)}

    # modified to person_0
    d = {'scale': scale,
        'translation': translation}

    with open(os.path.join(path_to_scene, 'scale.pickle'), 'wb') as f:
        pickle.dump(d, f)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--input', type=str, default=None, help='path to where point_cloud_cropped.ply is')
    
    args, _ = parser.parse_known_args()
    args = parser.parse_args()

    main(args)