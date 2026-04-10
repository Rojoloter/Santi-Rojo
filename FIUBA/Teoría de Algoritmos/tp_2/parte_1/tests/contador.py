import sys
import time

def contar_exp(n, m):
    if m == 0:
        return 1
    return 1 + contar_exp(n, m-1) + n * contar_exp(n-1, m-1)

def contar_nm(n, m):
    n+=1
    m+=1
    M = [[0] * (n+1) for _ in range(m)]
    
    for j in range(1, n+1):
        M[0][j] = 1

    for i in range(1, m):
        for j in range(1, n+1):
            M[i][j] = 1 + M[i-1][j] + (j-1) * M[i-1][j-1]
            
    return M[m-1][n]

def combinaciones(n, m):
    if m == 0:
        return 1
    return combinaciones(n, m-1) + n * combinaciones(n-1, m-1)

if __name__ == "__main__":
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    start = time.time()
    res_dyn = contar_nm(n, m)
    end = time.time()
    print(f"elementos en árbol dinámico: {res_dyn:_}")
    print(f"tiempo: {end - start:.6f} s")

    start = time.time()
    res_exp = contar_exp(n, m)
    end = time.time()
    print(f"elementos en árbol exponencial: {res_exp:_}")
    print(f"tiempo: {end - start:.6f} s")