#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import math
from ccdEvent import *
import matplotlib.pyplot as plt


# In[14]:


fileName1 = "pixelInfo_e_slant2.dat"


# In[15]:


evt1 = ccdEvent(1,fileName1)


# In[16]:


npix = evt1.GetNPixelHits()


# In[17]:


xpixList = []
ypixList = []

for ij in range(npix):
    xpixList.append(evt1.GetPixelHit(ij).GetXPixel())
    ypixList.append(evt1.GetPixelHit(ij).GetYPixel())


# In[18]:


len(xpixList)


# In[19]:


plt.scatter(xpixList,ypixList)


# In[20]:


houghList = []
listRho = []
listTheta = []


# In[21]:


for ij in range(npix-1):
    for jk in range(ij+1,npix):
        iHoughCell = ccdHoughCell(evt1.GetPixelHit(ij),evt1.GetPixelHit(jk))
        listRho.append(iHoughCell.GetRho())
        listTheta.append(iHoughCell.GetTheta()*180/math.pi)
        houghList.append(iHoughCell)


# In[22]:


len(houghList)


# In[23]:


plt.scatter(listTheta,listRho)


# In[24]:


_ = plt.hist(listRho,bins=100,range=[-10,510])


# In[25]:


_ = plt.hist(listTheta,bins=180,range=[-90,90])


# In[ ]:




