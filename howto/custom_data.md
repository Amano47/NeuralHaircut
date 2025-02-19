# 3. Prepare Custom Data

## ToC

[3.1 PIXIE and SMPLX](#31-get-pretrained-model-files-from-pixie-and-smplx-follow-multiview_optimization-md-in-repo)  
[3.2 PIXIE; initialization_pixie](#32-pixie-initialization_pixie)  
[3.3 Masks](#33-silhouette-and-hair-masks)  
[3.4 Confidence- and Orientationmaps](#34-orientation-and-confidence-maps)  
[3.5 COLMAP and MeshLab](#35-colmapmeshlab)  
[3.6 scale.pickle](#36-transform-scene-into-unit-sphere)  
[3.7 OpenPose Keypoints](#37-openpose-keypoint)  
[3.8 Training Views](#38-define-views-optional)  
[3.9 FLAME Head](#39-flame-head)


### 3.1 Get Pretrained Model Files from PIXIE and SMPLX (follow multiview_optimization md in repo)
	
1. create accounts on their websites
	- [PIXIE](https://pixie.is.tue.mpg.de/)
	- [SMPLX](https://smpl-x.is.tue.mpg.de/)

2. follow the Manual on PIXIE https://github.com/yfeng95/PIXIE/blob/master/Doc/docsgetting_started.md  
	- create Conda Environment  
	- download models

3. change the path to them in `src/multiview_optimization/utils/config.py`

Set the path to the models to the `/data` folder in the installed PIXIE folder, you just downloaded. There are all Models for Pixie and SMPLX

```python
12 	    cfg.pixie_dir = /path/to/PIXIE/data/ # in PIXIE
```

### 3.2 PIXIE: initialization_pixie

A **simple solution** is implemented by User [@ypan98](https://github.com/ypan98) in his fork of PIXIE, called [pixie_initialization.py](https://github.com/ypan98/PIXIE/blob/master/demos/pixie_initialization.py).

- go to his fork and download the file  

run it with:

```bash
python demos/pixie_initialization.py --input_path /path/to/your/image/folder --save_folder /TestSamples/face/CASE/
```

Add the following args to get more results:  
- `--showBody True` 
- `--saveImages True`  
- `--saveObj True`  
- `--saveGif True`

All the results are saved in the save folder.

### 3.3 Silhouette and Hair Masks

To generate silhouettes, we use [MODNet](/MODNet/) and for hair masks [CDGNet](/CDGNet/).  

1. Download MODNet Model

    MODNet : [link to MODNet/pretrained](https://github.com/ZHKKKe/MODNet/tree/master/pretrained) | download the file `modnet_photographic_portrait_matting.ckpt`  
    __Save__ the file in `/MODNet/pretrained/` (easier for executing later) 

2. Download CDGNet Model

    CDGNet : ~~[official link](https://github.com/tjpulkl/CDGNet/blob/9daf7ddee6045c151c90a2e300946ea5f5717591/README.md?plain=1#L22)~~ which is **outdated** | Download `LIP_epoch_149.pth` (the file has to be ~305 MB in size)  
    **[OneDrive Link](https://onedrive.live.com/?redeem=aHR0cHM6Ly8xZHJ2Lm1zL2YvcyFBaGZRbUVIelk1NFlhMmdHYXNsWG5NMklQQ2s%5FZT1waGs1bWU&id=189E63F34198D017%21131&cid=189E63F34198D017)** from [Monohair](https://github.com/KeyuWu-CS/MonoHair)    

    __Save__ the file in `/CDGNet/snapshots/` (create the directory)  

3. Calculate Masks

    Execute the code with  

```bash
python preprocess_custom_data/calc_masks.py --scene_path ./implicit-hair-data/data/SCENE_TYPE/CASE/
```

If you saved the pretrained models in another directory (or on another drive), use the args  
- `--MODNET_ckpt`
- `--CDGNET_ckpt`

You now should have the subfolders `masks/` and `hair_masks/` under `CASE/` with masks of the image and the hair.

### 3.4 Orientation and Confidence Maps

Calculate orientation maps and confidence maps with

```bash
python preprocess_custom_data/calc_orientation_maps.py --img_path ./implicit-hair-data/data/SCENE_TYPE/CASE/image --orient_dir ./implicit-hair-data/data/SCENE_TYPE/CASE/orientation_maps --conf_dir ./implicit-hair-data/data/SCENE_TYPE/CASE/confidence_maps
```

This should create the subdirectories `orientation_maps/` and `confidence_maps/` with the data. This also takes a while.

### 3.5 Colmap/Meshlab

The original document states, that this step is optional, but the files seem to be required in some stages afterwards.

#### (i) COLMAP

1. install Colmap

    Install COLMAP SfM with Conda

```bash
conda create -n colmap
conda install colmap
conda activate colmap
```

2. run `automatic_reconstructor`

    run the automatic reconstructor from the terminal with

```bash
colmap automatic_reconstructor --workspace_path ./implicit-hair-data/SCENE_TYPE/CASE/colmap --image_path ./implicit-hair-data/SCENE_TYPE/CASE/image
```

This runs for ~1.5 hours (depending on image quality and quantitiy).

It should run fine with normal video frames, but in case colmap can't identify camera positions and features, give colmap the masks you created earlier, by simply adding the path with: 

```bash
--mask_path ./implicit-hair-data/SCENE_TYPE/CASE/mask
```


3. run `model_converter`

    In the subdirectory of your colmap workspace `./implicit-hair-data/SCENE_TYPE/CASE/colmap/` should be `sparse/0/` where binaries are generated.  

Convert the three files with  

```bash
mkdir CASE_NAME/colmap/sparse_txt 

colmap model_converter --input_path CASE_NAME/colmap/sparse/0  --output_path CASE_NAME/colmap/sparse_txt --output_type TXT
```

This should convert the `.bin` to `.txt`, which is required for:

4. postprocess Colmap output

```bash
python preprocess_custom_data/colmap_parsing.py --path_to_scene  ./implicit-hair-data/data/SCENE_TYPE/CASE --save_path ./implicit-hair-data/data/SCENE_TYPE/CASE/colmap
```

This generates the folder and files:  
- `colmap/full_res_image/`  
- `colmap/cameras.npz`  
- `colmap/point_cloud.ply`

__!__ Be sure to copy or move the file `cameras.npz` out of `colmap/` to `Case/` one above.

#### (ii) MeshLab

We now want to get rid of the noise from `point_cloud.ply` and define the region of interest in [MeshLab](https://github.com/cnr-isti-vclab/meshlab)  

In the Testdata (`implicit-hair-data/data/monocular/person_0/`), the testperson is clearly visible as a pointcloud with next to none noise.  

1. Install MeshLab and load the `.ply`.   
2. double click on a point on the torso or face of your person to re-center the camera  
3. use the tool `Select Vertex Clusters` and try selecting the pointcloud of interest, while not to select too many outlying points  
4. invert your selection with Ctrl+Shift+I or `Filers > Selection > Invert Selection` and check the box `Invert Vertices`  
5. delete the vertices  

There are definitely other ways to do this, but this should reduce some of the noise from the background.

Export the pointcloud as `point_cloud_cropped.ply` and save it in your `CASE/` directory.

### 3.6 Transform scene into unit sphere

```bash
python preprocess_custom_data/scale_scene_into_sphere.py --case CASE --scene_type SCENE_TYPE --path_to_data ./implicit-hair-data/data/
```

This should create a file `scale.pickle` in `Case/`

### 3.7 OpenPose Keypoint

- Create a new directory in your data folder `openpose_kp`  

- Download the latest release of [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases)  

- go throug the installation guide  

    - if the models fail to download, go to [issue #1602](https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1602#issuecomment-641653411) and download it from the GDrive  

- run openpose with  

```bash
./build/examples/openpose/openpose.bin --image_dir image/ --render_pose 0 --display 0 --face --hand --write_json openpose_kp/
```

- if you use OpenPose on Windows, it should be the same, except use `.\bin\OpenPoseDemo.exe`

### 3.8 Define views (optional)

Define views, on which you want to train. Save it into `views.pickle`

### 3.9 FLAME head

(see also original doc [multiview optimization](/src/multiview_optimization/))  

The FLAME head is gonna be a `head_prior.obj`, which you can also see in the testdata.

1. Config file

- Create two new config files in [confs/](/src/multiview_optimization/confs/).  
- Copy the content of `confs/train_person_1.conf` into `confs/train_own_data_5.conf`  
- change the paths to the data accordingly to your own data    
- Do the same for `confs/train_person_1_.conf` and `confs/train_own_data_20.conf`.

2. Shell Script

- Create a new shell script in `scripts/`  
- Copy the contents of the given file `scripts/run_monocular_fitting.sh` into the new file and change the config file paths to your own data.

    <details>
    <summary> fit_armin.sh </summary>

    ```bash
    python fit.py --conf confs/train_armin.conf --batch_size 1 --train_rotation True    --save_path ./experiments/fit_armin_bs_1

    python fit.py --conf confs/train_armin.conf --batch_size 5 --train_rotation True    --save_path  ./experiments/fit_armin_bs_5 --checkpoint_path ./experiments/fit_armin_bs_1/  opt_params

    python fit.py --conf confs/train_armin_2.conf --batch_size 20 --train_rotation True     --train_shape True --save_path  ./experiments/fit_armin_bs_20_train_rot_shape   --checkpoint_path ./experiments/fit_armin_bs_5/opt_params
    ```

    </details>  
<br> 

- Only the last call of `fit.py` (which trains on a batch size of 20) uses the second config file, so be sure to match that

3. run your script

4. get FLAME mesh  
- after the script has finished, go to  
`experiments/fit_own_data/fit_own_data_bs_20_train_rot_shape/mesh/`  
- look for the last created mesh and rename it to `head_prior.obj`  
- copy it to your dataset 

---

## Troubleshoot 

If you encounter any Problem, look into the open and closed Issues of [NeuralHaircut](https://github.com/SamsungLabs/NeuralHaircut/issues)  

Some of them are also in my [Troubleshoot guide](/howto/troubleshoot.md)

### [Back to Overview](/howto/)