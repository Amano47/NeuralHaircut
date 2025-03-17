from PIL import Image
import numpy as np
from skimage.filters import gabor_kernel
from scipy import ndimage as ndi
from skimage.filters import difference_of_gaussians
import math
import os
import tqdm
import cv2
import argparse

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


def generate_gabor_filters(sigma_x, sigma_y, freq, num_filters):
    thetas = np.linspace(0, math.pi * (num_filters - 1) / num_filters, num_filters)
    print(thetas / math.pi * 180)
    kernels = []
    for theta in thetas:
        kernel = np.real(gabor_kernel(freq, theta=math.pi - theta, sigma_x=sigma_x, sigma_y=sigma_y))
        kernels.append(kernel)
    return kernels


def calc_orients(img, kernels):
    gray_img = rgb2gray(img)
    filtered_image = difference_of_gaussians(gray_img, 0.4, 10)
    gabor_filtered_images = [ndi.convolve(filtered_image, kernels[i], mode='wrap') for i in range(len(kernels))]
    F_orients = np.abs(np.stack(gabor_filtered_images)) # abs because we only measure angle in [0, pi]
    return F_orients


def calc_confidences(F_orients, orientation_map, num_filters):
    orients_bins = np.linspace(0, math.pi * (num_filters - 1) / num_filters, num_filters)
    orients_bins = orients_bins[:, None, None]
    
    orientation_map = orientation_map[None]
    
    dists = np.minimum(np.abs(orientation_map - orients_bins), 
                       np.minimum(np.abs(orientation_map - orients_bins - math.pi),
                                  np.abs(orientation_map - orients_bins + math.pi)))
        
    F_orients_norm = F_orients / F_orients.sum(axis=0, keepdims=True)
    
    V_F = (dists**2 * F_orients_norm).sum(0)
    
    return V_F


def main(args):
    
    if args.input is None:
        print('IllegalArgumentException: No input data')
        return 0
    else:
        img_path = os.path.join(args.input, 'image')
        
    if args.output is None:
        print(f'Files are saved in Input dir: {args.input}')
        
        orient_dir = os.path.join(args.input, 'orientation_maps')
        conf_dir = os.path.join(args.input, 'confidence_maps')
    else:
        print(f'Files are saved in {args.output}orientation_maps and /confidence_maps')
        
        orient_dir = os.path.join(args.output, 'orientation_maps')
        conf_dir = os.path.join(args.output, 'confidence_maps')

    os.makedirs(orient_dir, exist_ok=True)
    os.makedirs(conf_dir, exist_ok=True)
    
    print(f'Images located in {img_path}')

    
    num_filters = args.num_filters
    
    kernels = generate_gabor_filters(args.sigma_x, args.sigma_y, args.freq, args.num_filters)
    
    img_list = sorted(os.listdir(img_path))
    
    for img_name in tqdm.tqdm(img_list):
        basename = img_name.split('.')[0]
        img = np.array(Image.open(os.path.join(img_path, img_name)))
        F_orients = calc_orients(img, kernels)
        orientation_map = F_orients.argmax(0)
        orientation_map_rad = orientation_map.astype('float16') / num_filters * math.pi
        confidence_map = calc_confidences(F_orients, orientation_map_rad, num_filters)

        cv2.imwrite(f'{orient_dir}/{basename}.png', orientation_map.astype('uint8'))
        np.save(f'{conf_dir}/{basename}.npy', confidence_map.astype('float16'))


        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(conflict_handler='resolve')

    parser.add_argument('--input', type=str, default=None, help='dir, where your images are. The calculated maps are saved in a subdir')
    parser.add_argument('--output', type=str, default=None, help='Output directory, where stuff gets saved. If no output dir is set, it gets saved in the input folder' )
    
    parser.add_argument('--sigma_x', default=1.8, type=float)
    parser.add_argument('--sigma_y', default=2.4, type=float)
    parser.add_argument('--freq', default=0.23, type=float)
    parser.add_argument('--num_filters', default=180, type=int)

    args, _ = parser.parse_known_args()
    args = parser.parse_args()
    
    # print(f'DEBUG: orient_dir, conf_dir: {args.output}')

    main(args)