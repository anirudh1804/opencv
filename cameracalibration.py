import cv2
import numpy as np
import glob
import os
import argparse

# Define the chessboard size
chessboard_size = (7, 7)

# Prepare object points
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# Arrays to store object points and image points
objpoints = []
imgpoints = []


def parse_args():
    parser = argparse.ArgumentParser(description="Camera Calibration")
    parser.add_argument("--input_path", type=str, help="Path to the input images or videos")
    return parser.parse_args()


def calibrate_camera(images, frame_size):
    global objpoints, imgpoints

    for image_file in images:
        img = cv2.imread(image_file)
        if img is None:
            print(f"Failed to load image: {image_file}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Draw the corners
            cv2.drawChessboardCorners(img, chessboard_size, corners, ret)

            # Save output images
            output_image_path = os.path.join('output_images', os.path.basename(image_file))
            cv2.imwrite(output_image_path, img)
            print(f"Saved image with corners detected: {output_image_path}")
        else:
            print(f"No chessboard corners found in image: {image_file}")

    # Calibration
    if len(objpoints) > 0 and len(imgpoints) > 0:
        ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame_size, None,None)

        # Print camera intrinsic parameters
        print("Camera intrinsic parameters:")
        print("Focal Lengths (fx, fy):", camera_matrix[0, 0], ",", camera_matrix[1, 1])
        print("Principal Point Coordinates (cx, cy):", camera_matrix[0, 2], ",", camera_matrix[1, 2])
    else:
        print("No valid object points or image points were collected for calibration.")


def main():
    args = parse_args()
    input_path = args.input_path

    if not input_path:
        print("Error: Please provide a valid input path using the --input_path argument.")
        return

    # Check if the input path is a directory
    if os.path.isdir(input_path):
        # Load images or videos from the directory
        image_files = glob.glob(os.path.join(input_path, '*.jpg'))
        video_files = glob.glob(os.path.join(input_path, '*.mov'))

        # Create output directories
        os.makedirs('output_images', exist_ok=True)
        os.makedirs('output_videos', exist_ok=True)

        # Process images
        if image_files:
            frame_size = cv2.imread(image_files[0]).shape[:2][::-1]
            calibrate_camera(image_files, frame_size)
        else:
            print("No images found in the specified directory.")

        # Process videos
        if not video_files:
            print("No video files found in the specified directory.")
        else:
            for idx, video_file in enumerate(video_files, start=1):
                print(f"Processing video file {idx}: {video_file}")
                cap = cv2.VideoCapture(video_file)
                if not cap.isOpened():
                    print(f"Failed to open video file: {video_file}")
                    continue

                frame_count = 0
                frames_to_skip = 5  # Process every 5th frame
                frames_collected = 0
                max_frames = 240  # Maximum number of frames to collect
                output_frames_folder = f'output_frames_{idx}'
                os.makedirs(output_frames_folder, exist_ok=True)

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_count += 1
                    if frame_count % frames_to_skip != 0:
                        continue

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame_size = gray.shape[::-1]  # Update frame size for each frame

                    # Find the chessboard corners
                    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

                    if ret:
                        objpoints.append(objp)
                        imgpoints.append(corners)
                        frames_collected += 1

                        # Draw the corners
                        cv2.drawChessboardCorners(frame, chessboard_size, corners, ret)
                        output_frame_path = os.path.join(output_frames_folder, f"frame_{frame_count}.jpg")
                        cv2.imwrite(output_frame_path, frame)
                        print(f"Saved frame with corners detected: {output_frame_path}")

                        # Stop if we have collected enough frames
                        if frames_collected >= max_frames:
                            break

                cap.release()
    else:
        print(f"Invalid input path: {input_path}. Please provide a valid directory path.")


if __name__ == "__main__":
    main()
