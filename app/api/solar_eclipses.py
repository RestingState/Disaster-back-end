f = open('..\\database\\solar_eclipses.txt', encoding="utf-8-sig")
list_ = []
for line in f:
    line_strip = line.strip()
    l = line_strip.split(sep="_")
    list_.append(l)
print(list_)
