## Postprocess first Stage


#### 2.2.1 Copy Checkpoints for __hair sdf__ , __orientation field__ and __obtained meshes__ to the scene folder (for convenience)  

```bash
python ./preprocess_custom_data/copy_checkpoints.py --case CASE --exp_name first_stage_reconctruction_CASE --conf_path ./configs/SCENE_TYPE/neural_strands*.yaml
```

#### 2.2.2 Extract visible hair surface from sdf

```bash
python ./preprocess_custom_data/extract_visible_surface.py --conf_path ./configs/SCENE_TYPE/neural_strands*.yaml  --case CASE --scene_type SCENE_TYPE --img_size 2160 --n_views 2
```

This creates the file `hair_outer.ply` in your dataset `./implicit_hair_dataset/data/SCENE_TYPE/CASE/`  

#### 2.2.3 Remesh `hair_outer.ply` to ~10k vertices for acceleration

Note, you could use either Meshlab to do that or any other library.  
Also, for scenes with long hair do remeshing for final_head.ply to properly deal with occlusions.  
You need to change the value `render["mesh_path"]` to  `final_head_remeshed.ply` path in `./configs/hair_strands_textured.yaml`.

#### 2.2.4 Extract scalp region for diffusion using the distance between hair sdf to scalp

```bash
python ./preprocess_custom_data/cut_scalp.py --distance 0.07 --conf_path ./configs/SCENE_TYPE/neural_strands*.yaml  --case CASE --scene_type SCENE_TYPE --path_to_data ./implicit-hair-data/data 
```

Note, you could change the distance between scalp and hair sdf if obtained scalp mesh is too small or too big for current hairstyle.  

After this step in  `./implicit-hair-data/data/SCENE_TYPE/CASE`you would obtain `cut_scalp_verts.pickle`, `scalp.obj`, `dif_mask.png`.