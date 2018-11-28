val matrix = [[1,2,3,4],
              [5,6,7,8],
              [9,10,11,12]];

fun headcol [] = []
  | headcol ((x::_)::rows) = x::headcol rows;

fun tailcol [] = []
  | tailcol ((_::x)::rows) = x::tailcol rows;

fun transpose ([]::rows) = []
  | transpose M          = headcol M::transpose (tailcol M);


transpose matrix;


