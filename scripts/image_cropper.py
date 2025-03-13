import os
from PIL import Image
import argparse
from tqdm import tqdm

def crop_to_square(image_path, output_path):
    """Crop the image to a square and resize it to 2160x2160."""
    with Image.open(image_path) as img:
        width, height = img.size
        
        # Calculate the new dimensions for cropping
        new_size = min(width, height)
        left = (width - new_size) // 2
        right = left + new_size
        top = 0
        bottom = height
        
        # Crop the image
        img_cropped = img.crop((left, top, right, bottom))
        
        # Resize to 2160x2160
        img_resized = img_cropped.resize((2160, 2160), Image.ANTIALIAS)
        
        # Save the processed image
        img_resized.save(output_path)

def process_directory(input_dir, output_dir):
    """Process all images in the input directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in tqdm(os.listdir(input_dir)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            crop_to_square(input_path, output_path)
            # print(f"Processed: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crop images to square and resize to 2160x2160.")
    parser.add_argument("--input", required=True, help="Directory containing images to process.")
    parser.add_argument("--output", help="Directory to save processed images. If not provided, will create in current directory.")

    args = parser.parse_args()

    # Set output directory to current directory if not provided
    output_dir = args.output if args.output else os.path.join(os.getcwd(), "processed_images")

    process_directory(args.input, output_dir)
