import numpy as np

class MathError(Exception) :
  def __init__(self, err_msg : str) :
    self.err_msg = msg
  def __str__(self) -> str:
    return self.err_msg

def is_null(M) :
  # calculate if the given matrix is ​​null
  return not np.any(M)

def inverse_of(M) :
  # calculates the inverse matrix of M
  if(np.linalg.det(M) == 0) :
    raise MathError("Non-invertible matrix")
  else:
    return np.linalg.inv(M)

if __name__ == "__main__" :

  _debug = 0

  print("Primal Simplex Algorithm")
  print("Author: Antônio Sidnei Moreira Cirqueira\n")

  print("Considering the problem in standard form")
  n = int(input("Enter the number of variables: "))
  m = int(input("Enter the number of constraints: "))
  if _debug : print("\nm = %d, n = %d" %(m, n))

  choice = input("Want to minimize or maximize? [0 - MIN, 1 - MAX]: ")
  maximize = True if int(choice) == 1 else False
  if _debug : print("maximize" if maximize else "minimize")

  print("Enter the cost vector c: ")
  # reads n-dimensional cost vector desrcibing objective function
  # NOTE: fractions must be in decimal form
  c = [float(cj) for cj in input().split(' ')[:n]]
  if _debug : print("c = ", c)

  print("Enter matrix A(%dx%d): " %(m, n))
  # read matrix A
  A = [[float(aij) for aij in input().split(' ')[:n]] for i in range(m)]
  if _debug : print("A = ", A)

  print("Enter matrix b: ")
  # read b m-dimensional vector
  b = [float(bj) for bj in input().split(' ')[:m]]
  if _debug : print("b = ", b)

  # initialize basic variable indices
  while(True) :
    inpt = input("Enter the initial basic indexes: ")
    IB = [(int(i) - 1) for i in inpt.split(' ')[:m]]

    try:
      B = [[line[IB[j]] for j in range(m)] for line in A]
    
      if(np.linalg.det(B) == 0) :
        raise MathError("This is not a Basic Matrix of A!")        
    
    except MathError as err:
      print(err); continue # Enter a new vector IB of Linearly Independent columns of A
    else : break # B is a valid basic matrix, algorithm continues

  # initialize non-basic variable indexes
  IN = [i for i in range(n) if i not in IB]
  
  count = 1;

  while(True) :

    if _debug : 
      print("\niteration #%d" %(count)); 
    
    if(B is None) : # isn't the first iteration of the algorithm
      B = [[line_A[IB[j]] for j in range(m)] for line_A in A]
      
    if _debug : print("B = ", B)

    try:
      Binv = inverse_of(B) # calculate B^(-1)
    except MathError as err:
      # does not have inverse
      # the algorithm guarantees that B will always be valid for each new iteration
      print(err); break # will not enter here

    xB = list(np.dot(Binv, b)) # calculate B^(-1)*b
    
    if _debug :
      print("B^(-1) = ", Binv) 
      print("x_B = ", xB)

    x = [0.0] * n
    for i in range(m) :
      x[IB[i]] = xB[i]

    if _debug : print("x%d = " %(count), x)

    if(is_null(x)) : break # not a Viable Basic Solution

    cB = [c[IB[i]] for i in range(m)] # cost of basic variables
    if _debug : print("c_B^T = ", cB)

    uT = list(np.dot(cB, Binv)) # calcula cB*B^(-1)  
    if _debug : print("u^T = ", uT)

    i_in = -1 # index that enters the base
    i_out = -1   # index out of base

    for j in range(n-m) : # iterates through non-basic variables

      aj = [[line_A[IN[j]]] for line_A in A] # aj column of N

      zj = np.dot(uT, aj)[0] # cB*B^(-1)*aj

      cj = c[IN[j]]      

      rc = cj - zj # xj reduced cost

      if _debug :
        print("a%d = " %(IN[j] + 1), aj)
        print("z%d = %f" %(IN[j] + 1, zj))
        print("c%d = %f" %(IN[j] + 1, cj))
        print("rc = ", rc)

      if(maximize and rc > 0) or (not maximize and rc < 0) :
        i_in = j
        
        hj = list(np.dot(Binv, aj))
        if _debug : print("h%d = " %(IN[i_in] + 1), hj)

        low = np.infty # infinity

        for i in range(m) :
          if hj[i] <= 0 : continue

          a = xB[i] / hj[i]
          if _debug : print("xB[%d]/hj[%d] = " %(i, i), a)

          if(a >= 0 and a < low) :
            low = a
            i_out = i
        
        break

    if(i_in < 0) : # optimal solution, no one to enter the base
      print("# of iterations: %d" %(count))
      print("x%d is an optimal solution for the problem" %(count)) 
      print("x = ", x)

      print("IB = ", end='')
      for i in IB : 
        print(i + 1, end = ' ')
      print()      

      print("the optimal value of the objective function is: ", end= '')
      cT = np.transpose(c); best = np.dot(cT, x)
      print(best)
      break

    elif(i_out < 0) :
      print("\nUnlimited Linear Programming Problem!") 
      break
    else:
      count += 1

      IB[i_out], IN[i_in] = IN[i_in], IB[i_out]    
      IB.sort(); IN.sort()

      if _debug : 
        print("IB = ", end='')
        for i in IB : 
          print(i + 1, end = ' ')
        print()

      B = None
    
  
