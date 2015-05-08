import numpy as nm

# Sean Bryan
# sean.a.bryan@asu.edu
# 9/5/2014

# note...
# if you want to square an array
# just use... x**2.0
# that's the right answer!
# but, to illustrate the performance differences
# among these three methods, I'm choosing a simple apples-to-apples problem

# square the 1xN array naively using a for loop, really slow
def naive_squared(x):
    output = nm.zeros(len(x))
    for i in range(len(x)):
        output[i] = x[i]*x[i]
    
    return output

# alternately, use numpy to square the input array
# this is really fast and the code is easy to read
# BUT this kind of thing is only possible if you are doing a calculation
# that can be expressed in terms of native numpy functions
# such as arithmetic, sin/cos, exponential, straightforward logical indexing...
# (i.e. your problem is vectorizeable)
def numpy_squared(x):
    return x*x

# if you CANNOT express your calculation in terms of native numpy functions
# sometimes you just need to do a for loop over every element of your array
# and do your calculation one element at a time
# in that situation, using a naive python for loop would be IMPOSSIBLY slow
# but, there's another possibility
#
# here we use weave to run a snippet of C code to square the input array,
# which is still fast and the code is still easy to read
# plus this works even if the problem is NOT vectorizeable
def weave_squared(x):
    
    code = r"""
    int i;
    for(i = 0; i<N; i++) {
        output(i) = x(i)*x(i);
    }
    """
    # the three-quotes-in-a-row characters
    # allow for the string to extend onto multiple lines
    # in this text file
    # that's useful for writing code!
    #
    # also note, all the "r" does at the start there
    # is tell python that in the string to follow,
    # don't interpret any backslash or other special characters in the usual way
    # so, the string r'\n' comes out as an actual backslash and an actual letter n
    # where as the string '\n' comes out as a newline
    
    # preallocate the output variable outside of the C code
    output = nm.zeros(len(x))
    # calculate the length of the array out here in python
    # because the C language can't really do that
    # (upon further reading, maybe in C/python _Nx[0] is the length as well?)
    # (Anyway, len(x) is easy code to read)
    # (http://docs.scipy.org/doc/scipy/reference/tutorial/weave.html#inline)
    N = len(x)
    
    import scipy.weave
    scipy.weave.inline(code, ['output','x','N'], \
                       type_converters=scipy.weave.converters.blitz)
    # type_converters reflects the fact that a numpy array isn't the same as a C array
    # notice that we're using () and not [] inside the C code to index the array
    # that's because the "blitz" type converter has actually converted our numpy arrays
    # into C functions. that sounds slow, but it's actually no slower than native numpy
    # so...it's fast!
    
    return output


# let's try these three functions out, and see how fast they are
import time
# choose a number of elements in the array
length = 100000
# create an array that long
data = nm.random.randn(length)

# time how long it takes to square an array with a naive python for loop
starttime = time.time()
out = naive_squared(data)
print 'Naive For Loop - Elapsed time: ' + str(1000.0 * (time.time() - starttime)) + ' milliseconds'

# time how long it takes to square an array with vectorized numpy
starttime = time.time()
out = numpy_squared(data)
print 'Vectorized NumPy - Elapsed time: ' + str(1000.0 * (time.time() - starttime)) + ' milliseconds'

# time how long it takes to square an array with a for loop in c with weave
starttime = time.time()
out = weave_squared(data)
print 'C For Loop with Weave - Elapsed time: ' + str(1000.0 * (time.time() - starttime)) + ' milliseconds'
# note that the very first time this function is ever called, it will be "slow"
# this is because python is creating and compiling your C code.
# it stores the compiled file in a magical place somewhere, so
# that next time you call this function, python won't waste time
# recompiling it, but instead will just call the one it compiled
# earlier