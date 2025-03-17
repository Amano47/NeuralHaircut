import pytorch3d
import os
from pytorch3d.io import load_obj, save_obj
import torch
import argparse

def main(args):
        
    if args.input is None:
        print('No FLAME head given. Needs head_prior.obj to work')
        return -1
    
    path_to_scene = args.input
    
    verts, faces, _ =  load_obj(os.path.join(path_to_scene, 'head_prior.obj'))
    idx_wo_eyes, faces_wo_eyes = torch.load('./data/idx_wo_eyes.pt'), torch.load('./data/faces_wo_eyes.pt')

    save_obj(os.path.join(path_to_scene, 'head_prior_wo_eyes.obj'), verts[idx_wo_eyes], faces_wo_eyes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--input', type=str, default=None, help='path to head_prior.obj')
    
    args, _ = parser.parse_known_args()
    args = parser.parse_args()
    
    main(args)