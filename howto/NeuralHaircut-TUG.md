# Neural Haircut: Step by step Guide

This is a step by step guide to use Neural Haircut with your own data.  
Sometimes it is not very clear in the official documentation, what you have to do specifically at that point and they just say: go read the entire repo or something. idk


## Table of Contents

1. [Installing](#git-repo-initialization-and-stuff)  
	1.1 [Git and Conda](#1-clone-repo-and-create-conda-environment)  
	1.2 [Submodules](#2-init-submodules)  
	1.3 [npbgpp](#3-setup-npbgpp)  
	1.4 [Pretrained models](#4-download-pretrained-neuralhaircut-models-from-google-drive)  

2. [Usage](#)

---

## 1. Installing

<details>

#### 1. Clone

Clone the git repository.

Create a new Conda environment with the given [requirements](neural_haircut.yaml) file.

```bash
git clone https://github.com/Amano47/NeuralHaircut.git
cd NeuralHaircut
conda env create -n neuralhaircut -f neural_haircut.yaml
conda activate neuralhaircut
```

#### 2. Init Submodules

Initialize the Submodules [CDGNet](https://github.com/tjpulkl/CDGNet), [MODNet](https://github.com/ZHKKKe/MODNet), [NeuS](https://github.com/Totoro97/NeuS), [k-diffusion](https://github.com/crowsonkb/k-diffusion) and [npbgpp](https://github.com/rakhimovv/npbgpp) with:  

```bash
git submodule update --init --recursive
```

#### 3. setup npbgpp

Run the setup code for npbgpp

```bash
cd npbgpp
python setup.py build develop
cd ..
```

#### 4. Download pretrained NeuralHaircut models from Google Drive

Pretrained Models for the second stage are in this Google Drive, provided by the original Author of Neural Haircut.

If gdown doesn't work properly, you can go to this link and download it manually, or you can visit the troubleshoot guide of the [gdown repository](https://github.com/wkentaro/gdown).

```bash
gdown --folder https://drive.google.com/drive/folders/1TCdJ0CKR3Q6LviovndOkJaKm8S1T9F_8
```

</details>

---

## 2. Usage: Executing the code

Assuming you have the preprocessed files and data to run the code, which is explained in the next Part [3. Preprocess](#3-preprocess-custom-data), you need to follow these steps in order to obtain the 

1. 



--- 
## 3. Preprocess custom Data

Now we are getting into the part, where we preprocess our photos to put them into a folder and run the thing for 6 days.

To make it a bit more clear, what and why something needs to happen, you can take a look at the result we need to get to: [implicit-hair-data/](https://drive.usercontent.google.com/download?id=1CADXQfC2IgxmFLwcLrm4G3ilWpW1g_PA&authuser=0) <- this is a folder with the example data they generously gave us to look at and decipher. The data in there, combined with the example config files in the repo, are usable to do a test run (if you want to wait a week or so on a single A100-80GB).

The structure is also written in the repo under [preprocess_custom_data](https://github.com/SamsungLabs/NeuralHaircut/tree/main/preprocess_custom_data) 

---
#### 5. Get Pretrained Model Files from PIXIE and SMPLX (follow multiview_optimization md in repo)
	1. create accounts on their websites (I recommend with same email and password)
		- https://pixie.is.tue.mpg.de/
		- https://smpl-x.is.tue.mpg.de/

	2. follow the Manual on PIXIE https://github.com/yfeng95/PIXIE/blob/master/Doc/docs/getting_started.md

	3. copy the following files into your repo in multiview_optimization
		-  SMPL-X__FLAME_vertex_ids.npy 
		-  smplx_extra_joints.yaml
		-  SMPLX_NEUTRAL_2020.npz

	4. change the path to them in `utils/config.py`

```python
12 	    cfg.pixie_dir = /path/to/dir/
```

#### 6. PIXIE: initialization_pixie
