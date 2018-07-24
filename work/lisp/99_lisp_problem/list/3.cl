;;;; NO.3：找到第k个原子
;;; 我的实现，循环k-1次去掉第一个原子，不过setf破坏性，最好传入副本
(defun element-at (lista k)
  (dotimes (i (decf k))
	(setf lista (rest lista)))
  (print (first lista)))

;;; 答案的实现，递归的设计
(defun element-at (lista k)
  (if (= n 1)
	(first lista)
	(element-at (rest lista) (1- k))))
