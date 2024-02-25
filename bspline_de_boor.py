import numpy as np
import matplotlib.pyplot as plt
import math

def generateBezierControlpoints(controlPoints,k):
    n=len(controlPoints)
    N=n-k  # N bezier curves
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
    

    for j in range(k-1):
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

    def pointMinus(point):
        length=len(point)
        for i in range(length-1,0,-1):
            if point[i]==point[i-1]:
                if i==1:return str(int(point[0])-1)+point[1:]
                else:continue
            else:
                return point[0:i]+str(int(point[i])-1)+point[i+1:]
    
    def pointAdd(point):
        length=len(point)
        for i in range(length-1):
            if point[i]==point[i+1]:
                if i==length-2:return point[0:i+1]+str(int(point[i+1])+1)
                else:continue
            else:
                return point[0:i]+str(int(point[i])+1)+point[i+1:]

    def getBezierControlPoint(point):
        if point in polars.keys():return polars[point]
        else:
            pointM=getBezierControlPoint(pointMinus(point))
            pointA=getBezierControlPoint(pointAdd(point))
            v=0.5*(pointM+pointA)
            polars[point]=v
            return v

    for i in range(N):
        bezierControlPoints=[]
        for j in range(k):
            point=str(i)*(k-j)+str(i+1)*j
            bezierControlPoints.append(point)
        bezierControlPoints.append(str(i+1)*k)
        arrayPoints=np.array([getBezierControlPoint(key) for key in bezierControlPoints])
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
    if key1==key2:return []
    diffs=[key1]
    
    def subKeyDiff(key1,key2):
        n=len(key1)
        for i in range(n):
            if key1[i]==key2[i]:
                if i==n-1: diffs.append(key2)
                else:continue
            else:
                if i!=n-1:
                    if key1[i+1]==key2[i]:
                        newP=key1[0:i]+key2[i]+key1[i+1:]
                        diffs.append(newP)
                        return
                    else:continue
                else: 
                    newP=key1[0:i]+key2[i]
                    diffs.append(newP)
                    return

    while diffs[-1]!=key2:
        subKeyDiff(diffs[-1],key2)
    return diffs[1:len(diffs)-1]
    

controlPoints=np.array([[0, 0], [2, 3], [6, 3], [9, 0],[10,3],[12,3],[15,2],[16,0]])
generateBezierControlpoints(controlPoints,4)
