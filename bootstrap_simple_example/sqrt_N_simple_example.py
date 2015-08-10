import numpy as nm

# say we did an experiment and took 50 data points
# this was our entire experiment, like, it cost a million dollars
# and we're going to write a paper about it with an abstract

# what should we say our experiment measured?
# imagining that it were possible to repeat the experiment zillions of times,
# (it's not possible because it cost a million)
# how typical is the result we happened to get with the 50 data points we saw?

# if only it were this easy...
number_of_data_points = 50
actual_standard_deviation = 0.5
actual_mean = 3.0
real_data_for_paper = nm.random.randn(number_of_data_points)*actual_standard_deviation + actual_mean
print 'Entire Dataset:'
print real_data_for_paper


# ok, we've got one set of 50 data points, at a cost of 1 million dollars
# for the paper, we look in the following book to write the abstact:
# Bevington and Robinson, Data Reduction and Error Analysis for the Physical Sciences
# First, simulate analyzing the data for the abstract of the paper
mean_for_abstract = nm.mean(real_data_for_paper)
# that was pretty easy, but how "typical" is this result if we had been able to repeat
# the million-dollar experiment? B&R Page 71 says:
error_on_the_mean_for_abstract_from_formula = nm.std(real_data_for_paper) / nm.sqrt(len(real_data_for_paper))

# let's print this out and have a look
print ' '
print 'The mean and error-on-the-mean is:'
print str(mean_for_abstract) + ' +/- ' + str(error_on_the_mean_for_abstract_from_formula)
print ' '
print 'Or, rounding digits properly: '
print str(round(mean_for_abstract,3)) + ' +/- ' + str(round(error_on_the_mean_for_abstract_from_formula,3))
# (note, rounding should keep trailing zeros, and the "round" function doesn't...i.e. you should write 3.042 +/- 0.060)

# ok...that formula is slightly magic, although less magic than if you read the book carefully
# still, what if our data isn't gaussian?
# what if we apply some sophisticated analysis pipeline instead of just "numpy.mean" to the data?
# we can't afford to repeat the million-dollar experiment,
# but we can afford to simulate in software what it might be like to repeat the experiment
# this is called a "monte carlo simulation" because we generate random numbers...just like in a casino, like in monte carlo
# let's do that! let's repeat this million-dollar experiment in software 5000 times, and see how often we get certain mean values
times_to_repeat_experiment = 5000
simulated_experiment_outcomes = nm.zeros(times_to_repeat_experiment)
for i in xrange(times_to_repeat_experiment):
	# simulate new data
	simulated_data = nm.random.randn(number_of_data_points)*actual_standard_deviation + actual_mean
	# take the mean this time, and store it
	simulated_experiment_outcomes[i] = nm.mean(simulated_data)

# now we have an array, simulated_experiment_outcomes,
# where each element of the array is the number in the abstract of a paper resulting from doing the entire experiment
# (or, at least a simulation of doing that)
# what we can now do is ask directly, what is the typical spread of values of the number in the abstract?
monte_carlo_error_on_the_mean = nm.std(simulated_experiment_outcomes)
# we can even look at a histogram, and see visually how typical our real million-dollar experiment is
import pylab
pylab.figure(1)
pylab.clf()
pylab.hist(simulated_experiment_outcomes,50,label='Histogram from Monte Carlo')
pylab.xlabel('Value in the Abstract')
pylab.ylabel('# of Times it Came Out That Way')
# draw a line showing our million-dollar experiment result
pylab.plot([mean_for_abstract,mean_for_abstract],[0,350],'r',linewidth=10,label='Value in Abstract from Expensive Experiment')
pylab.plot([mean_for_abstract-error_on_the_mean_for_abstract_from_formula,mean_for_abstract+error_on_the_mean_for_abstract_from_formula],[175,175],'g',linewidth=10,label='Error from Formula')
pylab.legend()
pylab.ylim([0,475])
pylab.ion()
pylab.show()