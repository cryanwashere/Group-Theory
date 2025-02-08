

class Permutation: 
    def __init__(self, n: int, perm: dict):
        
        self.n = n 
        self.perm = perm

    
    def operate(self, x: int):
        return self.perm[x]


    def compose(self, a):
        # returns a new permutation, which performs a, then performs self

        # make sure that the permutations are in the same permutation group
        assert self.n == a.n
        
        perm = dict()

        # create a new permutation by finding where every number gets mapped to by the composition of permutations
        for i in range(1,self.n+1):
            # important: we perform a, then self, so this would have the notation (self)(a)
            perm[i] = self.operate(a.operate(i))
        
        return Permutation(self.n, perm)



    def __eq__(self, other):
        return self.perm == other.perm

    def __str__(self):
        out = "("
        x = 1
        passed = set()
        nrange = set([i for i in range(1,self.n+1)])
        for i in range(self.n):
            passed.add(x)
            out += str(x)
            x = self.operate(x)
            if x in passed: 
                # get the lowest number not already passed
                if len(nrange - passed) == 0:
                    break
                out +=")("
                x = min(nrange - passed)
        out += ")"
        return out     

    def __hash__(self):
        return hash(self.__str__())
    
    def power_group(self):
        G = list()
        G.append(self.copy())
        x = self
        while True: 
            x = x.compose(self)
            if x == self:
                break
            G.append(x)
        return G
    
    def inverse(self):
        perm = {}
        for i in range(1,self.n):
            x = self.operate(i)
            perm[x] = i
        return Permutation(self.n, perm)
    
    @classmethod
    def from_str(cls, s):
        s = s[1:-1]
        arr = s.split(")(")
        arr = [list(a) for a in arr]

        perm = {}
        for cycle in arr: 
            for i, x in enumerate(cycle):
                x = int(x)
                if i+1 == len(cycle):
                    # go back to the beginning
                    perm[x] = int(cycle[0])
                else: 
                    perm[x] = int(cycle[i+1])
   
        return cls(len(perm.values()),perm)
    



def printout(G):

    print(f"[ group of order: {len(G)}")
    for g in G:
        print(g)
    print("]")



def generate_group_from_perms(perms: list):
    G = list()
    
    for perm in perms:
        G.append(perm.__str__())
        

    while True: 
        # operate every element of G with every other element of G, and add every new permutation created
        element_added = False
        for g_1 in G: 
            for g_2 in G: 
                a = Permutation.from_str(g_1).compose(Permutation.from_str(g_2))
                if not a.__str__() in G:
                    G.append(a.__str__())
                    element_added = True
                    break
            break
        
        if not element_added:
            break
        #print(f"element added: {a}")
    return G





def equal(G_1, G_2):
    for g in G_1:
        if not g in G_2:
            return False
    for g in G_2:
        if not g in G_1:
            return False
    return True

def conjugate(G, perm:str):
    ret = []
    for g in G: 
        conj = Permutation.from_str(perm).compose(Permutation.from_str(g).compose(Permutation.from_str(perm).inverse()))
        ret.append(conj.__str__())
    return ret

def multiplication_table(G):
    print("          ",end="")
    for g1 in G: 
        print(g1, end="  ")
    print("\n","="*100)
    for g1 in G: 
        print(g1, " :", end=" ")
        for g2 in G: 
            print(Permutation.from_str(g1).compose(Permutation.from_str(g2)), end="  ")
        print("")





# generate the dihedral group D5
D5 = generate_group_from_perms([
    Permutation.from_str("(12345)"),
    Permutation.from_str("(1)(25)(34)")
])
print("D5:")
printout(D5)

# generate the dihedral group D6
D6 = generate_group_from_perms([
    Permutation.from_str("(123456)"),
    Permutation.from_str("(14)(26)(35)")
])
print("D6:")
printout(D6)


"""
D5:
[ group of order: 10
(12345)
(1)(25)(34)
(13524)
(12)(35)(4)
(14253)
(13)(2)(45)
(15432)
(14)(23)(5)
(1)(2)(3)(4)(5)
(15)(24)(3)
]
D6:
[ group of order: 12
(123456)
(14)(26)(35)
(135)(246)
(1542)(36)
(14)(25)(36)
(1643)(2)(5)
(153)(264)
(1)(23)(4)(56)
(165432)
(1245)(3)(6)
(1)(2)(3)(4)(5)(6)
(1346)(25)
]
"""