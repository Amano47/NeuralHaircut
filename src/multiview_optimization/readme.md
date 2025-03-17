## 1. PIXIE / SMPLX

Download pre-trained models and data from [SMPLX](https://smpl-x.is.tue.mpg.de/)  and [PIXIE](https://pixie.is.tue.mpg.de/) projects.

For more information please follow [PIXIE installation](https://github.com/yfeng95/PIXIE/blob/master/Doc/docs/getting_started.md).

For multiview optimization you need to have the following files ```SMPL-X__FLAME_vertex_ids.npy, smplx_extra_joints.yaml, SMPLX_NEUTRAL_2020.npz``` and change a path to them in ```./utils/config.py```

### PIXIE initialization

Note, that you need to obtain  [PIXIE initialization](https://github.com/yfeng95/PIXIE) for shape, pose parameters and save it as a dict in ```initialization_pixie``` file (see the structure in [example scene](../../example) for convenience). 

**Note**
Further details on how to get the file: see [the other guide](/custom_dataset/custom_data.md#32-pixie-initialization_pixie)  

## 2. OpenPose Keypoints

Furthermore, use [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) to obtain 3d keypoints or use only [FaceAlignment](https://github.com/1adrianb/face-alignment) loss in optimization process.

[see more](/custom_dataset/troubleshoot.md#47-openpose) about possible Issues with OpenPose.  

On Windows, run OpenPose with:  
```bash
.\bin\OpenPoseDemo.exe --render_pose 0 --display 0 --hand --face --image_dir .\path\to\image\dir --write_json .\CASE\openpose_kp
```

## 3. FLAME fitting

**Modified:**

To fit the FLAME prior Head, run the following:  
```bash
cd src/multiview_optimization

bash scripts/fit_script.sh <GPU ID> ../../implicit-hair-data/data/SCENE_TYPE/CASE ./experiments/CASE
```
- the second argument is the path to the prepared data  
- the third argument is the output path


**Original:**

To obtain FLAME prior run:

```bash
bash run_monocular_fitting.sh
```
To visualize the training process:

```bash
tensorboard --logdir ./experiments/EXP_NAME
```

After training put obtained FLAME prior mesh.obj into the dataset folder ```./implicit-hair-data/data/SCENE_TYPE/CASE/head_prior.obj```.

---
### Go back to /preprpocess_custom_data

[Go back and finish the preprocess](/custom_dataset/custom_data.md#39-flame-head)