import argparse


import cv2
import numpy as np

import matplotlib.pyplot as plt
from scipy import interpolate

class Fourier():
    def fourier(self,i_data, t_data):
        kaisu = 50 # フーリエ級数展開の回数
        T = 2*np.pi
        dt = T/kaisu
        point = len(i_data)
        t = np.arange(0,dt*point,dt)
        
        def cos(t, n):
            return np.cos(n * 2 * np.pi / T * t)  # cos(n * ωt)
        def sin(t, n):
            return np.sin(n * 2 * np.pi / T * t)

        i_gu = i_ki = 0
        for n in range(1, kaisu + 1):
            i_cos = i_data * cos(t_data, n)
            an = (2 / T) * i_cos.sum() * dt
            i_gu += an * cos(t, n)

            i_sin = i_data * sin(t_data, n)
            bn = (2 / T) * i_sin.sum() * dt
            i_ki += bn * sin(t, n)
        return [i_gu, i_ki]



class char_trans(Fourier):
    def __init__(self,width=300,height=300):
        self.width = width
        self.height = height

    def write_dot(self,img_path):
        img = np.zeros((self.width,self.height),np.uint8)
        with open(img_path, 'r') as f:
            dots =f.read().split('\n')
        for dot in dots:
            if dot == '':
                continue
            
            x,y = list(map(int, dot.split(',')))
            img[y][x] = 255
        return img

    def spline(self,x,y,point,deg):
        tck,u = interpolate.splprep([x,y],k=deg,s=0) 
        u = np.linspace(0,1,num=point,endpoint=True) 
        spline = interpolate.splev(u,tck)

        return spline[0],spline[1]

    def write_spline_dot(self,img_path):
        img = np.zeros((self.width,self.height),np.uint8)
        with open(img_path, 'r') as f:
            dots =f.read().split('\n')
        X,Y = [],[]
        for dot in dots:
            if dot == '':
                continue  
            x,y = list(map(int, dot.split(',')))
            X.append(x)
            Y.append(y)
        X,Y = self.spline(X,Y,1000,2)
        for x,y in zip(X,Y):
            img[int(round(y))][int(round(x))] = 255
        return X,Y,img


    def write_fourier_dot(self,img_path):
        X, Y, _ = self.write_spline_dot(img_path)
        t = np.linspace(0, np.pi, len(X))
        i,j = self.fourier(X, t)[0],self.fourier(Y, t)[0]
        # 正規化
        i,j = i-min(i), j-min(j)
        i,j = i/max(i), j/max(j)

        return i*self.width,j*(-self.height)




class char_averaging(char_trans):
    def __init__(self,width,height,*img_paths):
        self.img_paths = img_paths
        super().__init__(width,height)
    def char_ave(self,a):
        I,J = [],[]

        for img_path in self.img_paths:    
            i,j = self.write_fourier_dot(img_path)
            I.append(i)
            J.append(j)
        
        X =  (a*I[0] + (1-a)*I[1])/2
        Y =  (a*J[0] + (1-a)*J[1])/2
        return X,Y

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('txt1',type=str)
    parser.add_argument('txt2',type=str)
    args = parser.parse_args()

    chr = char_averaging(300,300,args.txt1,args.txt2)
    
    name = args.txt1.split('/')[1].rstrip('.txt')[:-1]
    
    for a in np.arange(0.0,1.0,0.01):
        X,Y = chr.char_ave(a)
        fig = plt.figure(figsize=(6,6), dpi=50)
        ax = fig.add_subplot(1, 1, 1)
        ax.axis('off')
        ax.plot(X*300,Y*300,'k')
        plt.savefig('images/{0}/{0}_{1}.png'.format(name,a))
        fig.clf()
        plt.close()

if __name__=='__main__':
    main()
