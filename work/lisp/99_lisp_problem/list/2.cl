;;;; No.2：输入一个列表，返回倒数第二个原子
;;; 我的实现，不知道什么原因无法运行
(defun my-to-last (lista)
  (if (or (null lista)
		  (null (rest lista)))
	nil
	(if (null (rest (rest null))) 
	  (first lista)
	  (my-to-last (rest lista)))))

;;; 答案的实现，居然有second这样的函数，典型的cond使用
(defun my-to-last-a (lista)
  (let ((relista (reverse lista)))
	(cond
	  ((null lista) inl)
	  ((<= (length lista) 2) lista)
	  (t (list (second relista) (first relista))))))
