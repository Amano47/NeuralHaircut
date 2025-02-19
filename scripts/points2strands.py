import open3d as o3d
import numpy as np
import argparse
import os

def load_ply(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    return points, colors

def create_strands(points, colors, threshold=0.05, color_tolerance=0.1):
    strands = []
    color_groups = {}
    
    for i, color in enumerate(colors):
        color_key = tuple((color / color_tolerance).astype(int))  # Group by similar colors with finer granularity
        if color_key not in color_groups:
            color_groups[color_key] = []
        color_groups[color_key].append(i)
    
    for indices in color_groups.values():
        if len(indices) < 2:
            continue
        
        strand_lines = []
        sorted_indices = sorted(indices, key=lambda i: points[i, 2])  # Sort by Z (or another axis)
        
        for j in range(len(sorted_indices) - 1):
            idx1, idx2 = sorted_indices[j], sorted_indices[j + 1]
            if np.linalg.norm(points[idx1] - points[idx2]) < threshold:
                strand_lines.append([idx1, idx2])
        
        if strand_lines:
            strands.append(strand_lines)
    
    return strands

def save_lineset(output_path, points, strands):
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    lines = [line for strand in strands for line in strand]
    line_set.lines = o3d.utility.Vector2iVector(lines)
    o3d.io.write_line_set(output_path, line_set)

def main():
    parser = argparse.ArgumentParser(description="Convert PLY points to LineSet strands.")
    parser.add_argument("--input", required=True, help="Path to input PLY file.")
    parser.add_argument("--output", required=True, help="Path to output directory.")
    args = parser.parse_args()
    
    points, colors = load_ply(args.input)
    strands = create_strands(points, colors)
    
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, "strands.ply")
    save_lineset(output_file, points, strands)
    print(f"Saved strands to {output_file}")
    
if __name__ == "__main__":
    main()
