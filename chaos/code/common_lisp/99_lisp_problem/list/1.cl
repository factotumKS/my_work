;;;; No.1:输入一个列表，返回最后一个原子
;;; 我的实现，依靠取最后点对的前元素实现
(defun my-last (lista)
  (car (last lista)))

;;; 答案实现，并使用了递归感觉没必要?
(defun your-last (lista)
  (if (null lista)
	nil 	; 检查列表非空
	(if (null (rest lista))
	  lista
	  (your-last (rest lista)))))
