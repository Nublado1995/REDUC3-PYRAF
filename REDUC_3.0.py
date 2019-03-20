#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 21:53:07 2018
Finished on Mon Apr 16 01:45:00 2018 (Practicamente hecho hoy)

CORRECCION: ES NECESARIO REVISAR LA PARTE DE RECORTAR LA IMAGENES.

@author: Fabricio 
"""

from pyraf import iraf
from pyraf.iraf import noao, imred, ccdred
import glob
i=iraf
print('Cargado...')
#Reduccion BIAS
lfile=glob.glob('B*.fits')

for ifile in lfile:
    i.noao.imred.ccdred.zerocombine(ifile, output='ZERO-none.fits', reject='none')
    i.noao.imred.ccdred.zerocombine(ifile, output='ZERO-sigclip.fits', reject='sigclip')
    i.noao.imred.ccdred.zerocombine(ifile, output='ZERO-avsigclip.fits', reject='avsigclip')
    
print('BIAS hechos...') #Para evitar posibles errores no añadir '-' en los prefijos o sufijos.
#Reduccion FLATS
flatlist=glob.glob('F*.fits')

for iflat in flatlist:
    i.imarith(operand1=iflat, op ='-' , operand2 ='ZERO-none.fits[1]', result='b' +iflat )

print('FLATS limpios...')

#Sacar BIAS a las imagenes.

listobj=glob.glob('O*.fits')

for iobj in listobj:
    i.imarith(operand1= iobj, op='-', operand2='ZERO-none.fits[1]', result='b' + iobj)

print('imagenes sin BIAS...')

#Recortar imagenes.

bflatlist=glob.glob('bF*.fits') #CREO QUE ESTO NO FUNCIONA.
blistobj=glob.glob('bO*.fits')

for ibflat in bflatlist:
    i.imcopy( input=ibflat +'[1]'+'[120:496,202:410]', output='c' + ibflat)
    
for ibobj in blistobj:
    i.imcopy(input=ibobj+'[1]'+'[120:496,202:410]', output='c' + ibobj)
    
print('Imagenes recortadas...')

#Seleccionar imagenes por filtros.

cbflatlist=glob.glob('cbF*.fits')
cblistobj=glob.glob('cO*.fits')

#Es importando indicar Stdout=1
#No entiendo porque ahora puedo emplear 'archivo*.fits', pero al principio 
#daba error.
LFLATV=i.hselect('cbF*.fits[1]', "$I", "INSFILTE?='V'", Stdout = 1)
ff = open('flatsV.txt', 'w')
ff.write('\n'.join(LFLATV)+ "\n")
ff.close()
LFLATB=i.hselect('cbF*.fits[1]', "$I", "INSFILTE?='B'", Stdout = 1)
ff = open('flatsB.txt', 'w')
ff.write('\n'.join(LFLATB)+ "\n")
ff.close()
LFLATR=i.hselect('cbF*.fits[1]', "$I", "INSFILTE?='R'", Stdout = 1)
ff = open('flatsR.txt', 'w')
ff.write('\n'.join(LFLATR)+ "\n")
LFLATU=i.hselect('cbF*.fits[1]', "$I", "INSFILTE?='U'", Stdout = 1)
ff = open('flatsU.txt', 'w')
ff.write('\n'.join(LFLATU)+ "\n")
LFLATI=i.hselect('cbF*.fits[1]', "$I", "INSFILTE?='I'", Stdout = 1)
ff = open('flatsI.txt', 'w')
ff.write('\n'.join(LFLATI)+ "\n")
ff.close()
LOBJV=i.hselect('cbO*.fits[1]', "$I", "INSFILTE?='V'", Stdout = 1)
ff = open('objV.txt', 'w')
ff.write('\n'.join(LOBJV)+ "\n")
ff.close()
LOBJB=i.hselect('cbO*.fits[1]', "$I", "INSFILTE?='B'", Stdout = 1)
ff = open('objB.txt', 'w')
ff.write('\n'.join(LOBJB)+ "\n")
ff.close()
LOBJR=i.hselect('cbO*.fits[1]', "$I", "INSFILTE?='R'", Stdout = 1)
ff = open('objR.txt', 'w')
ff.write('\n'.join(LOBJR)+ "\n")
ff.close()
LOBJU=i.hselect('cbO*.fits[1]', "$I", "INSFILTE?='U'", Stdout = 1)
ff = open('objU.txt', 'w')
ff.write('\n'.join(LOBJU)+ "\n")
ff.close()
LOBJI=i.hselect('cbO*.fits[1]', "$I", "INSFILTE?='I'", Stdout = 1)
ff = open('objI.txt', 'w')
ff.write('\n'.join(LOBJI)+ "\n")
ff.close()
    
print('Imagenes clasificadas por filtros...')

#Combinar FLATS.
#preflatV=glob.glob('V*.fits')
#preflatB=glob.glob('B*.fits')
#preflatR=glob.glob('R*.fits')

#for iFLATV in LFLATV:
i.imcombine('@flatsV.txt', output='VFLATFIELD.fits', reject='none')

#for iFLATB in LFLATB:
i.imcombine('@flatsB.txt', output='BFLATFIELD.fits', reject='none')

#for iFLATR in LFLATR:
i.imcombine('@flatsR.txt', output='RFLATFIELD.fits', reject='none')
i.imcombine('@flatsU.txt', output='UFLATFIELD.fits', reject='none')
i.imcombine('@flatsI.txt', output='IFLATFIELD.fits', reject='none')

print('FLATS combinados...')

#Normalizar FLATS

print('DATOS DEL FLAT DE V:')
i.imstat('VFLATFIELD.fits[1]')
print('DATOS DEL FLAT DE B:')
i.imstat('BFLATFIELD.fits[1]')
print('DATOS DEL FLAT DE R:')
i.imstat('RFLATFIELD.fits[1]')
print('DATOS DEL FLAT DE U:')
i.imstat('UFLATFIELD.fits[1]')
print('DATOS DEL FLAT DE I:')
i.imstat('IFLATFIELD.fits[1]')

meanV=input('El valor medio del FLAT en V:')
meanB=input('El valor medio del FLAT en B:')
meanR=input('El valor medio del FLAT en R:')
meanU=input('El valor medio del FLAT en U:')
meanI=input('El valor medio del FLAT en I:')

i.imarith(operand1='VFLATFIELD.fits[1]', op='/', operand2=meanV, result='normVFLATFIELD.fits')
i.imarith(operand1='BFLATFIELD.fits[1]', op='/', operand2=meanB, result='normBFLATFIELD.fits')
i.imarith(operand1='RFLATFIELD.fits[1]', op='/', operand2=meanR, result='normRFLATFIELD.fits')
i.imarith(operand1='UFLATFIELD.fits[1]', op='/', operand2=meanU, result='normUFLATFIELD.fits')
i.imarith(operand1='IFLATFIELD.fits[1]', op='/', operand2=meanI, result='normIFLATFIELD.fits')
#Cuando el operand no es un archivo, no poner ''.
print ('FLATS normalizados...')

#Normalizar imagenes de los objetos.
i.imarith(operand1='@objV.txt', op='/', operand2='normVFLATFIELD.fits[1]', result='norm'+'@objV.txt' )

i.imarith(operand1='@objB.txt', op='/', operand2='normBFLATFIELD.fits[1]', result='norm'+'@objB.txt' )

i.imarith(operand1='@objR.txt', op='/', operand2='normRFLATFIELD.fits[1]', result='norm'+'@objR.txt' )

i.imarith(operand1='@objU.txt', op='/', operand2='normUFLATFIELD.fits[1]', result='norm'+'@objU.txt' )

i.imarith(operand1='@objI.txt', op='/', operand2='normIFLATFIELD.fits[1]', result='norm'+'@objI.txt' )

print('Imagenes normalizadas') 

 


