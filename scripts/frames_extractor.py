import cv2
import os
import argparse

def is_blurry(image, threshold=100.0):
    """Check if the image is blurry using the variance of the Laplacian."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < threshold

def extract_frames(input, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the video file
    cap = cv2.VideoCapture(input)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate the interval for frame extraction
    interval = total_frames // 256  # Space frames as evenly as possible
    extracted_frames = 0

    while cap.isOpened() and extracted_frames < 256:
        frame_index = extracted_frames * interval
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()

        if not ret:
            break
        
        # Check if the frame is blurry
        if not is_blurry(frame):
            # Save the frame as an image file
            frame_filename = os.path.join(output_dir, f"frame_{extracted_frames:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_frames += 1

        # Save the frame as an image file
        frame_filename = os.path.join(output_dir, f"frame_{extracted_frames:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        extracted_frames += 1

    cap.release()
    print(f"Extracted {extracted_frames} frames to '{output_dir}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video file.")
    parser.add_argument("--input", help="Path to the input MP4 video file.")
    parser.add_argument("--output_dir", help="Directory to save extracted frames. If not provided, will create in current directory.")

    args = parser.parse_args()

    # Set output directory to current directory if not provided
    output_dir = args.output_dir if args.output_dir else os.path.join(os.getcwd(), os.path.splitext(os.path.basename(args.input))[0])

    extract_frames(args.input, output_dir)
