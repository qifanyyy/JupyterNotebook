import pysplinekernel
import numpy
import matplotlib.pyplot as plt

n = 101;

U1 = [0.0, 0.0, 0.25, 0.5, 0.75, 1.0, 1.0]
U2 = [0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0]
U3 = [0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 1.0]
U4 = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0]

t = numpy.linspace( 0.0, 1.0, n )

P = [ [ 1.5, 2.0, 2.5, 1.0, 1.0 ],
      [ 1.0, 0.5, 2.0, 2.5, 0.5 ] ];

xc1, yc1 = pysplinekernel.evaluate2DCurveDeBoor( t, P[0], P[1], U1 )
xc2, yc2 = pysplinekernel.evaluate2DCurveDeBoor( t, P[0], P[1], U2 )
xc3, yc3 = pysplinekernel.evaluate2DCurveDeBoor( t, P[0], P[1], U3 )
xc4, yc4 = pysplinekernel.evaluate2DCurveDeBoor( t, P[0], P[1], U4 )

plt.plot( xc1, yc1, label='p = 1' )
plt.plot( xc2, yc2, label='p = 2' )
plt.plot( xc3, yc3, label='p = 3' )
plt.plot( xc4, yc4, label='p = 4' )

plt.plot( P[0], P[1], 'rx')

plt.legend()

plt.show( )
