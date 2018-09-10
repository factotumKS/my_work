(*列表求积*)
fun prod ns = if null ns then 1 
              else (hd ns) * (prod(tl ns));

fun maxl [m] : int = m
  | maxl (m::n::ns) = if m>n then maxl (m::ns)
                      else maxl (n::ns);

prod [1,2,3,4,5,6];
maxl [1,2,3,7,5,6];
