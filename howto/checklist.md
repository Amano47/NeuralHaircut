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
                    |-- sparse
                    |-- dense
                    |-- sparse_txt

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

 