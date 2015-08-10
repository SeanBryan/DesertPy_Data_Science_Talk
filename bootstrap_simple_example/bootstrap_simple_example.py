import numpy as nm

# read the wikipedia page https://en.wikipedia.org/wiki/Bootstrapping_(statistics) 
# also, I haven't used it, but see scikits.bootstrap https://github.com/cgevans/scikits-bootstrap

# function inspired by http://nbviewer.ipython.org/gist/aflaxman/6871948
def bootstrap_resample(data, num_realizations):
    """ Bootstrap resample an array
    Parameters
    ----------
    data : array_like
      data to resample
    num_realizations : int, optional
      number of times to resample and take the mean
    Results
    -------
    returns array_of_resampled_means
    """
    # declare a data array to store the final results
    mean_resampled = nm.zeros(num_realizations)

    for i in xrange(num_realizations):
        # generate an array of random integers (ranging from 1 to N, where N is the length of the data array)
        resample_i = nm.floor(nm.random.rand(len(data))*len(data)).astype(int)
        # use that array of integers to resample the original data array
        # (some data points will be chosen more than once, others skipped, the order will be random
        #  ...it's ok, that's the whole point of the algorithm to generate something that's a little array like
        #  as if you had repeated the entire data collection process)
        data_resampled_i = data[resample_i]
        # now that we've got something like a data array from repeating the experiment, take the mean
        mean_resampled[i] = nm.mean(data_resampled_i)

    return mean_resampled

# in the sqrt-N example, we made two common assumptions that are actually valid a lot of the time,
# and nearly-valid I would say almost all of the time! so, that's why we went through it
# still, sometimes those two assumptions are wrong
# sometimes the data set is not distributed according to a gaussian
# or, even if it were, sometimes you just aren't certain _what_ kind of distribution it is

# so, in those cases, one way to proceed is with bootstrapping
# there, instead of monte carlo simulating your entire experiment end-to-end
# (since you can't do that, since you aren't certain what distribution to use for your simulation)
# you take your single expensive dataset and shuffle it in a certain prescribed way to "emulate" repeating the experiment

# so, let's do the same as in the sqrt-N example, but this time do the resampling with the bootstrap method instead

# if only it were this easy...
number_of_data_points = 50
actual_standard_deviation = 0.5
actual_mean = 3.0
real_data_for_paper = nm.random.randn(number_of_data_points)*actual_standard_deviation + actual_mean
print 'Entire Dataset:'
print real_data_for_paper

# instead of 5000 monte carlo simulations, let's get 5000 bootstrap resamples
bootstrap_simulated_experiment_outcomes = bootstrap_resample(real_data_for_paper, 5000)

# now, as before let's print this out
mean_for_abstract = nm.mean(real_data_for_paper)
print ' '
print 'The mean and error-on-the-mean from the bootstrap method is:'
print str(mean_for_abstract) + ' +/- ' + str(error_on_the_mean_for_abstract_from_bootstrap)
print ' '
print 'Or, rounding digits properly: '
print str(round(mean_for_abstract,3)) + ' +/- ' + str(round(error_on_the_mean_for_abstract_from_bootstrap,3))
# (note, rounding should keep trailing zeros, and the "round" function doesn't...i.e. you should write 3.042 +/- 0.060)

# and make the same plot as before
error_on_the_mean_for_abstract_from_formula = nm.std(real_data_for_paper) / nm.sqrt(len(real_data_for_paper))
import pylab
pylab.figure(2)
pylab.clf()
pylab.hist(bootstrap_simulated_experiment_outcomes,50,label='Histogram from Bootstrap')
pylab.xlabel('Value in the Abstract')
pylab.ylabel('# of Times it Came Out That Way')
# draw a line showing our million-dollar experiment result
pylab.plot([mean_for_abstract,mean_for_abstract],[0,350],'r',linewidth=10,label='Value in Abstract from Expensive Experiment')
pylab.plot([mean_for_abstract-error_on_the_mean_for_abstract_from_formula,mean_for_abstract+error_on_the_mean_for_abstract_from_formula],[175,175],'g',linewidth=10,label='Error from Formula')
pylab.legend()
pylab.ylim([0,475])
pylab.ion()
pylab.show()
