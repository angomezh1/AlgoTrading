from __future__ import division
from numpy import *
from pylab import *
from numpy.random import rand
import scipy.stats
import  scipy.linalg
from scipy.optimize.lbfgsb import fmin_l_bfgs_b


##########################################################################################################################################################
def historic_vol(currency,tenor):

    #Volatilidad historica estandar
            
    M = currency.shape[0]   #No de dias que tenemos del spot
    
    #Definimos un vector de retornos logaritmicos
    log_return = zeros((M-1,1))

    #Definimos el numero de observaciones moviles a usar dependiendo del plazo
    if tenor == '1W':
        obs = 5
    if tenor == '2W':
        obs = 10
    elif tenor == '1M':
        obs = 21
    elif tenor == '2M':
        obs = 43
    elif tenor == '3M':
        obs = 65
    elif tenor == '6M':
        obs = 129
    elif tenor == '9M':
        obs = 194
    elif tenor == '1Y':
        obs = 260
    elif tenor == '2Y':
        obs = 520

    N = M-obs     #No de retornos que usaremos para calcular la volatilidad. Perdemos el numero obs  
  
    #Calculamos los retornos
    for i in xrange(0,M-1):
        log_return[i] = log(currency[i+1,4])-log(currency[i,4])

    #Definimos una matriz para almacenar los calculos
    calculations = zeros((N,4))

    for i in xrange(0,N):
        calculations[i,0] = log_return[i+obs-1]
        calculations[i,1] = mean(log_return[i:i+obs])
        calculations[i,2] = (calculations[i,0] - calculations[i,1])**2

    for i in xrange(obs-1,N):
        calculations[i,3] = (252**0.5)*(sum(calculations[i-obs+1:i+1,2])/(size(calculations[i-obs+1:i+1,2])-1))**0.5

    #Definicion de un vector con las fechas
    fechas = empty((N,1),dtype =datetime.date)
        
    for i in xrange(obs,M):
        fechas[i-obs] = datetime.date(int(currency[i,0][6:10]), int(currency[i,0][3:5]), int(currency[i,0][0:2]))

    #Definimos una matrix de resultados finales
    vols_standar = zeros((N,2))

    #vols_standar[:,0] = currency[obs:M,0]
    vols_standar[1:N,0] = log_return[obs:M,0]
    vols_standar[:,1] = calculations[:,3]

    #Creacion de la matriz completa
    
    vols_standar=concatenate((fechas,vols_standar),axis=1)
    
    return  vols_standar    

###################################################################################################################################################
def parkinson_vol(currency,tenor):

    #Volatilidad historica estandar
            
    M = currency.shape[0]   #No de dias que tenemos del spot
    
    #Definimos un vector de retornos logaritmicos
    log_return = zeros((M-1,1))

    #Definimos el numero de observaciones moviles a usar dependiendo del plazo
    if tenor == '1W':
        obs = 5
    if tenor == '2W':
        obs = 10
    elif tenor == '1M':
        obs = 21
    elif tenor == '2M':
        obs = 43
    elif tenor == '3M':
        obs = 65
    elif tenor == '6M':
        obs = 129
    elif tenor == '9M':
        obs = 194
    elif tenor == '1Y':
        obs = 260
    elif tenor == '2Y':
        obs = 520

    N = M-obs     #No de retornos que usaremos para calcular la volatilidad. Perdemos el numero obs
    
    #Calculamos los retornos entre maximo y minimo
    for i in xrange(0,M-1):
        log_return[i] = log(currency[i+1,2])-log(currency[i+1,3])

    #Definimos una matriz para almacenar los calculos
    calculations = zeros((N,3))

    for i in xrange(0,N):
        calculations[i,0] = log_return[i+obs-1]        
        calculations[i,1] = (calculations[i,0])**2

    for i in xrange(obs-1,N):
        calculations[i,2] = (252**0.5)*(sum(calculations[i-obs+1:i+1,1])/(4*log(2)*(size(calculations[i-obs+1:i+1,1]))))**0.5

    #Definicion de un vector con las fechas
    fechas = empty((N,1),dtype =datetime.date)
        
    for i in xrange(obs,M):
        fechas[i-obs] = datetime.date(int(currency[i,0][6:10]), int(currency[i,0][3:5]), int(currency[i,0][0:2]))   

    #Definimos una matrix de resultados finales
    vols_parkinson = zeros((N,2))

    #vols_standar[:,0] = currency[obs:M,0]
    vols_parkinson [1:N,0] = log_return[obs:M,0]
    vols_parkinson [:,1] = calculations[:,2]    

    #Creacion de la matriz completa
    
    vols_parkinson=concatenate((fechas,vols_parkinson),axis=1)
    
    
    return  vols_parkinson
###################################################################################################################################################
def garmanklass_vol(currency,tenor):

    #Volatilidad historica estandar
            
    M = currency.shape[0]   #No de dias que tenemos del spot
    
    #Definimos un vector de retornos logaritmicos
    log_return = zeros((M-1,4))

    #Definimos el numero de observaciones moviles a usar dependiendo del plazo
    if tenor == '1W':
        obs = 5
    if tenor == '2W':
        obs = 10
    elif tenor == '1M':
        obs = 21
    elif tenor == '2M':
        obs = 43
    elif tenor == '3M':
        obs = 65
    elif tenor == '6M':
        obs = 129
    elif tenor == '9M':
        obs = 194
    elif tenor == '1Y':
        obs = 260
    elif tenor == '2Y':
        obs = 520

    N = M-obs     #No de retornos que usaremos para calcular la volatilidad. Perdemos el numero obs
    
    #Calculamos los retornos (diferentes medidas)
    for i in xrange(0,M-1):
        log_return[i,0] = log(currency[i+1,2])-log(currency[i+1,3])
        log_return[i,1] = log(currency[i+1,2])-log(currency[i+1,1])
        log_return[i,2] = log(currency[i+1,3])-log(currency[i+1,1])
        log_return[i,3] = log(currency[i+1,4])-log(currency[i+1,1])

    #Definimos una matriz para almacenar los calculos
    calculations = zeros((N,4))

    for i in xrange(0,N):
        calculations[i,0] = (log_return[i+obs-1,0])**2
        calculations[i,1] = log_return[i+obs-1,3]*(log_return[i+obs-1,1]+log_return[i+obs-1,2])-2*log_return[i+obs-1,1]*log_return[i+obs-1,2]
        calculations[i,2] = (log_return[i+obs-1,3])**2

    for i in xrange(obs-1,N):
        calculations[i,3] = (252**0.5)*(0.511*sum(calculations[i-obs+1:i+1,0])/(size(calculations[i-obs+1:i+1,0]))-0.019*sum(calculations[i-obs+1:i+1,1])/(size(calculations[i-obs+1:i+1,1]))-0.383*sum(calculations[i-obs+1:i+1,2])/(size(calculations[i-obs+1:i+1,2])))**0.5  
    
    #Definicion de un vector con las fechas
    fechas = empty((N,1),dtype =datetime.date)
        
    for i in xrange(obs,M):
        fechas[i-obs] = datetime.date(int(currency[i,0][6:10]), int(currency[i,0][3:5]), int(currency[i,0][0:2]))    

    #Definimos una matrix de resultados finales
    vols_garmanklass = zeros((N,2))

    #vols_standar[:,0] = currency[obs:M,0]
    vols_garmanklass [1:N,0] = log_return[obs:M,0]
    vols_garmanklass [:,1] = calculations[:,3]    

    #Creacion de la matriz completa
    
    vols_garmanklass=concatenate((fechas,vols_garmanklass),axis=1)    
    
    return  vols_garmanklass
###################################################################################################################################################
def RS_vol(currency,tenor):

    #Volatilidad historica estandar
            
    M = currency.shape[0]   #No de dias que tenemos del spot
    
    #Definimos un vector de retornos logaritmicos
    log_return = zeros((M-1,4))

    #Definimos el numero de observaciones moviles a usar dependiendo del plazo
    if tenor == '1W':
        obs = 5
    if tenor == '2W':
        obs = 10
    elif tenor == '1M':
        obs = 21
    elif tenor == '2M':
        obs = 43
    elif tenor == '3M':
        obs = 65
    elif tenor == '6M':
        obs = 129
    elif tenor == '9M':
        obs = 194
    elif tenor == '1Y':
        obs = 260
    elif tenor == '2Y':
        obs = 520

    N = M-obs     #No de retornos que usaremos para calcular la volatilidad. Perdemos el numero obs
    
    #Calculamos los retornos (diferentes medidas)
    for i in xrange(0,M-1):
        log_return[i,0] = log(currency[i+1,2])-log(currency[i+1,3])
        log_return[i,1] = log(currency[i+1,2])-log(currency[i+1,1])
        log_return[i,2] = log(currency[i+1,3])-log(currency[i+1,1])
        log_return[i,3] = log(currency[i+1,4])-log(currency[i+1,1])

    #Definimos una matriz para almacenar los calculos
    calculations = zeros((N,2))

    for i in xrange(0,N):        
        calculations[i,0] = log_return[i+obs-1,1]*(log_return[i+obs-1,1]-log_return[i+obs-1,3])+log_return[i+obs-1,2]*(log_return[i+obs-1,2]-log_return[i+obs-1,3])
        
    for i in xrange(obs-1,N):
        calculations[i,1] = (252**0.5)*(sum(calculations[i-obs+1:i+1,0])/((size(calculations[i-obs+1:i+1,0]))))**0.5
    
    #Definicion de un vector con las fechas
    fechas = empty((N,1),dtype =datetime.date)
        
    for i in xrange(obs,M):
        fechas[i-obs] = datetime.date(int(currency[i,0][6:10]), int(currency[i,0][3:5]), int(currency[i,0][0:2]))   

    #Definimos una matrix de resultados finales
    vols_RS = zeros((N,2))

    #vols_standar[:,0] = currency[obs:M,0]
    vols_RS [1:N,0] = log_return[obs:M,0]
    vols_RS [:,1] = calculations[:,1]    

    #Creacion de la matriz completa
    
    vols_RS = concatenate((fechas,vols_RS),axis=1)    
    
    return  vols_RS 
###################################################################################################################################################
def YZ_vol(currency,tenor):

    #Volatilidad historica estandar
            
    M = currency.shape[0]   #No de dias que tenemos del spot
    
    #Definimos un vector de retornos logaritmicos
    log_return = zeros((M-1,6))

    #Definimos el numero de observaciones moviles a usar dependiendo del plazo
    if tenor == '1W':
        obs = 5
    if tenor == '2W':
        obs = 10
    elif tenor == '1M':
        obs = 21
    elif tenor == '2M':
        obs = 43
    elif tenor == '3M':
        obs = 65
    elif tenor == '6M':
        obs = 129
    elif tenor == '9M':
        obs = 194
    elif tenor == '1Y':
        obs = 260
    elif tenor == '2Y':
        obs = 520

    N = M-obs     #No de retornos que usaremos para calcular la volatilidad. Perdemos el numero obs

    k = 0.34/(1+((obs+1)/(obs-1)))
    
    #Calculamos los retornos (diferentes medidas)
    for i in xrange(0,M-1):

        #Estos son para el Rogers-Satchell
        log_return[i,0] = log(currency[i+1,2])-log(currency[i+1,3])
        log_return[i,1] = log(currency[i+1,2])-log(currency[i+1,1])
        log_return[i,2] = log(currency[i+1,3])-log(currency[i+1,1])
        log_return[i,3] = log(currency[i+1,4])-log(currency[i+1,1])

        #Este es para el O
        log_return[i,4] = log(currency[i+1,1])-log(currency[i,4])

        #Este es para el C
        log_return[i,5] = log(currency[i+1,4])-log(currency[i,1])

        
    #Definimos una matriz para almacenar los calculos
    calculations = zeros((N,7))

    for i in xrange(0,N):
        #Este es para RS
        calculations[i,0] = log_return[i+obs-1,1]*(log_return[i+obs-1,1]-log_return[i+obs-1,3])+log_return[i+obs-1,2]*(log_return[i+obs-1,2]-log_return[i+obs-1,3])

        #Este es para O
        calculations[i,1] = (log_return[i+obs-1,4])**2
        
        #Este es para C
        calculations[i,2] = (log_return[i+obs-1,5])**2
        
        
    for i in xrange(obs-1,N):
        calculations[i,3] = sum(calculations[i-obs+1:i+1,0])/((size(calculations[i-obs+1:i+1,0])-1))
        calculations[i,4] = sum(calculations[i-obs+1:i+1,1])/((size(calculations[i-obs+1:i+1,1])-1))
        calculations[i,5] = sum(calculations[i-obs+1:i+1,2])/((size(calculations[i-obs+1:i+1,2])-1))


    for i in xrange(obs-1,N):
        #Calculo de la vol    
        calculations[i,6] = (252**0.5)*(calculations[i,4]+k*calculations[i,5]+(1-k)*calculations[i,3])**0.5
    
    
    #Definicion de un vector con las fechas
    fechas = empty((N,1),dtype =datetime.date)
        
    for i in xrange(obs,M):
        fechas[i-obs] = datetime.date(int(currency[i,0][6:10]), int(currency[i,0][3:5]), int(currency[i,0][0:2])) 

    #Definimos una matrix de resultados finales
    vols_YZ = zeros((N,2))

    #vols_standar[:,0] = currency[obs:M,0]
    vols_YZ [1:N,0] = log_return[obs:M,0]
    vols_YZ [:,1] = calculations[:,6]    

    #Creacion de la matriz completa
    
    vols_YZ = concatenate((fechas,vols_YZ),axis=1)    
    
    return  vols_YZ 
###################################################################################################################################################
def ewma_vol(currency):

    #Volatilidad historica estandar

    currency = COP
           
    M = currency.shape[0]   #No de dias que tenemos del spot
    lamda = 0.94

    #Definimos un vector de retornos logaritmicos
    log_return = zeros((M,1))

    #Calculamos los retornos
    for i in xrange(1,M):
        log_return[i] = log(currency[i,4])-log(currency[i-1,4])

    #Definimos una matriz para almacenar los calculos
    calculations = zeros((M,3))

    for i in xrange(1,M):
        calculations[i,0] = log_return[i]**2
        calculations[i,1] = (lamda*(calculations[i-1,1]**2)+(1-lamda)*calculations[i,0])**0.5
        

    for i in xrange(0,M):
        calculations[i,2] = (252**0.5)*calculations[i,1]

    #Definicion de un vector con las fechas
    fechas = empty((M,1),dtype =datetime.date)
        
    for i in xrange(0,M):
        fechas[i] = datetime.date(int(currency[i,0][6:10]), int(currency[i,0][3:5]), int(currency[i,0][0:2]))

    #Definimos una matrix de resultados finales
    vols_ewma = zeros((M,2))

    #vols_standar[:,0] = currency[obs:M,0]
    vols_ewma[0:M,0] = log_return[0:M,0]
    vols_ewma[:,1] = calculations[0:M,2]

    #Creacion de la matriz completa

    vols_ewma = concatenate((fechas,vols_ewma),axis=1)
    
    return vols_ewma  

###################################################################################################################################################

def loglik(x):    
    
    alfa0 = x[0]
    alfa1 = x[1]
    beta0 = x[2]

    returns = genfromtxt('HistoricalOvernightRates.csv',delimiter=',')
    rates=rates[:,1]/100
    factor1 = exp(-kappa*delta_t)*rates
    factor2 = theta*(1-exp(-kappa*delta_t))
    factor3=(1-exp(-2*kappa*delta_t))/(2*kappa)

    rates=delete(rates,0)
    factor1=delete(factor1,factor1.size-1)
    N = rates.size
    variance = (sigma**2)*factor3

    summand = (rates-factor1-factor2)**2

    loglikelihood = -0.5*N*log(2*pi)-0.5*N*log(variance)-0.5*(1/variance)*sum(summand)

    negative_LogL = -loglikelihood

    return negative_LogL

###################################################################################################################################################

def historic_skew(currency,tenor):

    
    vols = historic_vol(currency,tenor)
    vols[:,2]=vols[:,2]/(252)**0.5
    
    #Skew historico
            
    M = currency.shape[0]   #No de dias que tenemos del spot
    
    #Definimos un vector de retornos logaritmicos
    log_return = zeros((M-1,1))

    #Definimos el numero de observaciones moviles a usar dependiendo del plazo
    if tenor == '1W':
        obs = 5
    if tenor == '2W':
        obs = 10
    elif tenor == '1M':
        obs = 21
    elif tenor == '2M':
        obs = 43
    elif tenor == '3M':
        obs = 65
    elif tenor == '6M':
        obs = 129
    elif tenor == '9M':
        obs = 194
    elif tenor == '1Y':
        obs = 260
    elif tenor == '2Y':
        obs = 520

    N = M-obs     #No de retornos que usaremos para calcular la volatilidad. Perdemos el numero obs  
  
    #Calculamos los retornos
    for i in xrange(0,M-1):
        log_return[i] = log(currency[i+1,4])-log(currency[i,4])

    #Definimos una matriz para almacenar los calculos
    calculations = zeros((N,3))

    for i in xrange(0,N):
        calculations[i,0] = log_return[i+obs-1]        
        calculations[i,1] = (calculations[i,0] - calculations[i,1])**3

    for i in xrange(obs-1,N):
        calculations[i,2] = sum(calculations[i-obs+1:i+1,1])/size(calculations[i-obs+1:i+1,1])

    #Definicion de un vector con las fechas
    fechas = empty((N,1),dtype =datetime.date)
        
    for i in xrange(obs,M):
        fechas[i-obs] = datetime.date(int(currency[i,0][6:10]), int(currency[i,0][3:5]), int(currency[i,0][0:2]))

    #Definimos una matrix de resultados finales
    skews_standar = zeros((N,1))

    #vols_standar[:,0] = currency[obs:M,0]    
    skews_standar[:,0] = calculations[:,2]

    #Creacion de la matriz completa
    
    skews_standar=concatenate((fechas,skews_standar),axis=1)

    for i in xrange(0,N):
        if vols[i,2]==0:
            skews_standar[i,1] = 0
        else:
            skews_standar[i,1] = skews_standar[i,1]/((obs**0.5)*(vols[i,2]**3))
    
    return  skews_standar    
