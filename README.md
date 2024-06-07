# OpenCV projects
Welcome to my OpenCV projects repository! This repository contains a collection of computer vision projects implemented using OpenCV. 

1. Camera Calibration
Camera calibration is a crucial step in computer vision to obtain accurate measurements and rectify images. This project demonstrates how to use OpenCV for camera calibration, including:
  Checkerboard Pattern Detection: Using a checkerboard pattern to capture multiple images from different angles.
  Intrinsic and Extrinsic Parameters: Calculating the intrinsic (camera matrix) and extrinsic parameters (rotation and translation vectors) of the camera.
  Distortion Coefficients: Estimating distortion coefficients to correct lens distortion.
  Undistortion of Images: Applying the calibration results to undistort images and improve accuracy in further processing tasks.

2. Head Pose Estimation
Head pose estimation is the process of determining the orientation of a person's head in an image or video. This project demonstrates how to use OpenCV and MediaPipe for head pose estimation, including:
  Face Detection: Detecting facial landmarks using MediaPipe's Face Mesh solution.
  3D Pose Estimation: Estimating the 3D position and orientation of the head using Perspective-n-Point (PnP) algorithms.
  Real-Time Processing: Implementing real-time head pose estimation using a webcam feed.
  Visual Feedback: Displaying visual feedback on the head pose orientation (e.g., lines indicating the direction the head is facing).
