# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:54:49 2023

@author: HP
"""
import sympy as sym
import numpy as np
import matplotlib.pyplot as plt

x = sym.Symbol('x',real=True)
y = sym.Symbol('y',real=True)

def GetLaggereRecursive(n,x):

    if n==0:
        poly = 1
    elif n==1:
        poly = -x+1
    else:
        poly = ((2*n-1-x)*GetLaggereRecursive(n-1,x)-(n-1)*GetLaggereRecursive(n-2,x))/n

    return sym.simplify(poly)


def GetDLaggere(n,x):
    Pn = GetLaggereRecursive(n,x)
    return sym.diff(Pn,x,1)

def GetNewton(f,df,xn,itmax=10000,precision=1e-14):
    error = 1.
    it = 0
    while error >= precision and it < itmax:
        try:
            xn1 = xn - f(xn)/df(xn)
            error = np.abs(f(xn)/df(xn))
        except ZeroDivisionError:
            print('Zero Division')
        xn = xn1
        it += 1
    if it == itmax:
        return False
    else:
        return xn
    
def GetRoots(f,df,x,tolerancia = 10):
    Roots = np.array([])
    for i in x:
        root = GetNewton(f,df,i)
        if  type(root)!=bool:
            croot = np.round( root, tolerancia )
            if croot not in Roots:
                Roots = np.append(Roots, croot)
    Roots.sort()
    return Roots

def GetAllRootsGLag(n):
    xn = np.linspace(0,n+((n-1)*np.sqrt(n)),100)
    Laggere = []
    DLaggere = []
    
    for i in range(n+1):
        Laggere.append(GetLaggereRecursive(i,x))
        DLaggere.append(GetDLaggere(i,x))
    
    poly = sym.lambdify([x],Laggere[n],'numpy')
    Dpoly = sym.lambdify([x],DLaggere[n],'numpy')
    Roots = GetRoots(poly,Dpoly,xn)

    if len(Roots) != n:
        ValueError('El número de raíces debe ser igual al n del polinomio.')
    
    return Roots


def GetWeightsGLag(n):

    Roots = GetAllRootsGLag(n)

    weights=[]
    for i in range(n):
        Lagroot = GetLaggereRecursive(n+1,Roots[i])
        Weight = Roots[i]/(((n+1)**2)*(Lagroot)**2)
        weights.append(Weight)
    
    return weights


import matplotlib.pyplot as plt

def integral(f,n):
    pesos=GetWeightsGLag(n)
    raices=GetAllRootsGLag(n)  
    I=0
    for i in range(n):
        I+= pesos[i]*f(raices[i])
        i+=1
    return I


f= lambda x: ((x**3)*((np.exp(x))-1))/((np.exp(x))-2+(1/np.exp(x)))

r=np.linspace(1,7,7)

print(integral(f,2))

def graf(n,f):
    lista=[]
    for i in n:
        lista.append(integral(f,int(i))/((np.pi**4)/15))
    plt.scatter(n,lista)
    plt.show()
    
#graf(r,f) copiar y pegar para el 17


import numpy as np

m = np.array([[1, 2, -1], [1, 0, 1], [4, -4, 5]], dtype=float)
q = np.array([1, 2, 1], dtype=float)

def multi(m, vp):
    if len(vp.shape) == 1:  # Comprueba si vp es un vector
        vp = vp.reshape(-1, 1)  # Convierte vp en una matriz columna
    c1 = len(m[0])
    f2, c2 = vp.shape  # Obtiene la forma de vp
    if c1 != f2:
        print("Las matrices no se pueden multiplicar")
    else:
        f1 = len(m)
        r = np.zeros(shape=(f1, c2))

        for i in range(f1):
            for j in range(c2):
                for k in range(c1):
                    r[i][j] += m[i][k] * vp[k][j]
        return r

def mew(q, m):
    a = multi(m, q)
    return multi(a, q)

def potinv(m, q):
    for i in range(10):
        z = multi(m, q)
        q = z / np.sqrt(np.matmul(z.T, z))
        print(q)
        j = mew(q, q)
    return j

print(potinv(m, q))










