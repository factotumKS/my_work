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

;;; 宏的内部`引导的是一串代码模板，在宏展开期套用生成代码
;;; 与dotimes宏类似，但是只在素数中迭代，可以试试输出特定区间的素数
(defmacro do-primes ((var start end) &body body)
	;; 列表模板，反引号表达式中,引导的表达式会求值，否则不会展开
	`(do ((,var (next-prime ,start) (next-prime (1+ ,var))))
	   ((> ,var ,end))
	   ,@body)) 	; ,@引导的列表会被拼接到上级列表中

;;; 防止“多次求值”泄漏：假设end为(random 100)则会在每次迭代时求一次值
(defmacro do-primes-1 ((var start end) &body body)
	`(do ((ending-prime end)
		  (,var (next-prime ,start) (next-prime (1+ ,var))))
	   ((> ,var ,ending-prime))
	   ,@body))

;;; 防止新的泄漏：
;;; 1、如果调用时传入的是ending-prime那么展开后就和宏内重名
;;; 2、违反最小惊动原则，符合start,end的求值顺序，得把顺序调一下
(defmacro do-primes-2 ((var start end) &body body)
  ;; gensym返回一个在程序运行过程中绝对安全不会重复的符号
  (let ((ending-prime-name (gensym)))	
	`(do ((,var (next-prime ,start) (next-prime (1+ ,var)))
		  (,ending-prime-name ,end))
	   ((> ,var ,ending-prime))
	   ,@body)))

;;; 上面用let和gensym的模式很常用，也可以编写一个宏来
(defmacro with-gensym ((&rest names) &body body)
  `(let ,(loop for n in names collect `(,n (gensym)))
	 ,@body))
#|
 将上面的内容总结为，自定义宏的三点要求：
 1、（默认）将展开式的子形式放在一个位置上，使其求值顺序与宏调用的子形式相同
 2、（默认）子形式仅求值一次，在展开式中用变量保存求值一次后的值来代替
 3、在宏展开期用gensym来创建内部的变量，防止重名
|#
