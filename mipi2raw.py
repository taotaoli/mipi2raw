import os
import numpy as np
import argparse


def convertMipi2Raw(mipiFile, imgWidth, imgHeight, bitDeepth):
    mipiData = np.fromfile(mipiFile, dtype='uint8')
    print("mipiraw file size:", mipiData.size)

    bayerData = np.zeros([imgHeight * imgWidth], dtype='uint16')

    if bitDeepth == 8 or bitDeepth == 16:
        print("raw8 and raw16 no need to unpack")
        return
    elif bitDeepth == 10:
        # raw10
        imgWidth = imgWidth * 10 // 8
        byte_index = 0
        pixel_index = 0
        for byte_index in range(0, (imgHeight * imgWidth - 5), 5):
            bayerData[pixel_index + 0] = ((mipiData[byte_index + 0] * 4) & 0x03FC) + ((
                mipiData[byte_index + 4] // 1) & 0x0003)
            bayerData[pixel_index + 1] = ((mipiData[byte_index + 1] * 4) & 0x03FC) + (
                (mipiData[byte_index + 4] // 4) & 0x0003)
            bayerData[pixel_index + 2] = ((mipiData[byte_index + 2] * 4) & 0x03FC) + (
                (mipiData[byte_index + 4] // 16) & 0x0003)
            bayerData[pixel_index + 3] = ((mipiData[byte_index + 3] * 4) & 0x03FC) + (
                (mipiData[byte_index + 4] // 64) & 0x0003)
            pixel_index = pixel_index + 4
    elif bitDeepth == 12:
        # raw12
        imgWidth = imgWidth * 12 // 8
        byte_index = 0
        pixel_index = 0
        for byte_index in range(0, (imgHeight * imgWidth - 3), 3):
            bayerData[pixel_index + 0] = ((mipiData[byte_index + 0] * 16) & 0x0FF0) + ((
                mipiData[byte_index + 2] // 1) & 0x000F)
            bayerData[pixel_index + 1] = ((mipiData[byte_index + 1] * 16) & 0x0FF0) + (
                (mipiData[byte_index + 2] // 16) & 0x000F)
            pixel_index = pixel_index + 2
    elif bitDeepth == 14:
        # raw14
        imgWidth = imgWidth * 14 // 8
        byte_index = 0
        pixel_index = 0
        for byte_index in range(0, (imgHeight * imgWidth - 7), 7):
            bayerData[pixel_index + 0] = ((mipiData[byte_index + 0] * 64) & 0x03F0) + (
                (mipiData[byte_index + 4] // 1) & 0x003F)
            bayerData[pixel_index + 1] = ((mipiData[byte_index + 1] * 64) & 0x03F0) + (
                (mipiData[byte_index + 4] // 64) & 0x0003) + ((mipiData[byte_index + 5] // 1) & 0x000F)
            bayerData[pixel_index + 2] = ((mipiData[byte_index + 2] * 64) & 0x03F0) + (
                (mipiData[byte_index + 5] // 16) & 0x000F) + ((mipiData[byte_index + 6] // 1) & 0x0003)
            bayerData[pixel_index + 3] = ((mipiData[byte_index + 3] * 64) & 0x03F0) + (
                (mipiData[byte_index + 6] // 4) & 0x003F)

            pixel_index = pixel_index + 4
    else:
        print("unsupport bayer bitDeepth:", bitDeepth)

    bayerData.tofile(mipiFile[:-4]+'_unpack.raw')


def ProcSingleFile(rawFile, img_width, img_height, rawDepth):
    # (path, rawFile) = os.path.split(raw_name)
    print("process ", rawFile, "...")
    convertMipi2Raw(rawFile, img_width, img_height, rawDepth)


def ProcPath(path, img_width, img_height, rawDepth):
    file_list = os.listdir(path)
    for f in file_list:
        f_lower = f.lower()
        if f_lower.endswith('.raw'):
            raw_name = '%s\%s' % (path, f)
            ProcSingleFile(raw_name, img_width, img_height, rawDepth)


if "__main__" == __name__:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path", help="input raw path", required=False, type=str)
    parser.add_argument(
        "--file", help="input raw file name", required=False, type=str)
    parser.add_argument("--width", help="raw image width",
                        required=True, type=int)
    parser.add_argument("--height", help="raw image height",
                        required=True, type=int)
    parser.add_argument(
        "--depth", help="raw image depth [8, 10, 12, 14, 16]", required=True, type=int)

    args = parser.parse_args()

    rawPath = args.path
    rawFile = args.file
    img_width = args.width
    img_height = args.height
    rawDepth = args.depth

    if rawPath is not None:
        ProcPath(rawPath, img_width, img_height, rawDepth)
    elif rawFile is not None:
        ProcSingleFile(rawFile, img_width, img_height, rawDepth)
    else:
        print("parameters wrong!!! no path or file")
