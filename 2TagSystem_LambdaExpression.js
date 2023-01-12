//
// Collatz-like function sequence from 5 on 2-tag system
// by using lambda experssion only (with function and variable definitions)
//
// (C) 2023 TAKIZAWA Yozo
// This code is licensed under CC0.
// https://creativecommons.org/publicdomain/zero/1.0/
//

// Church booleans
const T = (x, y) => x;
const F = (x, y) => y;

// Church numerals and calculations
const ONE   = f => x => f(x)
const TWO   = f => x => f(f(x))
const THREE = f => x => f(f(f(x)))
function DEC(n) { return f => x => n(g => h => h(g(f)))(u => x)(u => u); }
function ZEROP(n) { return n(x => F)(T); }
function ELP(m, n) { return ZEROP(n(DEC)(m)); }
function EQP(m, n) { return ELP(m, n)(ELP(n, m), ELP(m, n)); }

//Church pairs and list encodings
function Cons(x, y) { return z => z(x, y); }
function Car(p) { return p((x, y) => x); }
function Cdr(p) { return p((x, y) => y); }
function CONS(x, y) { return Cons(F, Cons(x, y)); }
function CAR(p) { return Car(Cdr(p)); }
function CDR(p) { return Cdr(Cdr(p)); }
const NIL = Cons(T, F);
function NCONSP(n) { return Car(n); }

// initial value of queue: [1,1,1,1,1] as 5
const q = CONS(ONE, CONS(ONE, CONS(ONE, CONS(ONE, CONS(ONE, NIL)))));

// 2-tag system rules for Collatz-like function: {1:(2,3), 2:(1), 3:(1,1,1)}
const r1 = CONS(ONE, CONS(TWO, CONS(THREE, NIL)));
const r2 = CONS(TWO, CONS(ONE, NIL));
const r3 = CONS(THREE, CONS(ONE, CONS(ONE, CONS(ONE, NIL))));
const r = CONS(r1, CONS(r2, CONS(r3, NIL)));

// append and assoc
function AP(a, b) {
  return NCONSP(a)(() => b, () => CONS(CAR(a), AP(CDR(a), b)))();
}
function AS(k, a) {
  const TC = () => NIL;
  const FC1 = () => CDR(CAR(a));
  const FC2 = () => AS(k, CDR(a));
  const FC = () => EQP(k, CAR(CAR(a)))(FC1, FC2)();
  return NCONSP(a)(TC, FC)();
}

// 2-tag system
function two_ts(q, r) {
  const TC = () => CONS(q, NIL);
  const FC = () => CONS(q, two_ts(AP(CDR(CDR(q)), AS(CAR(q), r)), r));
  return NCONSP(CDR(q))(TC, FC)();
}


// Verification for the result of 2-tag system

function lambda2cons(x) {
  const TC = () => ({1:'a', 2:'b', 3:'c'}[CAR(x)(x => x+1)(0)]);
  const a = NCONSP(CAR(x))(TC, () => lambda2cons(CAR(x)))();
  let d = CDR(x); d = d == NIL ? [] : lambda2cons(d);
  return [a].concat(d);
}

const rc = lambda2cons(two_ts(q, r));
for (let i = 0; i < rc.length; i++) console.log(rc[i].join(''));

