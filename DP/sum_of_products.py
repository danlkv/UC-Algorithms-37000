import sys
import numpy as np

def U(a, T, N):
    m = 0
    for k in range(1, N+1):
        m1 = T[N-k] + a[N-k]*a[N]
        if m1 > m:
            m = m1
    return m

def solve_DP(a):
    n = len(a)
    T = np.zeros(n+1)
    T[0] = 0
    T[1] = 0
    for i in range(2, n+1):
        T[i] = max(U(a, T, i-1), T[i-1])

    #print('DBG:T', T)
    return T[i]

def main():
    fname = sys.argv[1]
    with open(fname) as f:
        line = f.readline()
    a = line.split()
    a = [int(x) for x in a]
    sol = solve_DP(a)
    print(sol)

if __name__=='__main__':
    main()
