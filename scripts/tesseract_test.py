# not currently in use

import pytesseract
from PIL import Image
import time
import os


def main():
	pytesseract.pytesseract.tesseract_cmd = "__PATH_TO_TESSERACT.EXE__"

	im1 = Image.open(f"{os.path.dirname(os.getcwd())}\\data\\claim.png").crop((0, 0, 109, 36))
	im1.show()

	start = time.time()
	imstr1 = pytesseract.image_to_string(im1)

	print(imstr1)
	print(time.time() - start)


if __name__ == '__main__':
	main()
