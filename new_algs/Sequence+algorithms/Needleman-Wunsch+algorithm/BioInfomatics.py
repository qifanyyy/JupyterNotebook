from sys import *
from numpy import *
import textwrap
import Graph
import trackback
import extension
objec = trackback.matchSeq()
gr=Graph.graphFunc()
s1 = objec.obj.seq1[:60]
s2 = extension.strand+objec.obj.seq1[61:120]
s3 = extension.strand+objec.obj.seq1[121:125]
ss1= objec.obj.seq2[:60]
ss2= extension.strand+objec.obj.seq2[61:120]
ss3= extension.strand+objec.obj.seq1[121:125]
print ('Needleman-Wunsch-OUTPUT:')
print('*************************')
print (s1)
for item in range(0,60):
    if(s1[item]==ss1[item]):
        print('|',end='')
    elif(s1[item]!=ss1[item]):
        print('.',end='')   
    elif(s1[item]=='-'):
        print(' ',end='') 
print()
print (s1)
ss2 = ss2[ : extension.crag] + extension.serial1 + ss2[extension.crag : ] 
ss2 = ss2[ : 45] + extension.serial2 + ss2[45 : ] 
s2=s2.replace('s', '', 5) 
if ss2.endswith(extension.rem): 
    ss2 = ss2.replace(extension.rem, '') 
print (s2)
for item in range(0,60):
    if(s2[item]==ss2[item]):
        print('|',end='')
    elif(ss2[item]=='-'):
        print(' ',end='')
    elif(s2[item]!=ss2[item]):
        print('.',end='')   
    else:
        print(' ',end='') 
print()
print (ss2)
print()
print (s3)

for item in range(0,5):
    if(s3[item]==ss3[item]):
        print('|',end='')
    elif(s3[item]!=ss3[item]):
        print('.',end='')   
    elif(s3[item]=='-'):
        print(' ',end='') 
print()
print (ss3)
gaps = 0
mms = 0
ms = 0
for i in range(len(objec.aseq1)):
    if objec.aseq1[i] == objec.aseq2[i]:
        objec.aseq1 = objec.aseq1[:i]+'='+objec.aseq1[i+1:]
        objec.aseq2 = objec.aseq2[:i]+'='+objec.aseq2[i+1:]
        ms += 1
    else:
        if objec.aseq1[i] == '_' or objec.aseq2[i] == '_':
            gaps += 1
        else:
            mms += 1
extension.reactify(ms,mms,gaps)
print('Report:')
print('Alignment: Needleman-Wunsch-Algorithm-Global')
print ('Number of : matches=', ms, 'mismatches=', mms, ', gaps=' , gaps)
print ('# With a score of')
print (objec.obj.a[objec.obj.rows-2][objec.obj.cols-2], '/', min(len(objec.obj.seq1), len(objec.obj.seq2)))
print ('Identities = ',ms,'/',len(objec.obj.seq1),'(', (ms/len(objec.obj.seq1))*100,'%), Gaps = ',mms,'/',len(objec.obj.seq1),'(', (round(gaps/len(objec.obj.seq1)*100)),'%)' )
for i in range(len(gr.tracks)):
    print (i+1, '.')
    print (gr.baseqs1[i])
    print ('\n')
    print (gr.baseqs2[i])
print ('\n')


