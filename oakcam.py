#!/usr/bin/env python3

import depthai as dai
import time
import argparse

enable_4k = True  # Will downscale 4K -> 1080p

parser = argparse.ArgumentParser()
parser.add_argument('-fb', '--flash-bootloader',
                    default=False, action="store_true")
parser.add_argument('-f',  '--flash-app',
                    default=False, action="store_true")
args = parser.parse_args()


def getPipeline():
    # Start defining a pipeline
    pipeline = dai.Pipeline()

    # Define a source - color camera
    cam_rgb = pipeline.createColorCamera()
    cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    cam_rgb.setInterleaved(False)
    cam_rgb.initialControl.setManualFocus(65)
    # cam_rgb.initialControl.AutoFocusMode(2)
    cam_rgb.initialControl.AutoWhiteBalanceMode(0)

    if enable_4k:
        cam_rgb.setResolution(
            dai.ColorCameraProperties.SensorResolution.THE_4_K)
        cam_rgb.setIspScale(1, 2)
    else:
        cam_rgb.setResolution(
            dai.ColorCameraProperties.SensorResolution.THE_1080_P)

    # Create an UVC (USB Video Class) output node. It needs 1920x1080, NV12 input
    uvc = pipeline.createUVC()
    cam_rgb.video.link(uvc.input)

    return pipeline


# Pipeline defined, now the device is connected to
with dai.Device(getPipeline()) as device:
    print("\nDevice started, please keep this process running")
    print("and open an UVC viewer. Example on Linux:")
    print("    guvcview -d /dev/video0")
    print("\nTo close: Ctrl+C")

    # Doing nothing here, just keeping the host feeding the watchdog
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
