import numpy as np
import cv2 as cv

def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10, wnd_name='Camera Calibration'):
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened()

    # Select images
    img_select = []
    while True:
        # Grab an images from the video
        valid, img = video.read()
        if not valid:
            break

        if select_all:
            img_select.append(img)
        else:
            # Show the image
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)}', (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
            cv.imshow(wnd_name, display)

            # Process the key event
            key = cv.waitKey(wait_msec)
            if key == ord(' '):             # Space: Pause and show corners
                complete, pts = cv.findChessboardCorners(img, board_pattern)
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img) # Enter: Select the image
            if key == 27:                  # ESC: Exit (Complete image selection)
                break

    cv.destroyAllWindows()
    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    # Find 2D corner points from given images
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0

    # Prepare 3D points of the chess board
    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points) # Must be `np.float32`

    # Calibrate the camera
    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)

def distortion_correction(video_file, K, dist_coeff, output_file='output.mp4'):
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened(), 'Cannot read the given input, ' + video_file

    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH)) * 2
    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv.CAP_PROP_FPS)

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    # Run distortion correction
    show_rectify = True
    map1, map2 = None, None
    while True:
        # Read an image from the video
        valid, img = video.read()
        if not valid:
            break

        original = img.copy()

        # Rectify geometric distortion (Alternative: `cv.undistort()`)
        info = "Original"
        if show_rectify:
            if map1 is None or map2 is None:
                map1, map2 = cv.initUndistortRectifyMap(K, dist_coeff, None, None, (img.shape[1], img.shape[0]), cv.CV_32FC1)
            img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
            info = "Rectified"
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

        # Combine the original video and undistorted video
        combined_frame = np.hstack((original, img))

        # Write the combined frame to the output video
        out.write(combined_frame)

        # Show the image and process the key event
        cv.imshow("Geometric Distortion Correction", img)
        key = cv.waitKey(10)
        if key == ord(' '):     # Space: Pause
            key = cv.waitKey()
        if key == 27:           # ESC: Exit
            break
        elif key == ord('\t'):  # Tab: Toggle the mode
            show_rectify = not show_rectify

    video.release()
    out.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    video_file = './data/20250404_164425.mp4 '
    board_pattern = (10, 7)
    board_cellsize = 0.025

    img_select = select_img_from_video(video_file, board_pattern)
    assert len(img_select) > 0, 'There is no selected images!'
    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(img_select, board_pattern, board_cellsize)

    # Print calibration results
    print('## Camera Calibration Results')
    print(f'* The number of selected images = {len(img_select)}')
    print(f'* RMS error = {rms}')
    print(f'* Camera matrix (K) = \n{K}')
    print(f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff.flatten()}')

    distortion_correction(video_file, K, dist_coeff)