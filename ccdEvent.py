import math
import numpy as np
import matplotlib.pyplot as plt

class ccdPixelHit():
    def __init__(self, tx, ty):
        self.xpixel = tx
        self.ypixel = ty
        self.edep = 0.0
        self.iRed = 0.0
        self.iBlue = 0.0
        self.iGreen = 0.0

    def GetXPixel(self):
        return self.xpixel

    def GetYPixel(self):
        return self.ypixel

    def GetEdep(self):
        return self.edep

    def SetEdep(self, xx):
        self.edep = xx

    def isSame(self, xx):
        if (xx.GetXPixel() == self.xpixel and xx.GetYPixel() == self.ypixel):
            return True
        else:
            return False


class ccdHoughCell():
    def __init__(self, pix1, pix2):
        self.pixel1 = pix1
        self.pixel2 = pix2
        self.slope = (float(pix2.GetYPixel())-float(pix1.GetYPixel())) / \
            (float(pix2.GetXPixel())-float(pix1.GetXPixel())+1e-20)
        self.intercept = pix2.GetYPixel()-(self.slope*pix1.GetXPixel())
        self.theta = 90
        self.rho = math.fabs(self.intercept)
        if (math.fabs(self.slope) > 1e-6):
            self.theta = math.atan(-1.0/self.slope)*180/math.pi
            self.rho = math.fabs(self.intercept) * \
                math.fabs(math.sin(self.theta*math.pi/180))

    def GetPixel1(self):
        return self.pixel1

    def GetPixel2(self):
        return self.pixel2

    def GetSlope(self):
        return self.slope

    def GetIntercept(self):
        return self.intercept

    def GetTheta(self):
        return self.theta

    def GetRho(self):
        return self.rho


class ccdEvent():
    def __init__(self, tfname):
        self.eventID = -1
        self.momin = 0
        self.thein = -1000
        self.phiin = -1000
        self.allHits = self.fileRead(tfname)
        self.meanRho = -10.0
        self.sigmaRho = -10.0
        self.meanTheta = -1000.0
        self.sigmaTheta = -1000.0
        self.houghSelHits = self.ApplyHoughTransform()

    def GetMeanRho(self):
        return self.meanRho

    def GetSigmaRho(self):
        return self.sigmaRho

    def GetMeanTheta(self):
        return self.meanTheta

    def GetSigmaTheta(self):
        return self.sigmaTheta

    def AddPixelHit(self, xx):
        self.allHits.append(xx)

    def GetNPixelHits(self):
        return len(self.allHits)

    def GetNHoughPixelHits(self):
        return len(self.houghSelHits)

    def AddHoughSelHit(self, xx):
        isFill = True
        for ihc in self.houghSelHits:
            if (ihc.isSame(xx)):
                isFill = False
                break
        if isFill:
            self.houghSelHits.append(xx)

    def GetPixelHit(self, xx):
        return self.allHits[xx]

    def GetHoughSelHit(self, xx):
        return self.houghSelHits[xx]

    def fileRead(self, fileName):
        iHitList = []
        inputFile = open(fileName, 'r')
        ilin = 0
        for xx in inputFile:
            yy = xx.split()
            if (ilin == 0):
                self.eventID = int(yy[0])
            elif (ilin == 1):
                self.pidin = int(yy[1])
                self.momin = float(yy[2])
                self.thein = float(yy[3])
                self.phiin = float(yy[4])
            else:
                ipHit = ccdPixelHit(int(yy[2]), int(yy[3]))
                ipHit.SetEdep(float(yy[4]))
                iHitList.append(ipHit)
            ilin += 1

        # print(len(iHitList))
        return iHitList

    def ApplyHoughTransform(self):
        npix = self.GetNPixelHits()
        houghList = []
        thetaList = []
        rhoList = []


        for ij in range(npix-1):
            for jk in range(ij+1, npix):
                iHoughCell = ccdHoughCell(
                    self.GetPixelHit(ij), self.GetPixelHit(jk))
                houghList.append(iHoughCell)
                thetaList.append(iHoughCell.GetTheta())
                rhoList.append(iHoughCell.GetRho())

        self.meanRho = np.mean(rhoList)
        self.sigmaRho = math.sqrt(np.var(rhoList))
        self.meanTheta = np.mean(thetaList)
        self.sigmaTheta = math.sqrt(np.var(thetaList))

        for iter in range(100):
            listRho = []
            listTheta = []
            newHoughList = []
            nHoughCell = len(houghList)
            for ihc in houghList:
                if (ihc.GetTheta() < (self.meanTheta + self.sigmaTheta) and ihc.GetTheta() > (self.meanTheta-self.sigmaTheta) # type: ignore
                        and ihc.GetRho() < (self.meanRho + self.sigmaRho) and ihc.GetRho() > (self.meanRho - self.sigmaRho)): # type: ignore
                    newHoughList.append(ihc)
                    listRho.append(ihc.GetRho())
                    listTheta.append(ihc.GetTheta())
            print("mean, sigma : ", iter)
            print(self.meanRho, self.sigmaRho)
            print(self.meanTheta, self.sigmaTheta)
            if (len(newHoughList) < nHoughCell):
                nHoughCell = len(newHoughList)
                self.meanRho = np.mean(listRho)
                self.sigmaRho = math.sqrt(np.var(listRho))
                self.meanTheta = np.mean(listTheta)
                self.sigmaTheta = math.sqrt(np.var(listTheta))
                houghList = newHoughList
                if (self.sigmaTheta < 0.0001):
                    self.sigmaTheta = 0.0001
                if (self.sigmaRho < 0.0001):
                    self.sigmaRho = 0.0001
            else:
                break

        return houghList
        
    