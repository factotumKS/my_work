(defun test-+ ()
  (format t "~:[fail~;pass~]...~a~%" (= (+ 1 2) 3) `(= (+ 1 2) 3))
  (format t "~:[fail~;pass~]...~a~%" (= (- 10 2) 8) `(= (+ 10 2) 8))
  (format t "~:[fail~;pass~]...~a~%" (= (+ 4 2) 6) `(= (+ 4 2) 6)))
