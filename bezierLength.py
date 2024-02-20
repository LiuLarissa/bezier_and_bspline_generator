# compute the length of cubic bezier curve

import math
import numpy as np

GAUSS_LEGENDRE_COEFFS_8=[
    (0.3626837833783620, -0.1834346424956498),
    (0.3626837833783620, 0.1834346424956498),
    (0.3137066458778873, -0.5255324099163290),
    (0.3137066458778873, 0.5255324099163290),
    (0.2223810344533745, -0.7966664774136267),
    (0.2223810344533745, 0.7966664774136267),
    (0.1012285362903763, -0.9602898564975363),
    (0.1012285362903763, 0.9602898564975363)]

GAUSS_LEGENDRE_COEFFS_8_HALF=[
    (0.3626837833783620, 0.1834346424956498),
    (0.3137066458778873, 0.5255324099163290),
    (0.2223810344533745, 0.7966664774136267),
    (0.1012285362903763, 0.9602898564975363),]

GAUSS_LEGENDRE_COEFFS_16_HALF=[
    (0.1894506104550685, 0.0950125098376374),
    (0.1826034150449236, 0.2816035507792589),
    (0.1691565193950025, 0.4580167776572274),
    (0.1495959888165767, 0.6178762444026438),
    (0.1246289712555339, 0.7554044083550030),
    (0.0951585116824928, 0.8656312023878318),
    (0.0622535239386479, 0.9445750230732326),
    (0.0271524594117541, 0.9894009349916499)]

GAUSS_LEGENDRE_COEFFS_24_HALF=[
    (0.1279381953467522, 0.0640568928626056),
    (0.1258374563468283, 0.1911188674736163),
    (0.1216704729278034, 0.3150426796961634),
    (0.1155056680537256, 0.4337935076260451),
    (0.1074442701159656, 0.5454214713888396),
    (0.0976186521041139, 0.6480936519369755),
    (0.0861901615319533, 0.7401241915785544),
    (0.0733464814110803, 0.8200019859739029),
    (0.0592985849154368, 0.8864155270044011),
    (0.0442774388174198, 0.9382745520027328),
    (0.0285313886289337, 0.9747285559713095),
    (0.0123412297999872, 0.9951872199970213)]

# return bezier curve point at t
def getBezierPoint(controlPoints,t):
    n=4
    b=[math.comb(n-1,j)*t**j*(1-t)**(n-1-j) for j in range(n)]
    return np.dot(b,controlPoints)

def distance(point1,point2=np.array([0,0])):
    point=point1-point2
    return math.sqrt(point[0]**2+point[1]**2)

def distance2(point1,point2=np.array([0,0])):
    point=point1-point2
    return point[0]**2+point[1]**2

def midPoint(point1,point2):
    return 0.5*(point1+point2)

def subdivide(controlPoints):
    pm=getBezierPoint(controlPoints,0.5)
    nP0=controlPoints[0]
    nP1=midPoint(controlPoints[0],controlPoints[1])
    nP2=0.25*(controlPoints[0]+2*controlPoints[1]+controlPoints[2])
    points1=np.array([nP0,nP1,nP2,pm])
    mP1=0.25*(controlPoints[1]+2*controlPoints[2]+controlPoints[3])
    mP2=midPoint(controlPoints[2],controlPoints[3])
    points2=np.array([pm,mP1,mP2,controlPoints[3]])
    return points1,points2

def arclen_quadrature_core(coeffs,dm,dm1,dm2):
    length=0
    for i in range(len(coeffs)):
        w,x=coeffs[i]
        d=dm+dm2*(x*x)
        dpx=distance(d+dm1*x)
        dmx=distance(d-dm1*x)
        length+=math.sqrt(2.25)*w*(dpx+dmx)
    return length

def bezierLen(controlPoints,accuracy,depth):
    p0,p1,p2,p3=controlPoints[0],controlPoints[1],controlPoints[2],controlPoints[3]
    d03,d01,d12,d23=p3-p0,p1-p0,p2-p1,p3-p2
    lp_lc=distance(d01)+distance(d12)+distance(d23)-distance(d03)
    dd1,dd2=d12-d01,d23-d12

    dm=0.25*(d01+d23)+0.5*d12 # first derivative at midpoint, namely t=0.5
    dm1=(dd2+dd1)*0.5 # second derivative at midpoint
    dm2=(dd2-dd1)*0.25  # 0.5*(third derivative at midpoint)

    est=0

    for i in range(8):
        w,x=GAUSS_LEGENDRE_COEFFS_8[i]
        d_norm2=distance2(dm+dm1*x+dm2*(x*x))
        dd_norm2=distance2(dm1+dm2*(2*x))
        est+=math.fabs(w*dd_norm2/d_norm2)

    est_gauss8_error=min(est**3*2.5e-6,3e-2)*lp_lc
    if est_gauss8_error<accuracy:
        return arclen_quadrature_core(GAUSS_LEGENDRE_COEFFS_8_HALF,dm,dm1,dm2)
    
    est_gauss16_error=min(est**6*1.5e-11,9e-3)*lp_lc
    if est_gauss16_error<accuracy:
        return arclen_quadrature_core(GAUSS_LEGENDRE_COEFFS_16_HALF,dm,dm1,dm2)
    
    est_gauss24_error=min(est**9*3.5e-16,3.5e-3)*lp_lc
    if est_gauss24_error<accuracy or depth>=20:
        return arclen_quadrature_core(GAUSS_LEGENDRE_COEFFS_24_HALF,dm,dm1,dm2)
    
    c0,c1=subdivide(controlPoints)
    return bezierLen(c0,accuracy*0.5,depth+1)+bezierLen(c1,accuracy*0.5,depth+1)

points=np.array([[86,93],[25,190],[180,231],[214,100]])
print(bezierLen(points,1e-3,0))
