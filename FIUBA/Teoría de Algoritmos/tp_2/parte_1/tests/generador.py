import random

# Parámetros
porciones = 10
personas = 10
max_restricciones = 9
min_restricciones = 8

# Nombres ficticios únicos para 25 personas
nombres = [
    "Elon", "Steve", "Mark", "Jeff", "Larry",
    "Bill", "Warren", "Tim", "Sundar", "Satya",
    "Zuckerberg", "Bezos", "Gates", "Musk", "Cook",
    "Nadella", "Page", "Brin", "Buffett", "Schmidt",
    "Ellison", "Hastings", "Jobs", "Thiel", "Balmer",
    "Santi", "Hugo", "Juli", "Joaco", "Alberto"
]
nombres = nombres[:personas]

# Generar ofertas aleatorias entre 0 y 15
ofertas = []
for nombre in nombres:
    valores = [random.randint(0, 1000) for _ in range(porciones)]
    linea = f"{nombre}," + ",".join(map(str, valores))
    ofertas.append(linea)

# Generar restricciones aleatorias: cada persona puede tener 0 a 4 restricciones
restricciones = []
for i in range(personas):
    n_restricciones = random.randint(min_restricciones, max_restricciones)
    posibles = [n for j, n in enumerate(nombres) if j != i]
    restringidos = random.sample(posibles, n_restricciones)
    linea = ",".join([nombres[i]] + restringidos) if restringidos else nombres[i]
    restricciones.append(linea)

# Guardar en archivos
i = 9
ofertas_path = "./ofertas"+str(i)+".txt"
restricciones_path = "./restricciones"+str(i)+".txt"

with open(ofertas_path, "w") as f:
    f.write(str(porciones)+"\n")
    f.write("\n".join(ofertas))

with open(restricciones_path, "w") as f:
    f.write("\n".join(restricciones))

