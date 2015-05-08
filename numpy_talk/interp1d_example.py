import numpy as nm
import scipy
import scipy.interpolate

# Sean Bryan
# sean.a.bryan@asu.edu
# 9/5/2014

# (note, go to line 40 if you want to change what type of interpolation we are using)

# create sparsely sampled data points
# they need not be sampled uniformly
time    = nm.array([0.0,0.5,1.0,1.5,2.3,4.0,4.5,6.2])
voltage = nm.array([2.6,3.2,5.7,4.3,3.7,6.1,7.2,4.8])

# plot the data to take a look
import pylab
pylab.figure(1)
pylab.clf()
pylab.plot(time,voltage,'*',markersize=15,label='Sparse Data Points')

# interpolate the time-voltage data
# to create a finely sampled array

# first, create the finely sampled time array
finely_spaced_time_array = nm.arange(0.0,6.2,0.001)

# then, use the interp1d function of scipy
# to create a function "interpolating_function"
# that we can use later to do the interpolation
#
# kind can be:
# 'linear', 'nearest', 'zero',
# 'slinear' 'quadratic', and 'cubic' refer to a spline interpolation of first, second, or third order
#
# 'linear', 'nearest', and 'cubic' are my personal favorites, probably in that order!
#
# (note that splines are named after pieces of flexible wood that were used in drafting...did you know that?)
# (http://en.wikipedia.org/wiki/Technical_drawing_tools#Templates)
kind_we_are_using = 'cubic'
interpolating_function = scipy.interpolate.interp1d(time,voltage,kind=kind_we_are_using)

# now, call this interpolating function on our finely sampled array
# to actually create the interpolated values
interpolated_voltages_array = interpolating_function(finely_spaced_time_array)

# add the interpolated curve to the plot
pylab.plot(finely_spaced_time_array,interpolated_voltages_array,label='Interpolated Finely-sampled Points\nusing ' + kind_we_are_using + ' interpolation')

# make axis labels and add a legend
pylab.xlabel('Time [s]')
pylab.ylabel('Voltage')
pylab.legend(loc='lower right')

pylab.ion()
pylab.show()