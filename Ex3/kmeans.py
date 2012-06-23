#!/usr/bin/python
import os
import math
import random
import operator
import numpy
from numpy import mean,cov,double,cumsum,dot,linalg,array,rank
from pylab import plot,subplot,axis,stem,show,figure

class cluster(object):

    
    def __init__(self):
        pass
        
    @staticmethod
    def read( file_name):
        data=[]
        with open(file_name) as file:
            for line in file:
                point=[float(s) for s in line.split()]
                data.append(point)
        return data        
            
    def kmeans_with_mapping(self,data,number_of_clusters=2,coeff=[1,1]):
        
        data2 = self._map(data,coeff)
        return self.kmeans(data2,number_of_clusters,[1])      
        
        pass   
    def kmeans(self, data,number_of_clusters, subset):
        #self.label = array
        
        data2 = self._feature_selection(data,subset)
        ncol = sum(subset) #check if subset only contains 1,0
        nrow = len(data2)
        clusters= self._initial_clusters(nrow,number_of_clusters)
        means = self._calculate_means(data2, clusters,ncol,number_of_clusters)
        prev_distort=0
        
        while abs(self._distortion(data2, means, clusters)-prev_distort) >0.01:
            
            #print "means", means
            prev_distort=self._distortion(data2, means, clusters)
            #print prev_distort
            for j,point in enumerate(data2):
                clusters[j] = self._min_distance(point, means)
            
            means = self._calculate_means(data2, clusters,ncol,number_of_clusters)
                
        return (clusters,means,prev_distort)
        
    def _map(self,orig_data,coeff):
        data=[]
        for point in orig_data:
            s=0
            for i,coord in enumerate(point):
               s = s + coeff[i] * coord
            data.append([s])
        sums=0.0
        for point in data:
            sums = sums + point[0]
        sums=sums/len(data)
        data2=[]
        for point in data:
            data2.append([point[0]-sums])    
        return data2 
            
            
    def _calculate_means(self,data2, clusters,ncol,number_of_clusters):
        segments=[[] for i in range(number_of_clusters)]
        means = []
        for i,cluster in enumerate(clusters):
#            print 'cluster',cluster
            segments[cluster].append(data2[i])
            #print segments[cluster],'\n\n'
#        print len(segments),'\n'    
        for i,segment in enumerate(segments):
            count = [0.0]*ncol
            for point in segment:
                
            #print "segment:",segment
                for j in range(ncol):
                    count[j] = count[j]+point[j]
            for j in range(ncol):
                 #print "len seg",count[j]
                 count[j]=count[j]/len(segment)
                
                    
            means.append(count)
        return(means)    
    
    def _initial_clusters(self,nrow,number_of_clusters):
        return [random.randrange(number_of_clusters) for i in range(nrow)]
    
    def _feature_selection(self,orig_data,subset):
        data=[]
        for point in orig_data:
            data.append( [v for i, v in enumerate(point) if subset[i] ]) 
        return data
    
    def _distance(self,point1, point2):
        s=0
        if len(point1) != len(point2):
            raise 
        for i in range (len(point1)):
            s= s + (point1[i]-point2[i])**2
            
        d = math.sqrt(s)    
        return d
    def _distortion(self, data, means, clusters):
        distort=0.0
        for i,point in enumerate(data):
            distort = distort + self._distance(point,means[int(clusters[i])])
        return(distort)
        
    def _min_distance(self,point1, points):
        dists=[self._distance(point1,point) for point in points]
        min_index, min_value = min(enumerate(dists), key=operator.itemgetter(1))
        return min_index
        
    def pca(self,data):
        data = self.convert(data)
        M = (data-mean(data.T,axis=1)).T # subtract the mean (along columns)
        [latent,coeff] = linalg.eig(cov(M))
        score = dot(coeff.T,M) # projection of the data in the new space
        return coeff,score,latent
            
    def convert(self,data):
         if data:
             new_data=[[] for i in range(len(data[0]))]
             for point in data:
                 for i in range(len(point)):
                     new_data[i].append(point[i])
             return numpy.array(new_data)
         else:
             raise   
        
if __name__ == '__main__':
    c = cluster()
    data = cluster.read('exercise3-data.txt')
    np_data = c.convert(data)
    (clusters1,means1, distortion1) = c.kmeans(data,2,[1,0])
    (clusters2,means2, distortion2) = c.kmeans(data,2,[0,1])
    (clusters3,means3, distortion3) = c.kmeans(data,2,[1,1])
    #(clusters4,means4, distortion4) = c.kmeans_with_mapping(data,2,[1,1])
    #print distortion1,distortion2,distortion3,distortion4
    coeffs_list=[]
    distortions=[]    
    for coeff1 in numpy.arange(0,2,0.1):
        for coeff2 in numpy.arange(0,2,0.1):
             if coeff1==0 and coeff2==0:
                continue
             (clusters_r,means_r, distortion_r) = c.kmeans_with_mapping(data,2,[coeff1,coeff2])
             #print (coeff1,coeff2),distortion_r
             coeffs_list.append((coeff1,coeff2))
             distortions.append(distortion_r)

    min_index, min_value = min(enumerate(distortions), key=operator.itemgetter(1))
    (clusters4,means4, distortion4) = c.kmeans_with_mapping(data,2,[coeffs_list[min_index][0],coeffs_list[min_index][1]])
    
    print "with just first feature:",distortion1,"\nwith just second feature:",distortion2,"\nwith just both features:",distortion3
    print "mapping with ",coeffs_list[min_index]," result in this distortion",min_value        
    
    
    
    cluster0 =[[],[],[],[]]
    cluster1 =[[],[],[],[]]
    for i,point in enumerate(data):
        if clusters1[i]==0:
            cluster0[0].append(point)
        else:
            cluster1[0].append(point)
        
        if clusters2[i]==0:
            cluster0[1].append(point)
        else:
            cluster1[1].append(point)
            
        if clusters3[i]==0:
            cluster0[2].append(point)
        else:
            cluster1[2].append(point)
        
        if clusters4[i]==0:
            cluster0[3].append(point)
        else:
            cluster1[3].append(point)
    
   
    
    figure()
    subplot(141)
    a=c.convert(cluster0[0])
    b=c.convert(cluster1[0])
    plot(a[0,:],a[1,:],'ob')
    plot(b[0,:],b[1,:],'xr')    
    subplot(142)
    a=c.convert(cluster0[1])
    b=c.convert(cluster1[1])
    plot(a[0,:],a[1,:],'ob')
    plot(b[0,:],b[1,:],'xr')
    subplot(143)
    a=c.convert(cluster0[2])
    b=c.convert(cluster1[2])
    plot(a[0,:],a[1,:],'ob')
    plot(b[0,:],b[1,:],'xr')    
    subplot(144)
    a=c.convert(cluster0[3])
    b=c.convert(cluster1[3])
    plot(a[0,:],a[1,:],'ob')
    plot(b[0,:],b[1,:],'xr')    
    show()        
        
    
    
    #coeff,score, latent = c.pca(data)
    #figure()
    #subplot(121)
    #plot(np_data[0,:],np_data[1,:],'ob')
    #axis('equal')
    #subplot(122)
    #print len(score)
    #plot(score[0,:],score[1,:],'*g')
    #axis('equal')
    #show()
    #print score

