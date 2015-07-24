
# Make sure the png requirement is satisfied by running
# pip install pypng

import png

def read_image_file(file_name):
    with open(file_name) as fp:
        image = png.Reader(fp).read()[2]
        return [a for a in image]
