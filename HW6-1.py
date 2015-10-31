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

#calculates mode of opperation given vout and vin for nmos
def nmos(vout,vin):
    vds = vout
    vgs = vin
    if vgs < VTO :
        return cutoff
    elif vds > (vgs-VTO):
        return saturationN
    else:
        return triodeN

#calculates mode of opperation given vout and vin for pmos
def pmos(vout):
    vds = 5 - vout
    vgs = 5
    if vgs < VTO :
        return cutoff
    elif vds > (vgs-VTO):
        return saturationP
    else:
        return triodeP

#current calculation if either is in cutoff
def cutoff(vout,vin):
    return 0

#current calculation if nmos is in stauration 
def saturationN(vout,vin):
    vovn = vin - VTO
    vdsn = vout
    return KN*(vovn**2)*(1+LAMBDA*(vdsn))

#current calculation if pmos is in saturation
def saturationP(vout):
    vovp = 5-VTO
    vdsp = 5-vout
    return KP*(vovp**2)*(1+LAMBDA*(vdsp))

#current calculation if nmos is in triode
def triodeN(vout,vin):
    vovn = vin - VTO
    vdsn = vout
    return 2*KN*(vovn*vdsn-((vdsn**2)/2))*(1+LAMBDA*(vdsn))

#current calculation if pmos is in triode
def triodeP(vout):
    vovp = 5 - VTO
    vdsp = 5 - vout
    return 2*KP*(vovp*vdsp-((vdsp**2)/2))*(1+LAMBDA*(vdsp))

#checks if output voltage results in both devices in saturation and if not recalculates for new mode of opperation
def check(out,vin):
    vovn = vin - VTO
    vdsn = out
    vovp = 5-VTO
    vdsp = 5-out
    #nmos in triode
    if(vdsn < vovn):
        print "nmos"
        vout = Symbol('vout')
        out = solve((2*KN*((vin - VTO)*vout-((vout**2)/2))*(1+LAMBDA*(vout)))-(KP*((5-VTO)**2)*(1+LAMBDA*(5-vout))),vout)
        print out
    #pmos in triode
    if(vdsp < vovp):
        print "pmos"
        vout = Symbol('vout')
        out = solve((KN*((vin - VTO)**2)*(1+LAMBDA*(vout)))-(2*KP*(5-VTO*5-vout-(((5-vout)**2)/2))*(1+LAMBDA*(5-vout))),vout)
        print out

#calculates output voltage for given input voltage
def output(vin):
    vovn = vin - VTO
    vovp = 5-VTO
    #check if cutoff
    if vin < VTO :
        return cutoff(0,0)
    #assume both in saturation 
    out = (-20*(vin**2-1.4*vin+0.39755))/(vin**2-1.4*vin+0.56396)
    print vin
    #check that asumption was valid
    out = check(out[0],vin)
    print out
    return out

#calculates input voltage for a given output voltage
def input(vout):
    i = pmos(vout)(vout) #pmos current
    #assume saturation
    vin = VTO+(i/(KN*(1+LAMBDA*vout)))**(0.5) 
    #check if triode
    if nmos(vout,vin).__name__ == triodeN:
        vin = (2*KN*(1+LAMBDA*vout)*vout*VTO+2*i+KN*(1+LAMBDA*vout)*vout**2)/(2*KN*(1+LAMBDA*vout)*vout)
    return vin


if __name__ == "__main__":

    #Part a
    for vin in range(0,6,1):
        x,y1,y2 = [],[],[]
        for vout in drange(0,5,.1):
            f1 = nmos(vout,vin)
            f2 = pmos(vout)
            x.append(vout)
            y1.append(f1(vout,vin))
            y2.append(f2(vout))
        #print 'generating plot'
        fig1 = plt.figure()
        plot1 = fig1.add_subplot(111)
        plot1.plot(x,y1, "-b", label='Idn')
        plot1.plot(x,y2, "-g", label='-Idb')
        plot1.legend(loc=5)
        plt.xlabel("Vout")
        plt.ylabel("Idn = -Idp")
        fig1.savefig('HW6-1-{}.pdf'.format(vin))

        fig2 = plt.figure()
        plot2 = fig2.add_subplot(111)
        plot2.plot(x,y2, "-g", label='-Idb')
        plot2.legend(loc=5)
        plt.xlabel("Vout")
        plt.ylabel("Idn = -Idp")
        fig2.savefig('HW6-1-{}-pmos.pdf'.format(vin))

    #part b
    x,y = [],[]
    x.append(5)
    y.append(0)
    for vout in drange(0,5,.1):
        x.append(input(vout))
        y.append(vout)
    x.append(0)
    y.append(5)
    fig = plt.figure()
    plot = fig.add_subplot(111)
    plot.plot(x,y,"-b")
    plt.xlabel("Vin")
    plt.ylabel("Vout")
    fig.savefig('HW6-2.pdf')

    #part d
    f1 = pmos(2.5)
    f2 = nmos(2.5,0.946982)
    print "Id for vout of 2.5V = {}".format(f1(2.5))
    print "m1 is in {}".format(f2.__name__)
    print "and m2 is in {}".format(f1.__name__)

    #part e 
    print "Vin for Vout of 2.5V = {}".format(input(2.5))


