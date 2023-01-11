# Church booleans
T = lambda x, y: x
F = lambda x, y: y

# Church pairs and list encodings
def Cons(x, y): return lambda z: z(x, y)
def Car(p): return p(lambda x, y: x)
def Cdr(p): return p(lambda x, y: y)
def CONS(x, y): return Cons(F, Cons(x, y))
def CAR(p): return Car(Cdr(p))
def CDR(p): return Cdr(Cdr(p))
NIL = Cons(T, F)
def NILP(n): return Car(n)

# Church numerals and calculations
ONE   = lambda f: lambda x: f(x)
TWO   = lambda f: lambda x: f(f(x))
THREE = lambda f: lambda x: f(f(f(x)))
def DEC(n): return lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda u: x)(lambda u: u) 
def ZEROP(n): return n(lambda x: F)(T)
def EQLP(m, n): return ZEROP(n(DEC)(m))
def EQP(x, y): return EQLP(x, y)(EQLP(x, y), EQLP(x, y))


print(EQP(ONE, TWO)(True, False))


#q = 'a'*5
#r = {'a':'bc', 'b':'a', 'c':'aaa'}
#while q[1:]:
#    q = q[2:] + r[q[0]]
#    print(q)
