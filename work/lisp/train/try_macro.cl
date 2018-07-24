;;;; 自定义宏实验：尝试定义一个素数循环宏
;;; 判断素数的函数
(defun primep (x)
  (do ((i 2 (1+ i)))
	((>= i x) t)
	(if (= 0 (mod x i)) (return nil))))

;;; 返回下一个大于等与实参的素数的函数
(defun next-prime (x)
  (do ((i (1+ x) (1+ i)))
	((primep i) i)))

;;; 与dotimes宏类似，但是只在素数中迭代，可以试试输出特定区间的素数
(defmacro do-primes ((var start end) &body body)
	;; 列表模板，反引号表达式中,引导的表达式会被求值，否则不会展开
	`(do ((,var (next-prime ,start) (next-prime (1+ ,var))))
	   ((> ,var ,end))
	   ,@body)) 	; ,@引导的列表会被拼接到上级列表中

;;; 防止“多次求值”泄漏：假设end为(random 100)则会在每次迭代时求一次值
(defmacro do-primes-1 ((var start end) &body body)
	`(do ((ending-prime end)
		  (,var (next-prime ,start) (next-prime (1+ ,var))))
	   ((> ,var ,ending-prime))
	   ,@body))

;;; 防止新的泄漏：1、如果调用时传入的是ending-prime那么展开后就和宏内重名
;;; 2、违反最小惊动原则，符合start,end的求值顺序，得把顺序调一下
(defmacro do-primes-2 ((var start end) &body body)
  ;; gensym返回一个在程序运行过程中绝对安全不会重复的符号
  (let ((ending-prime-name (gensym)))	
	`(do ((,var (next-prime ,start) (next-prime (1+ ,var)))
		  (,ending-prime-name ,end))
	   ((> ,var ,ending-prime))
	   ,@body)))


