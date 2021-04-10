import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread('img/parrots.jpg')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

square_width = 10
square_height = 25

width = img.shape[1]
height = img.shape[0]

while (width % square_width !=0):
    width -=1

while (height % square_height !=0):
    height -=1


tiles_x = int(width/square_width)
tiles_y = int(height/square_height)

img2 = np.zeros((tiles_y,tiles_x,3), dtype="uint8")
img3 = np.zeros((tiles_y,tiles_x,3), dtype="uint8")

img = cv2.resize(img, dsize=(width, height))


for x in range(tiles_x):
    for y in range(tiles_y):
        sumR = 0
        sumG = 0
        sumB = 0
        reds = [0]*256
        greens = [0]*256
        blues = [0]*256
        for xx in range(square_width):
            for yy in range(square_height):
                col = img[y*square_height + yy][x*square_width + xx]
                r = col[0]
                g = col[1]
                b = col[2]

                reds[r] += 1
                greens[g] += 1
                blues[b] += 1

                sumR += r
                sumG += g
                sumB += b
        sumR /= (square_width*square_height)
        sumG /= (square_width*square_height)
        sumB /= (square_width*square_height)
        # below: unoptimised
        # for xx in range(square_width):
        #     for yy in range(square_height):
        #
        #         img2[y*square_height + yy][x*square_width + xx] =  np.array([sumR,sumG,sumB])
        #

        # img2[y*square_height:(y+1)*square_height][x*square_width:(x+1)*square_width] = np.array([sumR,sumG,sumB])

        # optimised
        img2[y][x] = np.array([sumR,sumG,sumB])
        img3[y][x] = np.array([np.argmax(reds), np.argmax(greens), np.argmax(blues)])

img2 = cv2.resize(img2, dsize=(width, height), interpolation=cv2.INTER_NEAREST)
img3 = cv2.resize(img3, dsize=(width, height), interpolation=cv2.INTER_NEAREST)

for x in range(tiles_x):
    for y in range(tiles_y):

        for xx in range(square_width):
            for yy in range(square_height):
                if(xx < yy):
                    img[y*square_height + yy][x*square_width + xx] = img2[y*square_height + yy][x*square_width + xx]
                else:
                    img[y*square_height + yy][x*square_width + xx] = img3[y*square_height + yy][x*square_width + xx]

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.subplot(1, 2, 2)
plt.imshow(img3)
plt.show()
