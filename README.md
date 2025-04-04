# flaty

_Flaty_ is a simple python project for camera calibration and undistortion feature with openCV.

This python project is based on following features:
1. Calibration for camera using checkerboard.
2. Undistortion of images using camera calibration parameters.
3. Save the combined video of the original video and undistorted video.

## How to Use
1. Press space bar to start capturing image and press enter to collect image calibration data.
2. If you get enough images, the calibration result will be printed on the console log.
3. The undistorted video based on the calibration data will be automatically start.
4. If you press 'tab' key, you can switch the original video and undistorted video.
5. The combined video will be saved in the same directory as the original video with the name `output.mp4`.

## Example video environment
* 640 * 480 size, 480p video
## Camera Calibration Results
* The number of selected images = 22
* RMS error = 0.550642513685792
* Camera matrix (K) =
  [[724.13987448   0.         324.15867987]
  [  0.         725.51617063 239.72117183]
  [  0.           0.           1.        ]]
* Distortion coefficient (k1, k2, p1, p2, k3, ...) = [ 6.39599067e-02 -9.26211648e-02 -7.35625842e-03  2.65885963e-04
  4.65346995e+00]
## Undistorted video demo
[![Video Title](https://img.youtube.com/vi/W18AUvPAjh4/0.jpg)](https://www.youtube.com/watch?v=W18AUvPAjh4)