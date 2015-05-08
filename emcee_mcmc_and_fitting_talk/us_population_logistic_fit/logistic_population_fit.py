import numpy as nm
import emcee

def lnprob(params, time, population, ynoise):
	# unpack parameters from array
	L = params[0]
	tau = params[1]
	t0 = params[2]
	# calculate the model for the given parameters
	model = L / (1.0 + nm.exp(-(time - t0)/tau))
	# calculate chi squared
	chi2 = nm.sum(((model - population)*(model - population)) / (ynoise*ynoise))
	# calculate log likelihood and return
	return -0.5*chi2

# load the population data
tmp = nm.loadtxt('us_population_history.txt')
# rescale the data into "millions" to keep things sensible
time = tmp[:,0]
population = tmp[:,1]/1.0e6
# choose a "noise level" to reflect how well we think the model is fitting the data
ynoise = nm.ones_like(population)*5.0

# delete data before 1776 because...murica!
i_good = nm.where(time>1776)[0]
time = time[i_good]
population = population[i_good]
ynoise = ynoise[i_good]


## use emcee to do the fitting
# set up the number of walkers and initialze them
nwalkers = 40
ndim = 3 # it's a three-parameter fit
# choose an initial guess for the parameters
L_guess = 500.0
tau = 50.0
t0 = 2000.0
# scatter around the intial distrubution of walkers 
# near the intial guess
p0 = 10.0*nm.random.rand(ndim * nwalkers).reshape((nwalkers, ndim)) + \
     nm.transpose(nm.vstack((L_guess*nm.ones(nwalkers),tau*nm.ones(nwalkers),t0*nm.ones(nwalkers))))

# use emcee to create the sampler object
sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=[time, population, ynoise])

# run for 300 steps to burn in
pos, prob, state = sampler.run_mcmc(p0, 300)
sampler.reset()

# after the burn in, run 3000 steps
sampler.run_mcmc(pos, 3000)

# calculate the mean parameters and their covariance matrix
mcmc_params = nm.mean(sampler.flatchain,axis=0)
mcmc_params_cov = nm.cov(nm.transpose(sampler.flatchain))

# calculate the model at the mean parameters
# unpack parameters from array
L = mcmc_params[0]
tau = mcmc_params[1]
t0 = mcmc_params[2]
# calculate the model for the given parameters
# generate a more finely spaced time array
# and have it extend into the future
time_array_for_model = nm.arange(1776.0,2300.0,1.0)
model_best = L / (1.0 + nm.exp(-(time_array_for_model - t0)/tau))

# calculate the chi-squared for the best fit
model_best_for_chi2 = L / (1.0 + nm.exp(-(time - t0)/tau))
chi2_best = nm.sum(((model_best_for_chi2 - population)*(model_best_for_chi2 - population)) / (ynoise*ynoise))
# expect this to be roughly the same as the number of data points minus the number of fit parameters
# i.e. should be roughly 21

# plot the data and the best fit
import pylab
pylab.ion()
pylab.figure(2)
pylab.clf()
pylab.plot(time,population,'*',label='Actual US Population Data')
pylab.plot(time_array_for_model,model_best,'k',label='Best-Fit Logistic Model')
pylab.xlabel('Time [CE]')
pylab.ylabel('US Population [millions]')
pylab.legend(loc='upper left')
pylab.title('Logistic Model: Best chi-squared is ' + str(chi2_best))