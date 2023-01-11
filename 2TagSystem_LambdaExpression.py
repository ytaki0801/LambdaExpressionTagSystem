####
#### Collatz-like function sequence from 5 on 2-tag system
#### by using lambda experssion only (with function and variable definitions)
####
#### (C) 2023 TAKIZAWA Yozo
#### This code is licensed under CC0.
#### https://creativecommons.org/publicdomain/zero/1.0/
####

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
def ELP(m, n): return ZEROP(n(DEC)(m))
def EQP(m, n): return ELP(m, n)(ELP(n, m), ELP(m, n))

# initial value of queue: (1,1,1,1,1) as 5
q = CONS(ONE, CONS(ONE, CONS(ONE, CONS(ONE, CONS(ONE, NIL)))))

# 2-tag system rules for Collatz-like function: {1:(2,3), 2:(1), 3:(1,1,1)}
r1 = CONS(ONE, CONS(TWO, CONS(THREE, NIL)))
r2 = CONS(TWO, CONS(ONE, NIL))
r3 = CONS(THREE, CONS(ONE, CONS(ONE, CONS(ONE, NIL))))
r = CONS(r1, CONS(r2, CONS(r3, NIL)))

# append and dic search
def AP(a, b): return NILP(a)(lambda: b, lambda: CONS(CAR(a), AP(CDR(a), b)))()
def DS(k, a):
    TC = lambda: NIL
    FC = lambda: EQP(k, CAR(CAR(a)))(lambda: CDR(CAR(a)), lambda: DS(k, CDR(a)))()
    return NILP(a)(TC, FC)()

# 2-tag system
def two_ts(q, r):
    TC = lambda: CONS(q, NIL)
    FC = lambda: CONS(q, two_ts(AP(CDR(CDR(q)), DS(CAR(q), r)), r))
    return NILP(CDR(q))(TC, FC)()


#### Verification for the result of 2-tag system

def lambda2cons(x):
    try:
        a = {ONE:'a', TWO:'b', THREE:'c'}[CAR(x)]
    except KeyError:
        a = False
    d = CDR(x)
    return [a if a else lambda2cons(CAR(x))] + ([] if d == NIL else lambda2cons(d))

for x in lambda2cons(two_ts(q, r)): print(''.join(x))
