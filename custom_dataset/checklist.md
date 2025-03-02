# Checklist

Follow these rough steps to get your dataset and training.

## Dataset Filestructure

```bash

|-- NeuralHaircut/implicit-hair-data
    |-- data
        |-- h3ds
        |-- monocular
            |-- case_name
                |-- video_frames  # after parsing .mp4 (optional)
                |-- colmap # (optional) 
                    |-- full_res_image
                    |-- cameras.npz
                    |-- point_cloud.ply
                    |-- database.db
                    |-- sparse/
                        |-- 0/
                        |-- project.ini
                    |-- dense/
                        |-- ...
                    |-- sparse_txt/
                |-- cameras.npz    # camera parameters
                |-- image
                |-- mask
                |-- hair_mask
                |-- orientation_maps
                |-- confidence_maps
                |-- dif_mask.png # scalp masking for diffusion model
                |-- cut_scalp_verts.pickle # scalp vertex for hairstyle
                |-- head_prior.obj  # FLAME prior head
                |-- head_prior_wo_eyes.obj # version wo eyes
                |-- scale.pickle # scale the scene into unit sphere
                |-- views.pickle # index of chosen views (optional)
                |-- initialization_pixie # initialization for shape, expression, pose, ...
                |-- openpose_kp # needed for mesh prior fitting (optional)   
                |-- fitted_cameras.pth # Checkpoint for fitted cameras (optional)

```

## Preprocess

1. create directories  
    - implicit-hair-data/data/monocular/CASE/  
    - implicit-hair-data/data/monocular/CASE/image  
    - implicit-hair-data/data/monocular/CASE/colmap  
    - implicit-hair-data/data/monocular/CASE/colmap/sparse_txt

2. make masks  
    - `python calc_masks.py --input implicit-hair-data/data/monocular/CASE/`

3. colmap reconstruct  
    - `colmap automatic_reconstructor --workspace_path colmap/ --image_path image/ --mask_path mask/`  

4. run colmap_parser  
    - `colmap_parsing.py --input implicit-hair-data/data/monocular/CASE/ --output implicit-hair-data/data/monocular/CASE/`  

5. crop pointcloud  

6. scale into sphere  
    - `python scale_scene_into_sphere.py --input implicit-hair-data/data/monocular/CASE/`  

7. calculate orientation and confidence maps  

8. get initialization_pixie  

9. get OpenPose Keypoints  

10. fit FLAME head  

## first stage

11. run geometric reconstruction  

## Interprocess

12. copy checkpoints  

13. Extract visible hair surface from sdf  

14. Remesh hair_outer.ply to ~10k vertex for acceleration  

15. Extract scalp region for diffusion using the distance between hair sdf to scalp  

## second stage

16. run strands optimization

## Postprocess

17. make strands from pointcloud


[go back to overview](/custom_dataset/readme.md)