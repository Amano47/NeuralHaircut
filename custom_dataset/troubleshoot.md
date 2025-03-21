# 4. Troubleshoot Guide

Most of the things written here should not have come up, if you followd my [Guide](/custom_dataset/), but here are some types of errors I encountered.

GL;HF

## ToC

4.1 [Conda Environment](#41-conda-environment)  
4.2 [Colmap](#42-colmap)  
4.3 [Mask Models](#43-mask-models)  
4.4 [Masks Code](#44-masks-b)  
4.5 [Pixie (initialization)](#45-pixie)  
4.6 [MeshLab](#46-meshlab)  
4.7 [OpenPose](#47-openpose)  
4.8 [FLAME fitting](#48-flame-fitting)
4.8.1


## 4.1 Conda environment

You may have conflicts between packages when creating the conda environment with [neural_haircut.yaml](/neural_haircut.yaml).  

Change in [Line 165](../neural_haircut.yaml#L165)

```yaml
- notebook=6.5.3=py39h06a4308_0 #from this 
- notebook=6.5.* #to this
```


## 4.2 Colmap

Colmap is a optional step in the preprocessing step for custom data. But if there are not many images to extract features and to match these, then it is a rather difficult task to get usable results from colmap for the [preprocessing step](/preprocess_custom_data/readme.md#step-1-optional-run-colmap-sfm-to-obtain-cameras).  

If you have masks or silhouettes of your photos/frames, then you can use them in the automatic reconstructor of colmap with  
```bash
colmap automatic_reconstructor --workspace_path ./colmap/ --image_path ./image/ --mask_path ./masks/
```

```bash
|-- case_name			# run the command from here
	|-- video_frames
	|-- image			# all images
	|-- mask			# the masks created from the images
	|-- colmap
		|-- sparse		# this gets automatically generated by colmap
			|-- 0
				|-- image.bin     <--+
				|-- camera.bin    <--+-- get generated by automatic_reconstructor 
				|-- points3D.bin  <--+
	|-- ...				# rest of your preprocess files
	...

```

You can generate the masks with [Step 2.x]() (the one after Colmap)

There is also a difference when using the automatic reconstructor from colmap or doing it in the GUI, and using different file types, such as jpg and png.

## 4.3 Mask Models

The mask generator is very straight forward.  
It uses [MODNet](/MODNet/) for silhouettes, so whole body masks and [CDGNet](/CDGNet/) for hair masks.  
The pretrained models are not inside the submodules, so you have to download them from the linked Google Drive.  

**! Be careful !**  
There are at least two different versions of the CDGNet file, which all are named the same `LIP_epoch_149.pth` only with slightly different sizes (255MB and 305MB).  
The smaller one, which is "outdated" and also gets referred in the Master and other Repositories, doesn't work properly and stops the python code with errors.  

+++++++++++++++++++++++++++++  
+**[this is the one, which works in Jan 2025](https://onedrive.live.com/?redeem=aHR0cHM6Ly8xZHJ2Lm1zL2YvcyFBaGZRbUVIelk1NFlhMmdHYXNsWG5NMklQQ2s%5FZT1waGs1bWU&id=189E63F34198D017%21107&cid=189E63F34198D017)**+  
+++++++++++++++++++++++++++++  

Put it into `/CDGNet/snapshots/` and the code should be fine.  



## 4.4 Masks python code (solution already implemented)

Another issue with the mask generator is, that it seems to have problems with the code itself in [line 159](https://github.com/Amano47/NeuralHaircut/blob/1dbdd07797458e6e0000bd3a02f3092d419d1756/preprocess_custom_data/calc_masks.py#L159).

To resolve it:  

```python
...
156     state_dict = model.state_dict().copy()
157     state_dict_old = torch.load(args.CDGNET_ckpt, map_location='cpu')
158
159-    for key, nkey in zip(state_dict_old.keys(), state_dict.keys()): # delete this line
159+    state_dict_keys = list(state_dict.keys()) 
160+    for key, nkey in zip(state_dict_old.keys(), state_dict_keys):
161         if key != nkey:
162             # remove the 'module.' in the 'key'
163             state_dict[key[7:]] = deepcopy(state_dict_old[key])
...
```

So that the counting state_dict doesn't get mutated.  
This is from [Issue #13](https://github.com/SamsungLabs/NeuralHaircut/issues/13)  



## 4.5 Pixie

If you have troubles with creating an account for PIXIE and SMPLX, then refer to the according repositories, as the installation is documented there.  



## 4.6 MeshLab

In Step 4 of preparing your own custom data, it is required to install MeshLab and cleaning up the point cloud created by Colmap SfM.  

You may use a device, where you have access to a GUI and install MeshLab on it.  
[MeshLab Download page](https://www.meshlab.net/#download)  

Import your point cloud (point_cloud.ply, created by the colmap parser code) and use the various selection tools to select the unwanted vertices and delete them.  

The Support Page has some Tutorials for how to use MeshLab: [here](https://www.meshlab.net/#support)  

## 4.7 OpenPose

For OpenPose, you need Ubuntu 20.04 or earlier, as Caffe is not compiled for later versions.  
On Windows, you can download the pre-compiled Executable in the releases section.  
- look for CUDA prequisites in the [Windows Portable Demos section](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#windows-portable-demo)

- For fitting the FLAME model, you should get OpenPose keypoints or FaceAlignment Keypoints and save them as json files in a subfolder `openpose_kp`
- There should be one json file for each image you use   

- Download [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases)  
	- there is an Option for non CUDA machines  

### Models not downloading

- get the `.caffeemodel` file from this Google Drive as mentioned in [Issue #1602](https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1602#issuecomment-641653411)  
- put each model file into the directory with the same name in `/openpose/models/`  

## 4.8 FLAME fitting

If you encounter errors with when fitting the FLAME head with `fit.py`, then there should be two types of errors:  

1. the paths in the configs are wrong  
=> refer to [4.8.1](#481-file-path-error)

2. the number of colmapped and original images are not the same  
=> refer to [4.8.2](#482-image-numbers)

### 4.8.1 file path error

The `fit_original.py` code assumes, that you have every file in your dataset ready, but the file `fitted_cameras.pth` is not generated before the first stage.  
This means, that this file can not be aquired in the preprocess of the dataset.  

The current code `fit.py` replaces the original code and correctly implements the argument parser to use this optional file, only if the path is given.

### 4.8.2 image numbers

When you try to run `fit.py` or the script of that in `scripts/fit_person_1.sh` in Step 7 of [Multiview Optimization](/src/multiview_optimization/), you encounter the error, where there is no `fitted_cameras.pth` file in your dataset. This is a file, which you can get by running the [first stage](/run_geometry_reconstruction.py).  
The "easiest" way to solve this problem, is by either modifying the code to make the requirement of this file optional and thus ignoring the it, or copying the code from another fork of Neuralhaircut by [ypan98](https://github.com/ypan98/NeuralHaircut/tree/main). The corrected file [fit.py from ypan98](https://github.com/ypan98/NeuralHaircut/blob/2064ff912088782fc7426d5eba1a917cabeb8dc6/src/multiview_optimization/fit.py) does add some arguments, which you can optionaly add. The main running script [reconstruct_colmap.sh](https://github.com/ypan98/NeuralHaircut/blob/main/reconstruct_colmap.sh) (which also won't work in one try), calls the modified `fit.py` code in [Line 40 to 42](https://github.com/ypan98/NeuralHaircut/blob/2064ff912088782fc7426d5eba1a917cabeb8dc6/reconstruct_colmap.sh#L40).  

The script in this repository `fit_script.sh` is using the modified code, which is now named `fit_wo_fitted_cameras.py` with
```bash
./scripts/fit_script.sh $cuda_device_number $path_to_data_folder $output_folder $openpose_path
```

- `$cuda_device_number` : the GPU device number, like 0  
- `$path_to_data_folder` : most likely `../../implicit-hair-data/data/monocular/CASE`, if your data folder is located in the root dir of the porject  
- `$output_folder` : I recommend `./experiments/CASE`  
- `$openpose_path` : the path to your openpose keypoints, most likely located in your dataset folder `../../implicit-hair-data/data/monocular/CASE/openpose_kp`

## 4.9 Geometric Reconstruction

<!-- There are rather strage occurences when training the geometric reconstructor.   -->
If you have problems with NaN occuring in the orientation_fine Loss calculation, like when the raygenerator creates NaN in data, then the dataset was not good.

If the reconstructed Mesh after ~10000 Iterations is not looking anything similar like the person you are reconstructing, then the 