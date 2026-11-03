"""
Práctica 3: Modelado y control del sistema musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Emiliano Gómez Quiroa
Número de control: 23212196
Correo institucional: l23212196@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h=0,0,10,1E-3,7,3.5
N=round(tend/dt)+1 #numero de iteraciones para la funcion de tranferencia
t=np.linspace(t0,tend,N) #arreglo del tiempo

u2=np.ones(N) #Step
u1=np.zeros(N); u1[round(1/dt):round(2/dt)]=1
u3=t/tend #rampa
u4=np.sin(m.pi/2*t)
u=np.column_stack((u1,u2,u3,u4))

signals=["Step","Impulse","Ramp","Sinusoidal"]

# Componentes del circuito RLC y función de transferencia
#Control
num=[100*10E-6,1-.25]
den=[100*(100E-6+10E-6),1]
sys=ctrl.tf(num,den)
print(f"Función de tranferencia: {sys}\n")

#Caso:
num2=[10E3*10E-6,1-.25]
den2=[10E3*(100E-6+10E-6),1]
sys2=ctrl.tf(num2,den2)
print(f"Función de tranferencia: {sys2}\n")

# Polos del sistema
#L=np.roots(den)
#print(f"Polos del sistema: L1={L[0]:.3e}, L2={L[1]:.3e}\n")

# Componentes del controlador
kP=0.019136
kI=47422.9366
Cr=1E-6
Re=1/(Cr*kI)
Rr=kP*Re

numPID=[Rr*Cr,1]
denPID=[Re*Cr,0]
PID=ctrl.tf(numPID,denPID)
print(f"El valor de la capacitancia Cr es de {Cr} Faradios.\n")
print(f"El valor de la capacitancia Re es de {Re} Ohms.\n")
print(f"El valor de la capacitancia Rr es de {Rr} Ohms.\n")

print(f"Funcion de transferencia del controlador PID: {PID}.\n")

# Sistema de control en lazo cerrado
sysPID=ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
print(f"Función de transferencia del sistema de control de lazo cerrado: {sysPID}")

# Colores
clr1=np.array([255,0,0])/255
clr2=np.array([0,255,0])/255
clr3=np.array([0,0,255])/255
clr4=np.array([0, 0, 0])/255

# Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t,sys,u):
    _,PAu=ctrl.forced_response(sys,t,u,x0)
    return PAu

def closedloop(t,sysPID,u):
    _,PIDu=ctrl.forced_response(sysPID,t,u,x0)
    return PIDu


# Respuesta del sistema en lazo abierto y en lazo cerrado
for i in range(0,1):
    control=openloop(t,sys,u[:,i])
    caso=openloop(t,sys2,control)

    PID=closedloop(t,sysPID,control)

    fg=plt.figure(i+1)
    fg.set_size_inches(w,h)
    plt.rcParams['font.size']=11
    plt.rcParams['font.family']='serif'
    plt.rcParams['font.serif']=['Times New Roman']

    plt.plot(t,u[:,i],'-',color=clr1,label='F(t)')
    plt.plot(t,control,'--',color=clr2,label='Fs(t): Control')
    plt.plot(t,caso,'--',color=clr3,label='Fs(t): Caso')
    
    plt.plot(t,PID,':',linewidth=2.5,color=clr4,label='PID(t): Tratamiento')
    plt.xlim(0,10);plt.xticks(np.arange(0,11,1))
    plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.2,0.1))
   

    plt.xlabel('t [S]')
    plt.ylabel('V(t) [V]')
    plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
    plt.show()
    fg.savefig(signals[i]+'_python.pdf',bbox_inches='tight')