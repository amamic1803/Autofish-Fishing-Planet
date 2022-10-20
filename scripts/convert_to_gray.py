import cv2


def main():
	path = input("Full path (JPG or PNG): ")

	img = cv2.imread(path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	save_path = path[:-4] + "_gray.png"

	cv2.imwrite(save_path, gray)


if __name__ == '__main__':
	main()
