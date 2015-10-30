import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from sympy.solvers import solve
from sympy import Symbol

def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

VTO = .7
UN = .05
UP = .02
TOX = 1.5e-8
EPSILON = 3.4515e-13
COX = 2.3e-5
WLN = 10
WLP = .1
KN = 5.75e-6
KP = 2.3e-8
LAMBDA = .05
GAMA = .5

def nmos(vout,vin):
    vds = vout
    vgs = vin
    if vgs < VTO :
        return cutoff
    elif vds > (vgs-VTO):
        return saturationN
    else:
        return triodeN

def pmos(vout,Vgs):
    vds = 5 - vout
    vgs = vin
    if vgs < VTO :
        return cutoff
    elif vds > (vgs-VTO):
        return saturationP
    else:
        return triodeP

def cutoff(vout,vin):
    return 0

def saturationN(vout,vin):
    vov = vin - VTO
    vds = vout
    return KN*(vov**2)*(1+LAMBDA*(vds))

def saturationP(vout,vin):
    vov = 5-VTO
    vds = 5-vout
    return KP*(vov**2)*(1+LAMBDA*(vds))

def triodeN(vout,vin):
    vov = vin - VTO
    vds = vout
    return 2*KN*(vov*vds-((vds**2)/2))*(1+LAMBDA*(vds))

def triodeP(vout,vin):
    vov = 5 - VTO
    vds = 5 - vout
    return 2*KP*(vov*vds-((vds**2)/2))*(1+LAMBDA*(vds))

def output(vin):
    if vin < VTO :
        return cutoff
    vout = Symbol('vout')
    print solve()



if __name__ == "__main__":
    for vin in range(0,6,1):
        print vin
        x,y1,y2 = [],[],[]
        for vout in drange(0,5,.1):
            f1 = nmos(vout,vin)
            f2 = pmos(vout,vin)
            x.append(vout)
            y1.append(f1(vout,vin))
            y2.append(f2(vout,vin))
        print 'generating plot'
        fig1 = plt.figure()
        plot1 = fig1.add_subplot(111)
        plot1.plot(x,y1, "-b", label='Idn')
        plot1.plot(x,y2, "-g", label='-Idb')
        plot1.legend(loc=5)
        fig1.savefig('HW6-1-{}.pdf'.format(vin))

        fig2 = plt.figure()
        plot2 = fig2.add_subplot(111)
        plot2.plot(x,y2, "-g", label='-Idb')
        plot2.legend(loc=5)
        fig2.savefig('HW6-1-{}-pmos.pdf'.format(vin))

    f1 = pmos(2.5,0.946982)
    f2 = nmos(2.5,0.946982)
    print f1.__name__
    print f1(2.5,0.946982)
    print f2.__name__
    print f2(2.5,0.946982)
