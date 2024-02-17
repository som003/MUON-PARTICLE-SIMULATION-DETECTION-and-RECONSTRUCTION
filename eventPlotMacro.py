#!/usr/bin/env python
# coding: utf-8

# In[23]:


import numpy as np
import math
from ccdEvent import *
import matplotlib.pyplot as plt


# In[24]:


fileName1 = "pixelInfo_mu_slant2.dat"


# In[25]:


evt1 = ccdEvent(1,fileName1)


# In[26]:


npix = evt1.GetNPixelHits()


# In[27]:


xpixList = []
ypixList = []

for ij in range(npix):
    xpixList.append(evt1.GetPixelHit(ij).GetXPixel())
    ypixList.append(evt1.GetPixelHit(ij).GetYPixel())


# In[28]:


len(xpixList)


# In[29]:


plt.scatter(xpixList,ypixList)


# In[30]:


houghList = []
listRho = []
listTheta = []


# In[31]:


for ij in range(npix-1):
    for jk in range(ij+1,npix):
        iHoughCell = ccdHoughCell(evt1.GetPixelHit(ij),evt1.GetPixelHit(jk))
        listRho.append(iHoughCell.GetRho())
        listTheta.append(iHoughCell.GetTheta()*180/math.pi)
        houghList.append(iHoughCell)


# In[32]:


len(houghList)


# In[33]:


plt.scatter(listTheta,listRho)


# In[35]:


_ = plt.hist(listRho,bins=100,range=[-10,510])


# In[38]:


_ = plt.hist(listTheta,bins=180,range=[-90,90])


# In[ ]:




