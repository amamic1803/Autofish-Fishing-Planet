import cv2
import time
from PIL import ImageGrab
import numpy as np

time.sleep(5)

start = time.time()
screen_load = ImageGrab.grab(bbox=(1423, 916, 1666, 1020))
cv_img = cv2.cvtColor(np.array(screen_load), cv2.COLOR_RGB2GRAY)


poz_u_znam = {}
for z in ["", "_dark"]:
	for i in range(10):
		template = cv2.imread(fr'opencv-templates\{i}{z}.png', 0)
		result = cv2.matchTemplate(cv_img, template, cv2.TM_SQDIFF)

		tem = {}
		pozicije = np.where(result <= 11500000)
		pozicije_x = pozicije[1]
		pozicije_y = pozicije[0]

		for j in zip(pozicije_y, pozicije_x):
			if j[1] in tem.keys():
				tem[j[1]].append(result[j])
			else:
				tem[j[1]] = [result[j]]

		for j in tem.keys():
			if j in poz_u_znam.keys():
				poz_u_znam[j].append((i, min(tem[j])))
			else:
				poz_u_znam[j] = [(i, min(tem[j]))]

koordinate = list(poz_u_znam.keys())
norm_poz_u_znam = {}

while len(koordinate) != 0:
	koord = koordinate[0]
	vrijednosti_koord = poz_u_znam[koord]
	koordinate.remove(koord)
	for i in range(1, 11):
		if koord - i in koordinate:
			vrijednosti_koord.extend(poz_u_znam[koord - i])
			koordinate.remove(koord - i)
		if koord + i in koordinate:
			vrijednosti_koord.extend(poz_u_znam[koord + i])
			koordinate.remove(koord + i)
	norm_poz_u_znam[koord] = vrijednosti_koord

redoslijed = list(norm_poz_u_znam.keys())
redoslijed.sort()

broj = ""
for i in redoslijed:
	mogucnosti = norm_poz_u_znam[i]
	vrijednost = mogucnosti[0][1]
	znamenka = mogucnosti[0][0]
	for j in mogucnosti:
		if j[1] < vrijednost:
			vrijednost = j[1]
			znamenka = j[0]
	broj += str(znamenka)

if broj == "":
	broj = "0"

print(int(broj))
print(time.time() - start)
