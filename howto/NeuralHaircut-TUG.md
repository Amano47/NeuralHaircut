# Neural Haircut: Step by step Guide

This is a step by step guide to use Neural Haircut with your own data.  
Sometimes it is not very clear in the official documentation, what you have to do specifically at that point and they just say: go read the entire repo or something. idk


## Table of Contents

1. [Installing](#git-repo-initialization-and-stuff)  
	1.1 [Git and Conda](#11-clone)  
	1.2 [Submodules](#12-init-submodules)  
	1.3 [npbgpp](#13-setup-npbgpp)  
	1.4 [Pretrained models](#4-download-pretrained-neuralhaircut-models-from-google-drive)  

2. [Usage](#2-usage-running-the-code)  
	2.1 [First Stage](#21-geometric-reconstruction)  
	2.2 [Postprocess](/howto/postprocess.md#postprocess-first-stage)  
	2.3 [Second Stage](#23-strands-optimization)  

3. [Custom Data](#3-preprocess-custom-data)  

4. [Troubleshoot](#4-troubleshoot)

---

## 1. Installing

#### 1.1 Clone

Clone the git repository.

Create a new Conda environment with the given [requirements](neural_haircut.yaml) file.

```bash
git clone https://github.com/Amano47/NeuralHaircut.git
cd NeuralHaircut
conda env create -n neuralhaircut -f neural_haircut.yaml
conda activate neuralhaircut
```

#### 1.2 Init Submodules

Initialize the Submodules [CDGNet](https://github.com/tjpulkl/CDGNet), [MODNet](https://github.com/ZHKKKe/MODNet), [NeuS](https://github.com/Totoro97/NeuS), [k-diffusion](https://github.com/crowsonkb/k-diffusion) and [npbgpp](https://github.com/rakhimovv/npbgpp) with:  

```bash
git submodule update --init --recursive
```

#### 1.3 setup npbgpp

Run the setup code for npbgpp

```bash
cd npbgpp
python setup.py build develop
cd ..
```

#### 1.4 Download pretrained NeuralHaircut models from Google Drive

Pretrained Models for the second stage are in this Google Drive, provided by the original Author of Neural Haircut.

If gdown doesn't work properly, you can go to this link and download it manually, or you can visit the troubleshoot guide of the [gdown repository](https://github.com/wkentaro/gdown).

```bash
gdown --folder https://drive.google.com/drive/folders/1TCdJ0CKR3Q6LviovndOkJaKm8S1T9F_8
```

## 2. Usage: Running the code

Assuming you have the preprocessed files and data to run the code, which is explained in the next Part [3. Preprocess](#3-preprocess-custom-data), or the [test dataset](/example/), you need to follow these steps in order to get the model of your hair.  

There is also the guide for the testdata in [/example](/example/) 

Note that these steps take a long time, even with powerful GPUs with high V-Memory capacity and Bandwith  
- first stage 3~4 days  
- second stage 6~7 days  

The Code is not written for parallelisation on Nvidia GPUs, so the number of GPUs $x$ with $x > 1$ does not matter.  

It is marginally faster to compute with up to 40 GB of VRAM, but 24 GB should perform around the same. 

---

### 2.1  Geometric Reconstruction

First we run the first stage, the [geometric reconstruction code](/run_geometry_reconstruction.py) to get a rough reconstruction of your outer hair shell geometry and bust.

```bash
python run_geometric_reconstruction.py --case CASE_NAME --conf ./configs/SCENE_TYPE/neural_strands.yaml --exp_name first_stage_SCENE_TYPE_CASE
```

- You can add camera fitting with the flag `--train_cameras`  
- It is possible to continue training from checkpoints with `--is_continue`  
- for higher resolution mesh, add the flags `--mode_validation`


### 2.2 Postprocess first stage

Before running the second stage on your own dataset, do the following:  

__[Postprocess](/howto/postprocess.md)__

### 2.3 Strands Optimization

After the copying is done, we can run the second stage  

```bash
python run_strands_optimization.py --case CASE --scene_type SCENE_TYPE --conf ./configs/SCENE_TYPE/neural_strands.yaml  --hair_conf ./configs/hair_strands_textured.yaml --exp_name second_stage_SCENE_TYPE_CASE
```

If you fitted the camera during the first stage, you need to change the config file to `./configs/SCENE_TYPE/neural_strands_w_camera_fitted.yaml`

 
## 3. Preprocess custom data

It takes a lot of steps to create the dataset, which you need for running the first and second stage of Neural Haircut. The exact steps are written in: 
__[Prepare Custom Data](/howto/custom_data.md)__.  

It is also helpful to see the structure of the 
[implicit-hair-data/](https://drive.usercontent.google.com/download?id=1CADXQfC2IgxmFLwcLrm4G3ilWpW1g_PA&authuser=0) folder.  
You may use it as a checklist.

## 4. Troubleshoot

I personally had issues creating custom data, so here are some of the issues I had encountered and the *tricks* I used to solved them.  

Before that, I tested Neural Haircut on these specs:
- Nvidia A100-80GB GPU  
- AMD EPYC 7713 64-Core CPU  
- 2038 GiB Memory  

- Lightstage (for custom data)

There are up- and downsides to some of the component, like the Lightstage.  
At first glance, it seems to be good for getting consistent lighting, near perfect images with no motion blurr and consistentdata, which could be good to test some Benchmarks against other hair recreation methods, like Gaussian Splatting, etc...  
But in reality, the number of photos you get from a Lightstage can be counted as a constraint for training and colmapping.  


