import multiprocessing
import autofish


def main():
	autofish.run()


if __name__ == '__main__':
	multiprocessing.freeze_support()
	main()
