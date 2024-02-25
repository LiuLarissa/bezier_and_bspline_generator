import numpy as np
import matplotlib.pyplot as plt
import math

def generateBezierControlPoints(controlPoints,k):
    n=len(controlPoints)
    N=n-k # N bezier curves

    knotVector=[0 for i in range(k)]
    knotVector.extend([i for i in range(1,N)])
    knotVector.extend([N for i in range(k)])
    polars={}
    points=[]
    tmp=[]
    fig,ax=plt.subplots()
    ax.plot(controlPoints[:,0],controlPoints[:,1],'o--')
    
    for i in range(n):
        key=''.join(map(str,knotVector[i:i+k]))
        polars[key]=controlPoints[i]
        points.append(key)
    
    def computePoints(key1,key2):
        nums=[i for i in key2]
        same=[]
        diff=0
        for i in key1:
            if i in nums:
                same.append(i)
                nums.remove(i)
            else:
                diff=int(i)
        if len(nums)==1:  # only 1 different
            diff1=int(nums[0])
            length=diff1-diff
            if length==1:return
            for j in range(diff+1,diff1):
                sameCopy=same.copy()
                sameCopy.append(str(j))
                sameCopy.sort()
                key=''.join(x for x in sameCopy)
                if key in polars.keys():continue
                else:
                    value=(polars[key2]*(j-diff)+polars[key1]*(diff1-j))/length
                    polars[key]=value
                    tmp.append(key)
            return
        else:return

    for j in range(k-1):
        tmp=[]
        for i in range(len(points)-1):
            r=0
            while i+r+1<len(points):
                r+=1
                computePoints(points[i],points[i+r])
        points=tmp
    
    for i in range(N):
        bezierControlPoints=[]
        for j in range(k):
            point=str(i)*(k-j)+str(i+1)*j
            bezierControlPoints.append(point)
        bezierControlPoints.append(str(i+1)*k)
        arrayPoints=np.array([polars[key] for key in bezierControlPoints])
        curvePoints=generate_bezier_curve(arrayPoints)
        ax.plot(curvePoints[:,0],curvePoints[:,1])
        ax.plot(arrayPoints[:,0],arrayPoints[:,1],'o--')
    
    plt.show()

def generate_bezier_curve(control_points, num_points=20):
    t = np.linspace(0, 1, num_points)
    n = len(control_points)
    curve_points = np.zeros((num_points, 2))

    for i in range(num_points):
        time=t[i]
        b=[math.comb(n-1,j)*time**j*(1-time)**(n-1-j) for j in range(n)]
        curve_points[i]=np.dot(b,control_points)

    return curve_points
    

controlPoints=np.array([[0, 0], [2, 3], [6, 3], [9, 0],[10,3],[12,3],[15,0],[16,2],[18,3]])
generateBezierControlPoints(controlPoints,5)
