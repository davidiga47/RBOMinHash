
from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
if TYPE_CHECKING:
    from numpy.typing import ArrayLike
import random
from mpmath import nsum, inf
import numpy as np


#computes the RBO similarity between lists x and y
def rbo_sim(x, y, p=0.9, k=None):
    if k is None or k>max(len(x), len(y)):
        k = max(len(x), len(y))
    x_set = set()
    y_set = set()
    cumulative = 0.0
    A_d=0
    for d in range(1, k + 1):
        if d <= len(x):
            x_set.add(x[d - 1])
        if d <= len(y):
            y_set.add(y[d - 1])
        overlap = len(x_set.intersection(y_set))
        A_d = overlap / d
        cumulative += (p ** (d - 1)) * A_d
    final_int=A_d*k
    cumulative += float(nsum(lambda d: p**(d-1)*(final_int+d-k)/d, [k+1, inf]))
    return (1 - p) * cumulative

#Computes the hash of a ranking x given:
#   -d: depth of evaluation of x (it will be truncated at depth d)
#   -r: random sequence used to determine the hash
#The values are passed all together as a list since in this library
#   hash functions have just one input value
def _hash_RBO(xdr):
    x=xdr[0]
    d=xdr[1]
    r=xdr[2]
    if d<len(x):
        x=x[:d]            #truncate x if long enough
    res=[]
    for i in x:
        if i<len(r):
            res.append(r[i])
    if not res:
        res=[1]
    return min(res)



class RBOMinHash:
    """RBOMinHash is a probabilistic data structure for estimating
    RBO similarity between rankings.

    Args:
        p (float): the persistence of the model
        perm_len (int): the length of the permutation to be used to compute 
            the hash
        num_hashes (int): The number of different hash function to use on each 
            element
        hashfunc (Callable): The hash function used by
            this MinHash.
            It takes the input passed to the :meth:`update` method and
            returns a float.
        r
        d
        hashvalues (Optional[Iterable]): The hash values is
            the internal state of the MinHash. It can be specified for faster
            initialization using the existing :attr:`hashvalues` of another MinHash.
    """
    def __init__(
        self,
        p: float,
        perm_len: int,
        num_hashes: int,
        hashfunc: Callable = _hash_RBO,
        r: Optional[ArrayLike] = None,
        d: Optional[ArrayLike] = None,
        hashvalues: Optional[ArrayLike] = None,
    ) -> None:
        if hashvalues is not None:
            num_hashes = len(hashvalues)
        # Check the hash function.
        if not callable(hashfunc):
            raise ValueError("The hashfunc must be a callable.")
        self.hashfunc = hashfunc
        # Initialize hash values
        if hashvalues is not None:
            self.hashvalues = hashvalues
        else:
            self.hashvalues=[]
        
        #Just added the following attributes
        self.p=p
        self.perm_len=perm_len
        self.num_hashes=num_hashes
        
        if r is None and d is None:
            self.r=[]
            self.d=[]
            for _ in range(self.num_hashes):
                self.r.append([random.random() for _ in range(self.perm_len)])
                self.d.append(np.random.geometric(1-self.p))
        else:
            self.r=r
            self.d=d

    def update(self, b) -> None:
        """Update this RBOMinHash with a new value.
        The value will be hashed using the hash function specified by
        the `hashfunc` argument in the constructor.

        Args:
            b: The value to be hashed using the hash function specified.

        """
         
        for i in range(self.num_hashes):
            tmp_r = self.r[i]
            tmp_d = self.d[i]
            tmp=[b,tmp_d,tmp_r] #parse input
            self.hashvalues.append(self.hashfunc(tmp))

    def rbo(self, other: RBOMinHash) -> float:
        """Estimate the `RBO similarity`_ (resemblance) between the sets
        represented by this RBOMinHash and the other. It does so by computing 
        the probability of collisions of the two hashes

        Args:
            other (RBOMinHash): The other RBOMinHash.

        Returns:
            float: The probability of hash collisions.

        Raises:
            ValueError: If the two RBOMinHashes have different numbers of
                hash functions.

        """
        if len(self) != len(other):
            raise ValueError(
                "Cannot compute RBO given RBOMinHash with\
                    different numbers of permutation functions"
            )
        
        # k=min(len(self.hashvalues),len(other.hashvalues))
        k=len(self.hashvalues)
        cumulative=0
        for i in range(k):
            if(self.hashvalues[i]==other.hashvalues[i]):
                cumulative+=1
        return cumulative/k

    def merge(self, other: RBOMinHash) -> None:
        """Merge the other RBOMinHash with this one, making this one the union
        of both.

        Args:
            other (RBOMinHash): The other RBOMinHash.

        Raises:
            ValueError: If the two RBOMinHashes have different numbers of
                hash functions.

        """
        if len(self) != len(other):
            raise ValueError(
                "Cannot merge RBOMinHash with\
                    different numbers of permutation functions"
            )
        self.hashvalues = np.minimum(other.hashvalues, self.hashvalues)

    def is_empty(self) -> bool:
        """Returns:
        bool: If the current RBOMinHash is empty - at the state of just
            initialized.

        """
        return not self.hashvalues

    def clear(self) -> None:
        """Clear the current state of the RBOMinHash.
        All hash values are reset.
        """
        self.hashvalues = []

    def copy(self) -> RBOMinHash:
        """Return a copy"""
        return RBOMinHash(            
            p=self.p,
            perm_len=self.perm_len,
            num_hashes=self.num_hashes,
            hashfunc=self.hashfunc,
            r=self.r,
            d=self.d
        )

    def __len__(self) -> int:
        """Returns:
        int: The number of hash values.

        """
        return len(self.hashvalues)

    def __eq__(self, other: RBOMinHash) -> bool:
        """Returns:
        bool: If their hash values are both equal then two are equivalent.

        """
        return (
            type(self) is type(other) and np.array_equal(self.hashvalues, other.hashvalues)
        )

    


    

    
    
    