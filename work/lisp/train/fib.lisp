;;; 斐波纳契递归函数
(defun fib (x)
  (if (or (eql x 1) 
		  (eql x 2))
	x
	(+ (fib (- x 1)) (fib (- x 2)))))
