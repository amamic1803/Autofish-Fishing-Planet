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
	run_data_path = "run_data"
	icon_path = "data\\fish_icon.ico"
	upx_path = "data\\upx.exe"
	result_path = "."
	work_path = "build"

	while os.path.isdir(work_path):
		work_path = f"build_{random.randint(1, 1_000_000_000)}"

	run_list = ['main.py',
	            '--noconfirm',
	            f'--icon "{icon_path}"',
	            f'--add-data "{icon_path};{os.path.dirname(icon_path)}"',
	            f'--upx-dir "{upx_path}"',
	            f'--key "{key}"',
	            f'--name "{name}"',
	            f'--workpath "{work_path}"',
	            f'--distpath "{result_path}"',
	            f'--specpath "{work_path}"']

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
			run_list.append(f'--add-data "{os.path.join(run_data_path, file)};{run_data_path}"')

	PyInstaller.__main__.run(run_list)

	shutil.rmtree(path=work_path, ignore_errors=True)


if __name__ == '__main__':
	main()
