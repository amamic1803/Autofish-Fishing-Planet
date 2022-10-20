import cv2
import numpy as np
from PIL import ImageGrab
import os


def main():

	img = ImageGrab.grab()
	img = np.array(img)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	template = cv2.imread(f"{os.path.dirname(os.getcwd())}\\data\\claim.png", cv2.IMREAD_GRAYSCALE)

	methods = [cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

	for method in methods:

		print(methods.index(method))

		result = cv2.matchTemplate(img, template, method)

		min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)

		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			#min
			print(min_value, min_loc)
		else:
			#max
			print(max_value, max_loc)


if __name__ == '__main__':
	main()
