import tabula
df = tabula.read_pdf("../datafolder/demo.pdf", pages='1')

print(df)
print("hello")