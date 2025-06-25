# As chaves agora são strings ("k1", "k2", "k3")
a = 'teste: {k1}, teste: {k2}, teste: {k3}'
bases = {'k1': 'a', 'k2': 'b', 'k3': 'c'}

# Agora **bases funciona, pois desempacota para argumentos nomeados válidos
# (k1='a', k2='b', k3='c')
print(a.format(**bases))