import cv2
import os
import argparse
import shutil
import zipfile

#########################################################
# This is a cheap 'copy' of @marcelk04 magic            #
# Read more here:                                       #
# https://github.com/marcelk04/E-D3DGS/tree/main/vci    #
#########################################################

# execute command
def exec_cmd(cmd: str) -> None:
    print(f"Executing '{cmd}'")
    
    exit_code = os.system(cmd)
    
    if exit_code != 0:
        exit(exit_code)
        
    print()


def main(args):
    
    # If --redo is set, zip up the colmap directory and remove its contents
    #if args.redo and os.path.exists(colmap_dir):
    #    zip_path = os.path.join(args.scene, "colmap_backup.zip")
    #    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    #        for root, dirs, files in os.walk(colmap_dir):
    #            for file in files:
    #                file_path = os.path.join(root, file)
    #                zipf.write(file_path, os.path.relpath(file_path, colmap_dir))
    #    shutil.rmtree(colmap_dir)
    
    
    colmap_dir = os.path.join(args.scene, "colmap")
    sparse_dir = os.path.join(colmap_dir, "sparse")
    dense_dir = os.path.join(colmap_dir, "dense")
    db_path = args.db_path if args.db_path else os.path.join(colmap_dir, "database.db")

    # Determine default paths for image and mask directories if not set
    image_dir = args.image if args.image else os.path.join(args.scene, "image")
    mask_dir = args.mask if args.mask else os.path.join(args.scene, "mask")

    # Create directories if they do not exist
    os.makedirs(colmap_dir, exist_ok=True)
    os.makedirs(sparse_dir, exist_ok=True)
    os.makedirs(dense_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(mask_dir, exist_ok=True)
    
    # Create an empty database file if it does not exist
    if not os.path.exists(db_path):
        open(db_path, 'a').close()
    
    print(f"Created COLMAP structure at {colmap_dir}")
    print(f"Database path: {db_path}")
    print(f"Image directory: {image_dir}")
    print(f"Mask directory: {mask_dir}")


    ###
    
    print('Starting COLMAP ....')
    print()
    
    # feature extractor
    feature_ext = f"colmap feature_extractor\
        --database_path {db_path}\
        --image_path {image_dir}\
        --ImageReader.camera_model PINHOLE\
        --ImageReader.single_camera_per_image true"
        
    if args.rm_bg:
        feature_ext += f" --ImageReader.mask_path {mask_dir}"
    
    exec_cmd(feature_ext)
    
    # exhaustive matcher
    exh_matcher = f'colmap exhaustive_matcher\
        --database_path {db_path}'
        
    exec_cmd(exh_matcher)
    
    # mapper
    mapper = f"colmap mapper \
		--database_path {db_path} \
		--image_path {image_dir} \
		--output_path {sparse_dir} \
		--Mapper.ba_global_function_tolerance 0.000001 \
		--Mapper.multiple_models false"
  
    exec_cmd(mapper)
 
    # image undistortion
    image_undistortion = f"colmap image_undistorter \
		--image_path {image_dir} \
		--input_path {os.path.join(sparse_dir, '0')} \
		--output_path {dense_dir} \
		--output_type COLMAP"
  
    exec_cmd(image_undistortion)
 
    # skip dense if --dense= False
    if args.dense == True:
    
        fused_ply_path = os.path.join(dense_dir, 'fused.ply')
        # Create an empty file if it does not exist
        if not os.path.exists(fused_ply_path):
            open(fused_ply_path, 'a').close()

    
        # PatchMatch Stereo, needs CUDA
        patch_match_stereo = f"colmap patch_match_stereo \
			--workspace_path {dense_dir} \
			--workspace_format COLMAP \
			--PatchMatchStereo.geom_consistency true"
   
        exec_cmd(patch_match_stereo)

        # stereo fusion, also needs CUDA
        stereo_fusion = f"colmap stereo_fusion \
			--workspace_path {dense_dir} \
			--workspace_format COLMAP \
			--input_type geometric \
			--output_path {fused_ply_path} \
			--output_type PLY"
   
        # if masks are used
        if args.rm_bg:
            stereo_fusion += f" --StereoFusion.mask_path {mask_dir}"
   
        exec_cmd(stereo_fusion)

    print('COLMAP finished reconstructing automaticaly without automatic_reconstructor')
    
    # use model_converter to get sparse/0/* as txt files and save them in colmap/sparse_txt/
    if args.txt:
        sparse_txt_dir = os.path.join(colmap_dir, 'sparse_txt')
        os.makedirs(sparse_txt_dir, exist_ok=True)
        
        mod_con = f"colmap model_converter\
            --input_path {sparse_dir}\
            --output_path {sparse_txt_dir}\
            --output_type TXT"
        
        exec_cmd(mod_con)
        
        print('sparse/0/ converted and saved in sparse_txt/')
        print()
        
    print('Finished !')
        
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scene', type=str, help='Path to ./implicit-hair-data/data/SCENE_TYPE/CASE/')
    parser.add_argument('--txt', type=bool, default=True, help='Export model as txt along binaries')
    parser.add_argument('--gpu', type=int, default=-1, help='The Index of your GPU to use')
    parser.add_argument('--dense', type=bool, default=True, help='skip dense if not needed')
    parser.add_argument('--db_path', type=str, default=None,help='path to database if there is one. Else, a new db is created')
    parser.add_argument('--mask', type=str, default=None, help='path to masks dir; assumes you have masks in your scene dir')
    parser.add_argument('--image', type=str, default=None, help='path to images dir')
    parser.add_argument('--rm_bg', type=bool, default=True, help='remove the background by masking it, for --mask; if False, no masks are applied')
    
    # parser.add_argument('--redo', type=bool, default=False, help='to re-callmap, set it to True. Deletes all contents in colmap/')
    
    args = parser.parse_args()
    
    main(args)
    
# How the folder Structure looks
#
#   |--implicit-hair-data
#       |--data
#           |--SCENE_TYPE
#               |--CASE
#                   |--image/
#                   |--mask/
#                   |--colmap/ <----- new
#                       |--sparse/ <- new
#                       |--dense/  <- new
#                       |--database.db <- new
#                   |--hair_mask/
