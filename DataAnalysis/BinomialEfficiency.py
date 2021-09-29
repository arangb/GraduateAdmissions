import numpy as np
#from statsmodels.stats.proportion import proportion_confint # only does symmetric intervals!
from scipy.stats import beta
from scipy.stats import norm

def bayesian_binomial_hpdr(n, N, pct, a=1, b=1, n_pbins=1e3):
    """
    https://stackoverflow.com/questions/51617318/deprecationwarning-object-of-type-class-float-cannot-be-safely-interpreted
    Function computes the posterior mode along with the upper and lower bounds of the
    **Highest Posterior Density Region**.

    Parameters
    ----------
    n: number of successes 
    N: sample size 
    pct: the size of the confidence interval (between 0 and 1)
    a: the alpha hyper-parameter for the Beta distribution used as a prior (Default=1)
    b: the beta hyper-parameter for the Beta distribution used as a prior (Default=1)
    n_pbins: the number of bins to segment the p_range into (Default=1e3)

    Returns
    -------
    A tuple that contains the mode as well as the lower and upper bounds of the interval
    (mode, lower, upper)
    """
    # fixed random variable object for posterior Beta distribution
    rv = beta(n+a, N-n+b)
    # determine the mode and standard deviation of the posterior
    stdev = rv.stats('v')**0.5
    mode = (n+a-1.)/(N+a+b-2.)
    # compute the number of sigma that corresponds to this confidence
    # this is used to set the rough range of possible success probabilities
    n_sigma = np.ceil(norm.ppf( (1+pct)/2. ))+1
    # set the min and max values for success probability 
    max_p = mode + n_sigma * stdev
    if max_p > 1:
        max_p = 1.
    min_p = mode - n_sigma * stdev
    if min_p > 1:
        min_p = 1.
    # make the range of success probabilities
    p_range = np.linspace(min_p, max_p, int(n_pbins+1))
    # construct the probability mass function over the given range
    if mode > 0.5:
        sf = rv.sf(p_range)
        pmf = sf[:-1] - sf[1:]
    else:
        cdf = rv.cdf(p_range)
        pmf = cdf[1:] - cdf[:-1]
    # find the upper and lower bounds of the interval 
    sorted_idxs = np.argsort( pmf )[::-1]
    cumsum = np.cumsum( np.sort(pmf)[::-1] )
    j = np.argmin( np.abs(cumsum - pct) )
    upper = p_range[ (sorted_idxs[:j+1]).max()+1 ]
    lower = p_range[ (sorted_idxs[:j+1]).min() ]    
    return (mode, lower, upper)


def clopper_pearson(k,n,c):
    """
    k = number of successes
    n = sample size
    c = confidence interval: alpha=1-c
    http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
    alpha confidence intervals for a binomial distribution of k expected successes on n trials
    Clopper Pearson intervals are a conservative estimate.
    This gives the same result as ROOT:TEfficiency (with default method)
    from ROOT import TGraphAsymmErrors, TH1I, TCanvas, TEfficiency
    c1=TCanvas()
    hk = TH1I("hk","k",1,0,1); hk.SetBinContent(1,k)
    hn = TH1I("hn","n",1,0,1); hn.SetBinContent(1,n)
    g=TGraphAsymmErrors(1)
    g.BayesDivide(hk,hn)
    print('ROOT BayesDivide',g.GetErrorYlow(0),g.GetErrorYhigh(0))
    #k=9,n=10-> 0.11836128649123212, 0.06818779578397094
    pEff = TEfficiency(hk,hn) # Clopper-Pearson interval
    pEff.Draw()
    print('TEff',pEff.GetEfficiency(1),pEff.GetEfficiencyErrorLow(1),pEff.GetEfficiencyErrorUp(1))
    #k=9,n=10->0.9, 0.19413538963844057, 0.08287298586326675
    """
    lo = beta.ppf((1-c)/2, k, n-k+1)
    hi = beta.ppf(1 - (1-c)/2, k+1, n-k)
    mode=k/n
    return (mode,lo, hi)

def BinomialEfficiency(k,n,c=0.68269,method='bayes'):
    '''
    Inputs: 
    k = successes, 0 <= k <= n [int or array]
    n = total, n>0 [int or array]. If array, it must have the same shape as k.
    c = confidence level, float in [0,1], optional: 1 sigma=0.68
    method={'bayes', 'clopper','flat','jeffreys'}
    The 'bayes' method computes the lower and upper bounds of the posterior around the mode (highest posterior density region). This gives the same result as ROOT:BayesDivide.
    The 'clopper' method is not Bayesian, and uses the Clopper-Pearson method. This gives the same result as ROOT:TEfficiency.
    
    Returns: three arrays: mode, error_low, error_hi
    References: 
    BayesDivide: https://lss.fnal.gov/archive/test-tm/2000/fermilab-tm-2286-cd.pdf
    https://arxiv.org/pdf/1012.0566.pdf
    https://arxiv.org/pdf/0908.0130.pdf
    https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
    '''
    if c < 0. or c > 1.:
        print('confidence_level must be between 0. and 1.'); return

    k = np.asarray(k).astype(int)
    n = np.asarray(n).astype(int)
    if n.size != k.size: # initialize every element with the total
        n = np.full(k.size, n) # for example: n=[100,100,100,100,...,100]

    if (n <= 0).any():
        print('n must be positive'); return
    if (k < 0).any() or (k > n).any():
        print('k must be in {0, 1, .., n}'); return
    
    eff,error_lo,error_hi=[],[],[]
    for k_i,n_i in zip(k,n):
        if (k_i>n_i):
            print("BinomialEfficiency: bin %d in pass has more entries than corresponding bin in total! (%d>%d)"%(b,k_i,n_i))
         
        #norm=np.math.factorial(n+1)/np.math.factorial(n)/np.math.factorial(n-k)
        #v = (k+1)*(k+2)/((n+2)*(n+3)) - ((k+1)/(n+2))**2
        #print('book',mode,v)
        
        m,l,h = 0.,0.,0. # mode, lower bound, higher bound
        if (method == 'bayes'):
            m,l,h=bayesian_binomial_hpdr(k_i,n_i,c)
        elif (method == 'clopper'):
            m,l,h=clopper_pearson(k_i,n_i,c)
        elif (method == 'flat'):
            # Same as: astropy.stats.binom_conf_interval(k, n, confidence_level=c, interval='flat')
            m=k_i/n_i
            l=beta.ppf((1-c)/2.,k_i+1,n_i-k_i+1)
            h=beta.ppf(1-(1-c)/2.,k_i+1,n_i-k_i+1)
        elif (method == 'jeffreys'):
            m=k_i/n_i
            l=beta.ppf((1-c)/2. ,k_i+0.5, n_i-k_i+0.5)
            h=beta.ppf(1-(1-c)/2.,k_i+0.5, n_i-k_i+0.5)
        else:
            print("BinomialEfficiency: wrong method. Can be bayes,clopper,flat, or jeffreys"); return
        # Take care of extreme cases that return nan:
        if k_i==n_i: 
            h=1.0
        elif k_i==0:
            l=0.0

        eff.append(m)
        error_lo.append(m-l) # mode - lower_bound
        error_hi.append(h-m) # higher_bound - mode

    #print(method,eff,error_lo,error_hi)
    return (np.array(eff),np.array(error_lo),np.array(error_hi))
        
#k = [22, 5, 25, 35, 5, 61, 7, 85, 89, 95]
#n = 1000
#m,el,eh=BinomialEfficiency(k,n)
