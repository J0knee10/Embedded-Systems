# Q2: A system in action - Canny edge detection
# install opencv-python to import cv2:  pip3 install --upgrade opencv-python
#
# The edge detector is the "system": image in -> edge map out.
# Internally Canny convolves the image with Sobel kernels (2-D convolution),
# which is exactly the operation we study in 1-D for the rest of this lab.

import cv2
import matplotlib.pyplot as plt


def simple_edge_detection(image, title=''):
    edges_detected = cv2.Canny(image, 100, 200)

    images = [image, edges_detected]
    names = ['input x[m,n]', 'output y[m,n] (edges)']
    plt.figure(figsize=(10, 4))
    for loc, edge_image, name in zip([121, 122], images, names):
        plt.subplot(loc)
        plt.imshow(edge_image, cmap='gray')
        plt.title(name)
        plt.axis('off')
    plt.suptitle(title)
    plt.tight_layout()
    return edges_detected


# Run the same system on two different inputs
for fname in ['edgeflower.jpg', 'testimage.jpg']:
    img = cv2.imread(fname, 0)          # 0 = read as greyscale
    if img is None:
        print('Could not read', fname)
        continue
    simple_edge_detection(img, title='Canny edge detection on ' + fname)

# cv2.imwrite('edge_detected.png', edges_detected)
plt.show()
