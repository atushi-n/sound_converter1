import pykakasi

kks = pykakasi.kakasi()
print(type(kks))
# class 'pykakasi.kakasi.kakasi'

print(kks.convert("あいうえお漢字opあ"))

text = ""
for x in kks.convert("あいうえお漢字opあ"):
    text += x["hepburn"]
print(text)

text1 = ""
text2 = ""

if 16 <= len(text1):
    text1 += x["hepburn"]
else:
    text2 += x["hepburn"]
