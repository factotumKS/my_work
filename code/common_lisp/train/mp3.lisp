(defvar *db* nil)

; 添加一条CD进入数据库
(defun add-record (cd) (push cd *db*))

; 添加一条CD信息
(defun make-cd (title artist rating ripped)
  (list :title title :artist artist :rating rating :ripped ripped))

#|
 输出整个数据库信息
 1、~a表示美化，~%表示换行，~10t产生足够的空格
 2、~{ 和 ~} 分别表示对列表中的每个元素做的处理
|#
(defun dump-db ()
  (dolist (cd *db*)
	(format t "~{~a: ~10t~a~%~}~%" cd)))

; 提示信息并接受输入
(defun prompt-read (prompt)
  (format *query-io* "~a: " prompt)
  (force-output *query-io*)
  (read-line *query-io*))

#|
 引导用户依次输入每个值，得到一条CD记录
 1、or函数：的第一参数为NIL时，返回第二个参数为默认值
 2、y-orn-p函数：只接受Y,y,N,n作为输入，不是的话会重新调用
|#
(defun prompt-for-cd ()
  (make-cd
	(prompt-read "Title")
	(prompt-read "Artist")
	(or (parse-integer (prompt-read "Rating") :junk-allowed t) 0)
	(y-or-n-p "Ripped [Y/N]:")))

#|
 循环添加CD
 1、loop宏：不断执行一个表达式体，最后通过调用return函数来退出
|#
(defun add-cds ()
  (loop (add-record (prompt-for-cd))
	(if (not (y-or-n-p "Another CD? [y/n]: ")) (return))))

#|
 保存：保存当前数据库，需要指定文件名
 1、with-open-file宏：文件流绑定在一个变量上，执行一组表达式，最后关闭
 2、:output参数表示文件状态为“写入”；:supersede表示同名文件覆盖
 3、with-standard-io-syntax确保那些影响print行为的特殊变量能被设置为标准值
	确保lisp读取器和打印器的操作彼此兼容
 4、print将lisp对象打印为可被lisp读取的形式
|#
(defun save-db (filename)
  (with-open-file (out filename
					   :direction :output
					   :if-exists :supersede)
	(with-standard-io-syntax
	  (print *db* out))))

#|
 加载：将数据加载回数据库的函数
 1、使用默认值input
 2、setf宏：重要赋值操作宏，第二参数的求值结果赋给第一参数
|#
(defun load-db (filename)
  (with-open-file (in filename)
	(with-standard-io-syntax
	  (setf *db* (read in)))))
#|
 筛选：选出符合条件的CD
 1、remove-if-not宏：第一个参数是返回布尔值的函数，第二个参数是待筛选列表
 2、#'()：表示“获取函数，其名如下”，如果不用的话表示传入变量
 3、lambda：匿名函数，临时定义一个函数，与上面配合使用
|#
(defun select (selector-fn)
  (remove-if-not selector-fn *db*))

#|
 更新：选出符合条件的CD，并全部更改
 1、mapcar宏：把函数映射在一个列表上，得到新列表
|#
(defun update (selector-fn &key title artist rating (ripped nil ripped-p))
  (setf *db*
		(mapcar
		  #'(lambda (row)
			  (when (funcall selector-fn row)
				(if title    (setf (getf row :title) title))
				(if artist   (setf (getf row :artist) artist))
				(if rating   (setf (getf row :rating) rating))
				(if ripped-p (setf (getf row :ripped) ripped)))
			  row) *db*)))

#|
 返回选择器函数的生成函数，在select中使用
 1、关键字形参：形参开头加&keys，调用时就要指明参数名和值
 2、关键字参数可以用一个列表表示，第二个原子表示默认值，第三个可以表示是否
	传入这个参数；这里可以区分传入的nil和没有传入导致的默认nil
 3、if宏：相当于三目运算符，本身是个有返回值的表达式，t表示逻辑真
|#
(defun where (&key title artist rating (ripped nil ripped-p))
  #'(lambda (cd)
	  (and
		(if title    (equal (getf cd :title) title) t)
		(if artist   (equal (getf cd :artist) artist) t)
		(if rating   (equal (getf cd :rating) rating) t)
		(if ripped-p (equal (getf cd :ripped) ripped) t))))
