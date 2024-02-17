from fileinput import filename
import numpy as np
import math
from ccdEvent import *
import matplotlib.pyplot as plt

class readfiles(self,fname):
    self.fname = fileName
    evt1 = ccdEvent(1, filename)

    npix = evt1.GetNPixelHits()

    xpixList = []
    ypixList = []

    for ij in range(npix):
        xpixList.append(evt1.GetPixelHit(ij).GetXPixel())
        ypixList.append(evt1.GetPixelHit(ij).GetYPixel())

    plt.scatter(xpixList, ypixList)
    # plt.show()

    houghList = []
    thetaList = []
    rhoList = []

    for ij in range(npix-1):
        for jk in range(ij+1, npix):
            iHoughCell = ccdHoughCell(evt1.GetPixelHit(ij), evt1.GetPixelHit(jk))
            houghList.append(iHoughCell)
            thetaList.append(iHoughCell.GetTheta())
            rhoList.append(iHoughCell.GetRho())

    nHoughCell = len(houghList)
    meanRho = np.mean(rhoList)
    sigmaRho = math.sqrt(np.var(rhoList))
    meanTheta = np.mean(thetaList)
    sigmaTheta = math.sqrt(np.var(thetaList))

    for iter in range(100):
        listRho = []
        listTheta = []
        newHoughList = []
        for ihc in houghList:
            if (ihc.GetTheta() < (meanTheta+sigmaTheta) and ihc.GetTheta() > (meanTheta-sigmaTheta)
                    and ihc.GetRho() < (meanRho + sigmaRho) and ihc.GetRho() > (meanRho - sigmaRho)):
                newHoughList.append(ihc)
                listRho.append(ihc.GetRho())
                listTheta.append(ihc.GetTheta())
        print("mean, sigma : ", iter)
        print(meanRho, sigmaRho)
        print(meanTheta, sigmaTheta)
        if (len(newHoughList) < nHoughCell):
            nHoughCell = len(newHoughList)
            meanRho = np.mean(listRho)
            sigmaRho = math.sqrt(np.var(listRho))
            meanTheta = np.mean(listTheta)
            sigmaTheta = math.sqrt(np.var(listTheta))
            houghList = newHoughList
            if (sigmaTheta < 0.0001):
                sigmaTheta = 0.0001
            if (sigmaRho < 0.0001):
                sigmaRho = 0.0001
        else:
            break
        
    print("mean, sigma : final")
    print(meanRho, sigmaRho)
    print(meanTheta, sigmaTheta)
    
    
    for ihc in houghList:
        if (ihc.GetTheta() < (meanTheta+sigmaTheta) and ihc.GetTheta() > (meanTheta-sigmaTheta)
                and ihc.GetRho() < (meanRho + sigmaRho) and ihc.GetRho() > (meanRho - sigmaRho)):
            evt1.AddHoughSelHit(ihc.GetPixel1())
            evt1.AddHoughSelHit(ihc.GetPixel2())
    
    xpixHoughList = []
    ypixHoughList = []
    
    for ij in range(evt1.GetNHoughPixelHits()):
        xpixHoughList.append(evt1.GetHoughSelHit(ij).GetXPixel())
        ypixHoughList.append(evt1.GetHoughSelHit(ij).GetYPixel())
    
    plt.scatter(xpixHoughList, ypixHoughList)
    plt.show()