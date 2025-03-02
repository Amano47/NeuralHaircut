# Openpose and Face Alignment

In [multiview_optimization](../src/multiview_optimization/readme.md) is a step, which requires you to obtain face keypoints from [Openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) or rather the [face alginment](https://github.com/1adrianb/face-alignment) keypoints.  
If you have the testdata [implicit-hair-data/](https://drive.google.com/file/d/1CADXQfC2IgxmFLwcLrm4G3ilWpW1g_PA/view), then look into the Folder named `../implicit-hair-data/data/monocular/person_0/openpose_kp`. There you can see a json file for each image, which stores the keypoint coordinates in 2D and 3D for pose, face and hands (left & right).  

To get the files, go through these steps  
(if there are any issues with Openpose, there is a [FAQ](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/05_faq.md) with Troubleshooting guides):

### 1. Install OpenPose

[Official Guide](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md)  
[OpenPose FAQ](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/05_faq.md) (for Troubleshoot)  
[Alternative Model Caffeemodel Download](https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1602#issuecomment-641653411) (Model Download if the Server is down)

TL;DR: Windows is the easiest way to install OpenPose for quick use.

__But__: it should be enoguh to install [face-alignment](https://github.com/1adrianb/face-alignment) from 1adrianb in a conda environment, which is already done in the `neuralhaircut`conda environment, which should be done in [step 1](/custom_dataset/NeuralHaircut-TUG.md#1-installing) (more on face-alignment in [2 b)](#b-face-alginment).    

### 2. Run script

After you have installed either Openpose or face-alignment, run the commands below

#### a) OpenPose

```powershell
.\bin\OpenPoseDemo.exe --image_dir C:\path\to\images --write_json C:\path\to\output --display 0 --render_pose 0 --face --hand
```
This should return a json file, just like in the [/person_0/openpose_kp/](../implicit-hair-data/data/monocular/person_0/openpose_kp) folder.

#### b) face alginment

