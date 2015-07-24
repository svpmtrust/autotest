
# Make sure the png requirement is satisfied by running
# pip install pypng

import png

def read_image_file(file_name):
    """
    Read a file and return the Image as a two dimensional bitmap

    :param file_name: Name of the file to read
    :return:
        Your image will be returned as arrays of rows.  Each row will
        have one number for grayscale images and 3 numbers for RGB Images.
    """

    with open(file_name) as fp:
        image = png.Reader(fp).read()[2]
        return [a for a in image]
