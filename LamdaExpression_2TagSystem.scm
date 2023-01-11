;;;;
;;;; Collatz-like function sequence from 5 on 2-tag system
;;;; by using lambda expression only
;;;;
;;;; (C) 2023 TAKIZAWA Yozo
;;;; This code is licensed under CC0.
;;;; https://creativecommons.org/publicdomain/zero/1.0/
;;;;

; Church booleans
(define T (lambda (x y) x))
(define F (lambda (x y) y))

; Church pairs and list encodings
(define (Cons x y) (lambda (z) (z x y)))
(define (Car p) (p (lambda (x y) x)))
(define (Cdr p) (p (lambda (x y) y)))
(define (CONS x y) (Cons F (Cons x y)))
(define (CAR p) (Car (Cdr p)))
(define (CDR p) (Cdr (Cdr p)))
(define NIL (Cons T F))
(define (NILP n) (Car n))

; Church numerals and calculations
(define ONE   (lambda (f) (lambda (x) (f x))))
(define TWO   (lambda (f) (lambda (x) (f (f x)))))
(define THREE (lambda (f) (lambda (x) (f (f (f x))))))
(define (DEC n)
  (lambda (f)
    (lambda (x)
      (((n (lambda (g) (lambda (h) (h (g f))))) (lambda (u) x)) (lambda (u) u)))))
(define (ZEROP n) ((n (lambda (x) F)) T))
(define (EQLP m n) (ZEROP ((n DEC) m)))
(define (EQP x y) ((EQLP x y) (EQLP y x) (EQLP x y)))

; initial value of queue: (1 1 1 1 1) as 5
(define q (CONS ONE (CONS ONE (CONS ONE (CONS ONE (CONS ONE NIL))))))

; 2-tag system rules for Collatz-like function: {1=>(2 3), 2=>(1), 3=>(1 1 1)}
(define r (CONS (CONS ONE (CONS TWO (CONS THREE NIL)))
          (CONS (CONS TWO (CONS ONE NIL))
          (CONS (CONS THREE (CONS ONE (CONS ONE (CONS ONE NIL))))
          NIL))))

;; append and assoc
(define (AP a b)
  (((NILP a)
    (lambda () b) (lambda () (CONS (CAR a) (AP (CDR a) b))))))
(define (AQ k a)
  (((NILP a)
    (lambda () NIL)
    (lambda () (((EQP k (CAR (CAR a)))
                 (lambda () (CDR (CAR a)))
                 (lambda () (AQ k (CDR a)))))))))

;; 2-tag system
(define (two-ts q r)
  (((NILP (CDR q))
    (lambda () (CONS q NIL))
    (lambda () (CONS q (two-ts (AP (CDR (CDR q)) (AQ (CAR q) r)) r))))))


;;;; Verification for the result of 2-tag system

(define (lambda2cons x)
  (let ((a (assq (CAR x) `((,ONE . a) (,TWO . b) (,THREE . c)))) (d (CDR x)))
    (cons (if a (cdr a) (lambda2cons (CAR x)))
          (if (eq? d NIL) '() (lambda2cons d)))))

(for-each (lambda (x) (display x) (newline)) (lambda2cons (two-ts q r)))

