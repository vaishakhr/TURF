from __future__ import division
import collections
import scipy
import numpy as np
NewHypothesisPiece = collections.namedtuple('NewHypothesisPiece', ['left', 'right', 'hypothesis'])

# given left, right, parameter k, cuts the interval into more segments
def GeomUnif(left, right, po, k_po, k_unif):
# these are dummy intervals for experimentation, replace with proper partition
    a = []
    mid = (left+right)/2
    diff = right - left
    delta = 0
    left_inter_rightside = mid
    right_inter_rightside = mid
    right_inter_leftside = mid 
    left_inter_leftside = mid
    for i in range(k_po):
        # print(i, delta)
        if i == k_po - 1:
            delta = right - right_inter_rightside
        else:
            delta = diff/(2*2**(po*(i+1)))
        # print(i, diff/2, 2**(po*(i+1)), diff/(2*2**(po*(i+1))), right - right_inter_rightside, delta)
        left_inter_rightside =  right_inter_rightside
        right_inter_rightside += delta
        right_inter_leftside = left_inter_leftside
        left_inter_leftside -= delta
        # print(max(1, int(np.ceil(k_unif/2**(0.25*(i+1))))))
        if left_inter_rightside != right_inter_rightside:
            a += UnifIntervals(left_inter_rightside, right_inter_rightside, max(1, int(np.ceil(k_unif/2**(0.25*(i+1))))))
        if left_inter_leftside != right_inter_leftside:
            a += UnifIntervals(left_inter_leftside, right_inter_leftside, max(1, int(np.ceil(k_unif/2**(0.25*(i+1))))))
        a.sort()
    return a

# returns a list of k uniformly spaced intervals 
def UnifIntervals(left, right, k):
    diff = right-left
    offset = diff/k
    a = []
    for i in range(k):
        a += [[left+i*offset, left+(i+1)*offset]]
    return a

#  returns the number of samples in an interval
def NumSamples(inter, samples):
    ctr = 0
    for x in samples:
        if inter[0] <= x < inter[1]:
            ctr += 1
    return ctr

# shifts hypothesis based on the empirical mass
def ShiftHypothesis(inter, hypothesis, samples, n):
    delta = samples/n-PolyWeight(hypothesis, inter)
#     delta = 73
    shift_hypothesis = np.concatenate((hypothesis[:-1], np.array([hypothesis[-1]+delta/(inter[1]-inter[0])])))
    return shift_hypothesis

def PolyWeight(hypothesis, inter):
    func = lambda x : np.polyval(hypothesis, x)
    integral = scipy.integrate.romberg(func, inter[0], inter[1], vec_func=True, tol=1e-5, divmax=30)
    return integral

def NewHypothesisPieces(HypothesisPieces, t, d, samples):
    po = 1 
    l = 1
    k_po = max(1, int(np.log(l*(d+1)**2*np.sqrt(len(samples)/(t*(d+1)))/100)))
    # print(k_po)
    k_unif = 2
    newpieces = []
    for HypoPiece in HypothesisPieces:
        left = HypoPiece.left
        right = HypoPiece.right
        hypothesis = HypoPiece.hypothesis
        inter_vec = GeomUnif(left, right, po, k_po, k_unif)
# this loop runs over intervals in the new partition, inter[0] is the left end point and inter[1] is the right end point
        for inter in inter_vec:
            numsamples_inter = NumSamples(inter, samples)
# modifies the hypothesis in the interval referred by inter based on the fraction of samples in that interval
            newhypothesis = ShiftHypothesis(inter, hypothesis, numsamples_inter, len(samples))
            newpieces += [NewHypothesisPiece(inter[0], inter[1], newhypothesis)]
    return newpieces

def UnifHypothesisPieces(HypothesisPieces, k, samples):
    newpieces = []
    for HypoPiece in HypothesisPieces:
        left = HypoPiece.left
        right = HypoPiece.right
        hypothesis = HypoPiece.hypothesis
        inter_vec = UnifIntervals(left, right, k)
# this loop runs over intervals in the new partition, inter[0] is the left end point and inter[1] is the right end point
        for inter in inter_vec:
            numsamples_inter = NumSamples(inter, samples)
# modifies the hypothesis in the interval referred by inter based on the fraction of samples in that interval
            newhypothesis = ShiftHypothesis(inter, hypothesis, numsamples_inter, len(samples))
            newpieces += [NewHypothesisPiece(inter[0], inter[1], newhypothesis)]
    return newpieces

