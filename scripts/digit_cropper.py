import cv2
import numpy as np
from PIL import ImageGrab
import time
import os


def main():
	br = input()
	time.sleep(5)
	cv2.imwrite(f"{os.path.dirname(os.getcwd())}\\data\\{br}.png", np.array(ImageGrab.grab())[930:1003, 1586:1634])


if __name__ == "__main__":
	main()
