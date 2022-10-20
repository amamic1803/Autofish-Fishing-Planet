import PyInstaller.__main__
import os
import datetime
import random
import shutil


def main():
	console = True
	onefile = True
	clean = True
	admin = False
	key = "DarkLord76865"
	name = f"Autofish_{datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}"
	run_data_path = os.path.join(os.path.abspath("."), "run_data")
	icon_path = os.path.join(os.path.abspath("."), "data\\fish_icon.ico")
	upx_path = os.path.join(os.path.abspath("."), "data")
	result_path = os.path.abspath(".")
	work_path = "build"

	while os.path.isdir(work_path):
		work_path = f"build_{random.randint(1, 1_000_000_000)}"
	work_path = os.path.join(os.path.abspath("."), work_path)

	run_list = ['main.py',
	            '--noconfirm',
	            '--icon', icon_path,
	            '--add-data', f"{icon_path};{os.path.basename(os.path.dirname(icon_path))}",
	            '--upx-dir', f"{upx_path}",
	            '--key', f"{key}",
	            '--name', f"{name}",
	            '--workpath', f"{work_path}",
	            '--distpath', f"{result_path}",
	            '--specpath', f"{work_path}"]

	if admin:
		run_list.append("--uac-admin")

	if clean:
		run_list.append("--clean")

	if onefile:
		run_list.append("--onefile")
	else:
		run_list.append("--onedir")

	if console:
		run_list.append("--console")
	else:
		run_list.append("--noconsole")

	for file in os.listdir(run_data_path):
		if os.path.isfile(os.path.join(run_data_path, file)):
			run_list.extend(('--add-data', f"{os.path.join(run_data_path, file)};{os.path.basename(run_data_path)}"))

	PyInstaller.__main__.run(run_list)

	shutil.rmtree(path=work_path, ignore_errors=True)


if __name__ == '__main__':
	main()
