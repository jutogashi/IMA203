#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""


#%% SECTION 1 inclusion de packages externes 


import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
# necessite scikit-image 
from skimage import io as skio
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage import img_as_float
from skimage.segmentation import chan_vese
from skimage.segmentation import checkerboard_level_set
from skimage.segmentation import circle_level_set

#%% SECTION 2 - Lecture de l'image

#im=skio.imread('coeurIRM.bmp')

#im=skio.imread('retineOA.bmp')

im=skio.imread('brain.bmp')
im=im[:,:,1]

#im=skio.imread('brain2.bmp')

plt.imshow(im, cmap="gray")

#%% SECTION 3a - Segmentation by contours actifs

s = np.linspace(0, 2*np.pi, 100)
r = 220 + 80*np.sin(s)
c = 220 + 80*np.cos(s)
init = np.array([r, c]).T

snake = active_contour(gaussian(im, 0.1),
                       init, alpha=0.05, beta=0.7, w_edge=1.6, gamma=0.005)


fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(im, cmap=plt.cm.gray)
ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, im.shape[1], im.shape[0], 0])

plt.show()

#%% SECTION 3b - Contours ouverts

# Interessant sur l'image retineOA.bmp

r = np.linspace(20, 80, 100)
c = np.linspace(20, 100, 100)
init = np.array([r, c]).T

snake = active_contour(gaussian(im, 1), init, bc='fixed',
                       alpha=0.01, beta=2, w_line=0, w_edge=10, gamma=0.01)

fig, ax = plt.subplots(figsize=(9, 5))
ax.imshow(im, cmap=plt.cm.gray)
ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, im.shape[1], im.shape[0], 0])

plt.show()

#%% SECTION 4 - Segmentation par ensembles de niveaux

image = img_as_float(im)

# Init avec un damier
#init_ls = checkerboard_level_set(image.shape, 6)

#Init avec un cercle
init_ls = circle_level_set (image.shape, (220,220), 40)

# Init avec plusieurs cercles
# =============================================================================
# circleNum = 8
# circleRadius = image.shape[0] / (3*circleNum)
# circleStep0 = image.shape[0]/(circleNum+1)
# circleStep1 = image.shape[1]/(circleNum+1)
# init_ls = np.zeros(image.shape)
# for i in range(circleNum):
#         for j in range(circleNum):
#             init_ls = init_ls + circle_level_set (image.shape, 
#                                                   ((i+1)*circleStep0, (j+1)*circleStep1), circleRadius)
# =============================================================================


cv = chan_vese(image, mu=0.9, lambda1=100, lambda2=1, tol=1e-3, max_iter=200,
               dt=0.5, init_level_set=init_ls, extended_output=True)

fig, axes = plt.subplots(2, 2, figsize=(8, 8))
ax = axes.flatten()

ax[0].imshow(image, cmap="gray")
ax[0].set_axis_off()
ax[0].set_title("Original Image", fontsize=12)

ax[1].imshow(cv[0], cmap="gray")
ax[1].set_axis_off()
title = "Chan-Vese segmentation - {} iterations".format(len(cv[2]))
ax[1].set_title(title, fontsize=12)

ax[2].imshow(cv[1], cmap="gray")
ax[2].set_axis_off()
ax[2].set_title("Final Level Set", fontsize=12)

ax[3].plot(cv[2])
ax[3].set_title("Evolution of energy over iterations", fontsize=12)

fig.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(9, 5))
ax.imshow(im, cmap=plt.cm.gray)
  
from skimage.measure import find_contours 
init_mask = find_contours(init_ls, 0.5)
for contour in init_mask:
	ax.plot(contour[:, 1], contour[:, 0], '--r', lw=3)
    
res = find_contours(cv[0], 0.5)
for contour in res:
	ax.plot(contour[:, 1], contour[:, 0], '--b', lw=3)
   
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, im.shape[1], im.shape[0], 0]) 
plt.show()

#%% FIN  TP - Modeles deformables
