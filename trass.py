#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 19:41:44 2018

"""
import numpy as np

def sweep_out(L,m):
    N1= len (L)
    N2= len (L [0])
    Lm =[L[i][m] for i in range (N1)]
    for i in range (N1):
        if i==m:
            pass
        else :
            for k in range (N2):
                L[i][k]-=L[m][k]* Lm[i]
    return L

def choice_sweep(L,m):
    L = sweep_out(L,m)
    return L

def choice_sweep_all(L):
    for m in range(len(L)):
        L = choice_sweep(L,m)
    return L 

def k_mat(N,M,area,E,lgth,cnct,theta_d):
    Ka =np. zeros ([N*2,N *2])
    for i in range (M):
        k= E[i]*area[i]/lgth[i]
        theta = theta_d[i]/180.* np.pi
        K=np.array([[1,0,-1,0],[0,0,0,0] ,[ -1 ,0 ,1 ,0] ,[0 ,0 ,0 ,0]])*k
        R=np.array([[np.cos(theta ),np.sin(theta),0,0],[-np.sin(theta),np.cos(theta),0,0],[0,0,np.cos(
theta),np.sin(theta)],[0,0,-np.sin(theta),np.cos(theta)]])
        zentai_K = np.dot(R.T,np.dot(K,R))
        start = cnct[i][0] - 1
        start_2 = cnct[i][1] - 1
        Ka[2*start:2*start+2,2*start:2*start+2] += zentai_K[0:2,0:2]
        Ka[2*start:2*start+2,2*start_2:2*start_2+2] += zentai_K[0:2,2:4]
        Ka[2*start_2:2*start_2+2,2*start:2*start+2] += zentai_K[2:4,0:2]
        Ka[2*start_2:2*start_2+2,2*start_2:2*start_2+2] += zentai_K[2:4,2:4]
        print(Ka)
    return Ka

def gs_in(K,x_zero,y_zero,forcex,forcey):
    kesu = []
    print(K.shape)
    for i in x_zero:
        kesu.append(2*(i-1))
    for j in y_zero:
        print(j)
        kesu.append(2*(j-1) + 1)
    newK = np.delete(K,kesu,0)
    newK = np.delete(K,kesu,1)
    forcex = np.array(forcex)
    print(newK.shape)
    print(forcex.shape)
    
    return 0
    
  


def main():
    M = 6
    N = 10  
    area =[30*np.sqrt(2) ,30. ,30. ,30. ,30. ,30* np.sqrt(2) ,30* np.sqrt(2) ,30. ,30. ,30* np.sqrt(2) ]
    E =[70.*10**9 for i in range (10) ]
    lgth =[6*np.sqrt(2) ,6. ,6. ,6. ,6. ,6* np.sqrt(2) ,6* np.sqrt(2) ,6. ,6. ,6*np.sqrt(2)]
    cnct =[[1 ,2] ,[1 ,3] ,[2 ,3] ,[2 ,4] ,[3 ,5] ,[3 ,4] ,[2 ,5] ,[4 ,5] ,[5 ,6] ,[4 ,6]]
    angle = [45,0,-90,0,0,45,-45,-90,-45]
    forcey =np.array([0 ,0 ,0 , -500. ,0 ,0 ,0 ,0, -200. ,0])
    forcey =forcey*1000
    forcex = np.array([0,0,0,0,0,0,0,0,0,0])
    print(forcex)
    x_zero = [1]
    y_zero = [1,6]
    K = k_mat(N,M,area,E,lgth,cnct,angle)
    gs = gs_in(K,x_zero,y_zero,forcex,forcey)


    return x
    
main()
