# Neural Haircut: Step by step Guide

This is a step by step guide to reconstruct Hair with your own data.  


## Table of Contents

1. [Installing](#git-repo-initialization-and-stuff)  
	1.1 [Setup](#11-setup)  
	1.2 [Submodules](#12-initialize-submodules)  
	1.3 [Pretrained models](#13-download-pretrained-neuralhaircut-models-from-google-drive)  

2. [Usage](#2-usage-running-the-code)  
	2.1 [First Stage](#21-geometric-reconstruction)  
	2.2 [Postprocess First Stage](/custom_dataset/postprocess.md#postprocess-first-stage)  
	2.3 [Second Stage](#23-strands-optimization)  

3. [Custom Data](#3-preprocess-custom-data)  

4. [Troubleshoot](#4-troubleshoot)

---

## 1. Installing

#### 1.1 Setup

Clone the git repository and create a new Conda environment with the given [requirements](neural_haircut.yaml) file:

```bash
git clone https://github.com/Amano47/NeuralHaircut.git
cd NeuralHaircut
conda env create -n neuralhaircut -f neural_haircut.yaml
conda activate neuralhaircut
```

#### 1.2 initialize Submodules

Initialize the Submodules [CDGNet](https://github.com/tjpulkl/CDGNet), [MODNet](https://github.com/ZHKKKe/MODNet), [NeuS](https://github.com/Totoro97/NeuS), [k-diffusion](https://github.com/crowsonkb/k-diffusion) and [npbgpp](https://github.com/rakhimovv/npbgpp) with:  

```bash
git submodule update --init --recursive
```

Run the setup code for npbgpp

```bash
cd npbgpp
python setup.py build develop
cd ..
```

#### 1.3 Download pretrained NeuralHaircut models from Google Drive

Pretrained Models for the second stage are in this Google Drive, provided by the original Author of Neural Haircut.

If gdown doesn't work properly, you can go to this link and download it manually, or you can visit the troubleshoot guide of the [gdown repository](https://github.com/wkentaro/gdown).

```bash
gdown --folder https://drive.google.com/drive/folders/1TCdJ0CKR3Q6LviovndOkJaKm8S1T9F_8
```
Save the folder like:
<details>
<summary>Folder Structure</summary>

Save the folder in the rootfolder of NeuralHaircut like
```bash
|-- NEURALHAIRCUT
	|-- docs
	|-- pretrained_models
		|-- strand_prior
			|-- strand_ckpt.pth
		|-- diffusion_prior
			|-- dif_ckpt.pth
	|- ...
	...
```
</details>

## 2. Usage: Running the code

**Prequisites:**
- testdata explained in [/example](/example/)   
or    
- [custom data](#3-preprocess-custom-data)  


**Caution:**
- geometric reconstruction (first stage) takes 1 day on a Nvidia 4090  
- strands reconstruction (second stage) takes 2 or more days on a Nvidia 4090  
_BUT_: a Nvidia A100 Tensor Core GPU (40 or 80GB VRAM) takes **three times longer** than on a 4090 (24GB VRAM)  
- the code can utilize one GPU at a time  



### 2.1  Geometric Reconstruction

First we run the first stage to get a rough reconstruction of your outer hair shell geometry and bust.

```bash
python run_geometric_reconstruction.py --case CASE_NAME --conf ./configs/SCENE_TYPE/neural_strands.yaml --exp_name first_stage_SCENE_TYPE_CASE
```

- You can add camera fitting with the flag `--train_cameras`  
- It is possible to continue training from checkpoints with `--is_continue`  
- for higher resolution mesh, add the flags `--mode_validation`


### 2.2 Postprocess first stage

Before running the second stage on your own dataset, do the following:  

__[Postprocess](/custom_dataset/postprocess.md)__

Be sure to do these steps, before running the strand optimizer.

### 2.3 Strands Optimization

After the copying is done, we can run the second stage  

```bash
python run_strands_optimization.py --case CASE --scene_type SCENE_TYPE --conf ./configs/SCENE_TYPE/neural_strands.yaml  --hair_conf ./configs/hair_strands_textured.yaml --exp_name second_stage_SCENE_TYPE_CASE
```

If you fitted the camera during the first stage, you need to change the config file to `./configs/SCENE_TYPE/neural_strands_w_camera_fitted.yaml`

### 2.4 Results

The result of the second stage is a `.ply` in your experiment save folder.  
It contains a pointcloud with colored/grouped points, which you can make into strands with `open3d.geometry.LineSet`, for which you would need to import open3d-python  

```bash
python scripts/points2strands.py --input hair_300000.ply --output .
```

It should connect the sturctured points into sets of lines, although the strand coluors are lost.

Each Strand in the pointcloud is assigned a RGBA value, such that every Point on the strand is colored with this RGBA value.
 
## 3. Preprocess custom data

It takes a lot of steps to create the dataset, which you need for running the first and second stage of Neural Haircut. The exact steps are written in: 
__[Prepare Custom Data](/custom_dataset/custom_data.md)__.  

It is also helpful to see the structure of the 
[implicit-hair-data/](https://drive.usercontent.google.com/download?id=1CADXQfC2IgxmFLwcLrm4G3ilWpW1g_PA&authuser=0) folder.  

**Overview**
1. get masks  
2. colmap
3. crop the pointcloud  
4. scale into sphere  
5. get orientation and confidence maps  
6. get pixie file  
7. get openpose keypoints  
8. fit FLAME head  


## 4. Troubleshoot

**[4 Troubleshoot Guide](/custom_dataset/troubleshoot.md)**

Think of it like the issue-board, but in clean.