# Sean Bryan
# sean.a.bryan@asu.edu
# 5/3/2015

import numpy as nm
import pylab

##### make some fake data
xdat = nm.array([1.0,2.0,3.0,4.0,5.0,6.0])

actual_m = 2.1
actual_b = 1.3
realparams = nm.array([actual_b,actual_m])

noiselevel = 0.5
ynoise = nm.ones(len(xdat))*noiselevel

ydat = actual_m*xdat + actual_b + nm.random.randn(len(xdat))*noiselevel
#####

# plot each step as its taken, and stop to have a look
plotting_progress=True
num_to_skip = 1 # 1 = don't skip any, bigger than 1 (i.e. 20 or 200) means skip
if plotting_progress:
    pylab.figure(1,figsize=(14,5))
    pylab.clf()
    pylab.ion()
    pylab.show()

## make a (bad) guess at the actual parameters
guess_m = -1.0
guess_b = -1.0
## better guess
#guess_m = 2.0
#guess_b = 1.2
# choose a stepsize
stepsize = nm.array([0.1,0.1])
# choose how many steps we will take
nsteps = 10000



ndim = 2 # it's a two parameter fit



# set up the array storing the entire chain of steps through parameter space
# (initialize it with NaN as placeholders)
params = nm.zeros((nsteps,ndim)) + nm.nan
params[0,0] = guess_m
params[0,1] = guess_b
# set up the array to store the likelihood at each step
logp_stored = nm.zeros(nsteps) + nm.nan



# define the likelihood function
def logp(params, xdat, ydat, ynoise):
    # unpack the params array
    m = params[0]
    b = params[1]

    # calculate the model here
    model = m*xdat + b

    # calculate chi squared
    chi2 = nm.sum(((model - ydat)*(model - ydat)) / (ynoise*ynoise))

    # calculate log likelihood and return
    return -0.5*chi2


# count how many steps were rejected
n_rejects = 0


# calculate log likelihood at x_1 to start
logp_xi = logp(params[0,:], xdat, ydat, ynoise)
# main loop
for i in xrange(nsteps):    
    # store probability value for this step in the chain
    logp_stored[i] = logp_xi

    # generate candidate step
    y = nm.random.randn(len(params[0,:]))*stepsize

    # try the move
    z = params[i,:] + y

    # find the likelihood at the move
    logp_z = logp(z, xdat, ydat, ynoise)
    # ...and use that likelihood to
    # calculate the probability that we'll accept the step
    alpha = nm.exp(logp_z - logp_xi) # = p_z/p_xi

    # decide whether or not to make the move
    # (if likelihood is improved, then always move)
    # (if p(z) = 0, then never move)
    if nm.random.rand() < alpha:
        # make move to accepted step
        params[i+1,:] = z

        # calculate log likelihood at accepted step
        logp_xi = logp_z
    else :
        # reject the point and count it
        n_rejects = n_rejects + 1
        
        # stay at the previous point
        params[i+1,:] = params[i,:]

        # logp_xi stays the same

    if plotting_progress:
        if not(nm.mod(i,num_to_skip)):
            pylab.clf()
            pylab.subplot(1,3,1)
            pylab.plot(params[:,0],params[:,1],'b',label='Chain')
            pylab.plot(actual_m,actual_b,'k*',label='True Parameter Values')
            pylab.legend()
            pylab.xlabel('m')
            pylab.ylabel('b')
            pylab.title('Parameter Space')
            pylab.subplot(1,3,2)
            pylab.plot(logp_stored)
            pylab.xlabel('steps')
            pylab.title('Log Likelihood')
            pylab.subplot(1,3,3)
            pylab.errorbar(xdat,ydat,yerr=ynoise,linestyle='*',label='Data')
            pylab.plot(xdat,params[i,0]*xdat + params[i,1],'k',label='Model At This Step')
            pylab.legend()
            pylab.title('i = ' + str(i) + ' so far ' + str(n_rejects) + ' rejected')

            raw_input('Press Enter to Take Next Step')


# store last log likelihood
logp_stored[n-1] = logp_xi

# calculate the step rejection rate
rejection_rate = float(n_rejects) / float(n)