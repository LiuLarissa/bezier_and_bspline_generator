import numpy as np
import matplotlib.pyplot as plt
import math

def generateBezierControlpoints(controlPoints,k):
    n=len(controlPoints)
    N=n-k
    knotVector=[0 for i in range(k)]
    knotVector.extend([i for i in range(1,N)])
    knotVector.extend([N for i in range(k)])
    polars={}
    points=[]
    fig,ax=plt.subplots()
    ax.plot(controlPoints[:,0],controlPoints[:,1],'o--')
    
    for i in range(n):
        key=''.join(map(str,knotVector[i:i+k]))
        polars[key]=controlPoints[i]
        points.append(key)
    
    for i in range(k-1):
        tmp=[]
        for i in range(len(points)-1):
            diffs=keyDiff(points[i],points[i+1])
            tmp.extend(diffs)
            m=len(diffs)
            length=m+1
            for n in diffs:
                v=(m*polars[points[i]]+(length-m)*polars[points[i+1]])/length
                polars[n]=v
                m-=1
        points=tmp
    
    for i in range(N):
        start=''.join(map(str,[i for j in range(k)]))
        bezierControlpoints=[start]
        for j in range(k):
            lastPoint=bezierControlpoints[-1]
            newP=lastPoint[:k-j-1]+''.join(map(str,[i+1 for m in range(j+1)]))
            bezierControlpoints.append(newP)
        arrayPoints=np.array([polars[key] for key in bezierControlpoints])
        print(arrayPoints)
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


def keyDiff(key1,key2):
    diffs=[key1]
    n=len(key1)
    j=n-1
    while(j>0):
        if key1[j]==key2[j]:j-=1
        else:break
    
    for i in range(j):
        p=diffs[-1]
        if p[i]!=key2[i]:
            newP=p[0:i]+key2[i]+p[i+1:]
            diffs.append(newP)
    return diffs[1:]

controlPoints=np.array([[0, 0], [2, 3], [6, 3], [9, 0],[10,3],[12,2]])
generateBezierControlpoints(controlPoints,3)