# _*_ coding: utf-8 _*_
# !/usr/bin/env python3

"""
Quick and dirty image format converter.
Converts images within a source directory to a specified target
format using the Python Image Library.

Created on: 28/02/2020

Requirements:

Python 3.5 or higher
Pillow==7.0.0

Run command:
    pip3 install Pillow
to install the Python Image Library.

Default source directory: ./to_be_converted/
Default target image file extension: .png
Default target directory: .converted/<time_stamp>/

Command line usage example (on Mac):
    python3 image_converter.py /Users/$USER/Desktop/ .tiff
"""


import sys
import time
from pathlib import Path
from PIL import Image
from os import listdir
from os.path import splitext


class ImageConverter:
    """
    Converts one image format into another using the Python Image Library.
    Default conversion to .png unless overridden at the command line.
    """
    def __init__(self, src_dir='./to_be_converted/', target_ext='.png',
                 target_dir='./converted/'):
        """
        Set the source directory, file extension and create target directory if it doesn't exist.
        :param src_dir: str
        :param target_ext: str
        :param target_dir: str
        """
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.source_directory = src_dir
        self.target_file_extension = target_ext
        self.target_directory = target_dir
        Path(self.target_directory + self.timestr).mkdir(parents=True, exist_ok=True)

    def cycle_through_files_and_convert(self) -> list:
        """
        Get list of the files in the source directory and send them to the _convert_image function.
        :return: list
        """
        list_of_converted_images = []
        for file in listdir(self.source_directory):
            filename, extension = splitext(file)
            list_of_converted_images.append(self._convert_image(filename, extension))
        return list_of_converted_images

    def _convert_image(self, filename: str, extension: str) -> None:
        """
        Open the image and save it to the target directory in the desired format.
        :param filename: str
        :param extension: str
        :return: None
        """
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            im = Image.open(self.source_directory + filename + extension)
            im.save(self.target_directory + self.timestr + '/' + filename +
                    self.target_file_extension)
            print('{} converted successfully'.format(self.target_directory + self.timestr +
                                                     '/' + filename + self.target_file_extension))


def main():
    """
    Ascertain whether the script has been run with command line parameters and populate the
    ImageConverter class accordingly.
    """

    print('\n The default target format for this script to convert to is .png. \n'
          'if you require a different target format, please run the script with the \n'
          'following command line parameters: \n \n'
          'python3 <source_directory> <desired_image_file_type> \n')

    if len(sys.argv) > 1:
        source_directory = sys.argv[1]
        target_file_ext = sys.argv[2]
        image_converter = ImageConverter(source_directory, target_file_ext)
        image_converter.cycle_through_files_and_convert()
    else:
        image_converter = ImageConverter()
        image_converter.cycle_through_files_and_convert()


if __name__ == '__main__':
    main()
