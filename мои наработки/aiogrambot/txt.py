res = []
res.append("закажи вфыв ыфв фыв")
text = res[0]
ogrizok = (text[text.find('закажи') + 6:])
f = open('1.txt', 'r')
f.write(ogrizok +"\n")
print(f.read())
f.close()