# Sean Bryan
# sean.a.bryan@asu.edu
# 5/3/2015

# numpy outline
import numpy as nm # ok...everyone else does np, but..."py" is such a common package ending...anyway...



# making arrays one element at a time with a list
x = nm.array([10.0,17.0,3.4,7.6,9.5,11.2])



# indexing a 1d array
# say we want the second through fourth elements
x[1:4] # note that this is starting at zero, and only goes to 4-1...i.e. it gives us elements 1,2,3 (which is second through fourth)
# ...
# counting is hard! :)
# also note that "-1" means "end of the array - 1"
# "-2" would be "end-2" so...yeah.
# negative indexing...ftw
x[2:-1]



# adding, subtracting, multiplying, dividing
[10.0,17.0,3.4,7.6,9.5,11.2] + 2.3 # fail, because lists can't do that
x + 2.3 # works
x - 23.4
x * 2.0
x / 7.3



# adding, subtracting, multiplying, dividing arrays elementwise
y = nm.array([11.0,6.3,5.1,12.3,9.0,15.2])

[10.0,17.0,3.4,7.6,9.5,11.2] * [11.0,6.3,5.1,12.3,9.0,15.2] # fail, because lists can't do that

x * y # works

# this means, often, you can "magically" put numpy arrays into
# a calculation that you thought you were only writing to handle
# numbers

z = nm.array([3.4,5.2])

x + z # fail...the array shapes don't match
      # or...somewhat cryptically: "ValueError: operands could not be broadcast together with shapes (6,) (2,)"




# making 2d arrays one element at a time
x_2d = nm.array([[3.5,7.2,1.2,5.3],[9.2,0.2,1.2,5.2]])



# nm.where in the 2d case
list_of_index_arrays = nm.where(x_2d>2.0)
x_2d[list_of_index_arrays]



# nm.where in the (more common? less obvious?) 1d case
list_of_index_arrays_1d = nm.where(x>5.0)
x[list_of_index_arrays_1d] # ok...indexing still works...



# let's look at the list of index arrays itself
list_of_index_arrays_1d
# say we were interested in just the first two instances of x less than 5
# let's just index this
list_of_index_arrays_1d[0:2] # fail, kind of...because it's a list...with one element...where that element is an array...argh, subtle
# ok, just nab the first element of the one-element list
index_array = list_of_index_arrays_1d[0]
# now we can get this easily
index_array[0:2]



# nm.loadtxt on us population data
data_as_2d_array = nm.loadtxt('us_population_logistic_fit/us_population_history.txt')
data_as_2d_array.shape
# looking at the file, the first column is the year and the second is the population
# let's burn some more cpu cycles, and create some new arrays
time = data_as_2d_array[:,0] # note that the ':' just means 'go through the whole thing'
population = data_as_2d_array[:,1]

# pylab.plot population vs time
# so...this isn't numpy...but...
# when you're working with arrays you're going to need to plot them
# technically this will be matplotlib, but...pylab is a superset of matplotlib
import pylab as pl
pl.ion() # this turns interactive-mode on, otherwise plotting will take over the terminal...can show this
         # this also automatically "shows" any subsequent plots that are made
         # by default, all plots aren't shown on the screen

# instead of typing this, copying it, and using %paste is a good plan
pl.plot(time,population/1.0e6,linestyle='none',marker='*',color='k',label='Data')
# try plot, semilogy, loglog
pl.title('US Population')
pl.xlabel('Year [CE]')
pl.ylabel('Population [millions]')
pl.legend(loc='upper left')
# xlim, and ylim, set the displayed range on the plot
# there are many many other plots (including xkcd-style!)
# http://matplotlib.org/gallery.html



# make a random 1d array with nm.random.randn
x_random = nm.random.randn(20)
nm.mean(x_random)
nm.std(x_random)
# say you've got missing data
x_data_some_missing = nm.array([-0.096,-0.677,nm.nan,1.384,nm.nan,1.037,0.243,-3.722,nm.nan,0.194])
nm.mean(x_data_some_missing) # fail
nm.nanmean(x_data_some_missing) # win!
nm.nanstd(x_data_some_missing) # yeah!
pl.figure()
pl.plot(x_data_some_missing,'*') # that works too



# lots of other random functions are in numpy, have a look!
# double-check that the array manipulation or math function you're about to write hasn't already been written
# http://docs.scipy.org/doc/numpy/reference/index.html
# for example...Mark Mitsubishi will give you 72 months no interest
# and you could buy a Mirage with automatic and AC there for $12,598
# payments per month is easy: 12598/72 = 175
# however...what if we miss this special deal, and we're stuck with
# what the bank offers, 48 months, 3.5% interest

# nm.pmt(interest rate per pay period, number of pay periods, present value of the loan)
nm.pmt(0.035/12.0,48,12598)
# $281.64 a month...dang, we better get to the dealership!



# here's another random function, interp1d
# go to that example file interp1d_example.py




# on the back end of numpy is C and some fortran
# so, speed of operations in is about the same as if you wrore the code in C
# yet it's often easier to read numpy code
# except if you're got a really weird for loop over all the elements of an array
# itertools can help sometimes, but sometimes it's really hard to read or just can't be done
# (prove all this with the scipy.weave example)
# weave_example.py



# finally, scipy is great
# so is scikit-learn
# here's a whirlwhind tour of support vector machines for facial recognition from a textbook
# svm_faces_example.py
