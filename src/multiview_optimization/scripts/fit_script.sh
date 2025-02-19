#!/bin/bash

cud=$1 # set cuda device
imp_path=$2 # set path to data folder
exp_path=$3 # set output path
#openpose_path=$4 # set path to the openpose keypoints

# Corrected the syntax for checking the directory or symlink
if [[ -d "$imp_path/openpose_kp" || -L "$imp_path/openpose_kp" ]]; then
    openpose_path="$imp_path/openpose_kp"  # Removed spaces around '='
    echo 'openpose_kp/ found'
else
    openpose_path="None"  # Removed spaces around '='
    echo 'openpose_kp/ not found'
fi

echo "using CUDA Device $cud"
echo "data path: $imp_path"
echo "outputting to: $exp_path"

save_path_1=$exp_path/bs1
save_path_5=$exp_path/bs5
save_path_20=$exp_path/bs20

batch_1_opt_param=$save_path_1/opt_params
batch_5_opt_param=$save_path_5/opt_params

echo 'starting bs 1 ...'

CUDA_VISIBLE_DEVICES=$cud python fit_wo_fitted_cameras.py --data_path $imp_path --batch_size 1 --save_path $save_path_1 --openpose_kp_path $openpose_path

echo 'starting bs 5 ...'

CUDA_VISIBLE_DEVICES=$cud python fit_wo_fitted_cameras.py --data_path $imp_path --batch_size 5 --save_path $save_path_5 --openpose_kp_path $openpose_path --checkpoint_path $batch_1_opt_param

echo 'starting bs 20 ... '

CUDA_VISIBLE_DEVICES=$cud python fit_wo_fitted_cameras.py --data_path $imp_path --batch_size 20 --train_shape True --save_path $save_path_20 --openpose_kp_path $openpose_path --checkpoint_path $batch_5_opt_param

echo "head_prior.obj is in $save_path_20/mesh/ with the highest number" 