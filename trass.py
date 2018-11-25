#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import math as mt
from PIL import Image, ImageDraw,ImageOps
#class definition#
class tras():
    check = 0#正しい順序で進んでいるかをチェックする
    def insert_direct(self,m,n,area,E,length,cnct,angle):
        self.M = m
        self.N = n
        self.area = area
        self.E = E
        self.length = length
        self.cnct = cnct
        self.angle = np.array(angle)*(np.pi/180.)
        
        self.check = 1
        if (len(area) != m) or (len(E) != m) or (len(length) != m) or (len(cnct) != m):
            print("your value is wrong")
            self.check = -1
            return -1
        return 0
        
    
    def make_K_easy(self,force):
        if self.check != 1:
            print("you have to do insert_value function")
            return -1
        self.force = force
        
        Ka =np. zeros ([N*2,N *2])
        for i in range (M):
            k= self.E[i]*self.area[i]/self.length[i]
            theta = self.angle[i]
            K=np.array([[1,0,-1,0],[0,0,0,0] ,[ -1 ,0 ,1 ,0] ,[0 ,0 ,0 ,0]])*k
            R=np.array([[np.cos(theta ),np.sin(theta),0,0],[-np.sin(theta),np.cos(theta),0,0],[0,0,np.cos(
theta),np.sin(theta)],[0,0,-np.sin(theta),np.cos(theta)]])
            zentai_K = np.dot(R.T,np.dot(K,R))
            start = self.cnct[i][0] - 1
            start_2 = self.cnct[i][1] - 1
            Ka[2*start:2*start+2,2*start:2*start+2] += zentai_K[0:2,0:2]
            Ka[2*start:2*start+2,2*start_2:2*start_2+2] += zentai_K[0:2,2:4]
            Ka[2*start_2:2*start_2+2,2*start:2*start+2] += zentai_K[2:4,0:2]
            Ka[2*start_2:2*start_2+2,2*start_2:2*start_2+2] += zentai_K[2:4,2:4]
        self.Katmp = Ka
        self.Ka = Ka
        self.check = 2
        return 0
    
    def adjust_steq(self,x_zero,y_zero):
        if self.check != 2:
            return -1
        self.x_zero = x_zero
        self.y_zero = y_zero
        kesu = []
        for i in x_zero:
            kesu.append(2*i-2)
        for j in y_zero:
            kesu.append(2*j-1)
        newK = np.delete(self.Ka,kesu,0)
        newK = np.delete(newK,kesu,1)
        self.newK = newK
        self.check = 3
        #print(newK.shape)
        #print(self.force.shape)
        return 0
    
    def solve_steq(self):
        if self.check != 3:
            return -1
        self.x = np.round(np.linalg.solve(self.newK,self.force),5)
        self.check = 4
        print(self.x)
        huyasu = []
        print(huyasu)
        print(self.x_zero)
        for j in self.x_zero:
            print(j)
            huyasu.append(2*j -2)
        for j in self.y_zero:
            huyasu.append(2*j -1)
        print(huyasu)
        for j in huyasu:
            if j > len(self.x):
                self.x = np.append(self.x,0)
            else:
                self.x = np.insert(self.x,j,0)
        print(self.x)
        return self.x

    def power(self):
        self.power = np.dot(self.Katmp,self.x)
        print(self.power)
    
    def zikuPower(self):
        ziku = []
        for i in range(M):
            angle = self.angle[i]
            start = self.cnct[i][0] - 1
            start2 = self.cnct[i][1] - 1
            zpower = self.E[i]*self.area[i]/self.length[i]*(-np.cos(angle)*self.x[2*start]-np.sin(angle)*self.x[2*start+1]+np.cos(angle)*self.x[2*start2]+np.sin(angle)*self.x[2*start2+1])
            ziku.append(round(zpower,2))
        self.ziku = ziku
        return ziku
    def drawImg(self,x,y):
        if (len(x) != self.N) or (len(x) != self.N):
            print("your value is wrong. your arguments hava to mutch N")
            return -1
        im = Image.new('RGB', (500, 300), (128, 128, 128))
        draw = ImageDraw.Draw(im)
        self.x=self.x*10
        for j in range(self.M):
            #元の部材の描画
            xini = int(x[self.cnct[j][0] - 1])
            xfin = int(x[self.cnct[j][1] - 1])
            yini = int(y[self.cnct[j][0] - 1])
            yfin = int(y[self.cnct[j][1] - 1])
            size = int(10*self.area[j]/max(self.area))
            if self.ziku[j] > 0:
                draw.line((xini,yini,xfin,yfin),fill=(0,255,0),width = 1)
            else:
                draw.line((xini,yini,xfin,yfin),fill=(0,255,255),width = 1)
            #変位の描画
            xini = int(x[self.cnct[j][0] - 1] + self.x[2*(self.cnct[j][0] - 1)])
            xfin = int(x[self.cnct[j][1] - 1] + self.x[2*(self.cnct[j][1] - 1)])
            yini = int(y[self.cnct[j][0] - 1] + self.x[2*(self.cnct[j][0] - 1)+1])
            yfin = int(y[self.cnct[j][1] - 1] + self.x[2*(self.cnct[j][1] - 1)+1])
            draw.line((xini,yini,xfin,yfin),fill=(255,0,0),width = 1)
        im = ImageOps.flip(im)
        #im = ImageOps.mirror(im)
        im.show()
        
        
        return 0
    
#def analyze_all():

#main function#
#param    
M = 10
N = 6  
area =[10*np.sqrt(2) ,10. ,10. ,10. ,10. ,10* np.sqrt(2) ,10* np.sqrt(2) ,10. ,10. ,10* np.sqrt(2) ]
area = np.array(area)*0.0001
E =[70.*10**9 for i in range (10) ]
lgth =[10*np.sqrt(2) ,10. ,10. ,10. ,10. ,10* np.sqrt(2) ,10* np.sqrt(2) ,10. ,10. ,10*np.sqrt(2)]
cnct =[[1 ,2] ,[1 ,3] ,[2 ,3] ,[2 ,4] ,[3 ,5] ,[3 ,4] ,[2 ,5] ,[4 ,5] ,[5 ,6] ,[4 ,6]]
angle = [45,0,-90,0,0,45,-45,-90,0,-45]
force =np.array([0 ,0 ,0 , -900. ,0 ,0 ,0 , -500. ,0])    
force =force*1000
x_zero = [1]
y_zero = [1,6]
x = [0,1,1,2,2,3]
y = [0,1,0,1,0,0]
    
instance = tras()
tras.insert_direct(instance,M,N,area,E,lgth,cnct,angle)
tras.make_K_easy(instance,force)
tras.adjust_steq(instance,x_zero,y_zero)
heni = tras.solve_steq(instance)
tras.power(instance)
zikuryoku = tras.zikuPower(instance)
#tras.drawImg(instance,x,y)
tras.drawImg(instance,[(t+1)*200/max(x) for t in x],[(t+1)*200/max(x) for t in y])
