import pytorch3d
import os
from pytorch3d.io import load_obj, save_obj
import torch
import argparse
import trimesh
import numpy as np

def normalize_to_bounding_box_unit_scale(obj_path, output_path):
    # Mesh laden
    mesh = trimesh.load(obj_path, process=False)
    
    # Mittelpunkt der Bounding Box berechnen
    min_bounds = mesh.vertices.min(axis=0)
    max_bounds = mesh.vertices.max(axis=0)
    centroid = (min_bounds + max_bounds) / 2.0
    
    # Verschieben zum Ursprung
    mesh.vertices -= centroid
    
    # Skalierung so, dass die längste Seite der Bounding Box genau 1 ist
    bbox_size = max_bounds - min_bounds
    max_extent = np.max(bbox_size)
    mesh.vertices /= max_extent
    
    # Normalisiertes Mesh speichern
    mesh.export(output_path)
    print(f"Normalized mesh saved to {output_path}")


def main(args):
        
    if args.input is None:
        print('No FLAME head given. Needs head_prior.obj to work')
        return -1
    
    path_to_scene = args.input
    
    verts, faces, _ =  load_obj(os.path.join(path_to_scene, 'head_prior.obj'))
    idx_wo_eyes, faces_wo_eyes = torch.load('./data/idx_wo_eyes.pt'), torch.load('./data/faces_wo_eyes.pt')

    save_obj(os.path.join(path_to_scene, 'head_prior_wo_eyes_no_scale.obj'), verts[idx_wo_eyes], faces_wo_eyes)
    
    normalize_to_bounding_box_unit_scale(os.path.join(path_to_scene, 'head_prior_wo_eyes_no_scale.obj'), os.path.join(path_to_scene, 'head_prior_wo_eyes.obj'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--input', type=str, default=None, help='path to head_prior.obj')
    
    args, _ = parser.parse_known_args()
    args = parser.parse_args()
    
    main(args)