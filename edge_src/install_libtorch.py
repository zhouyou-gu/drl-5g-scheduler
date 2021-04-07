import os
import sys
if sys.version_info[0] < 3:
	raise SystemExit('Sorry, this code need Python3')

download_path = "https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-1.8.0%2Bcpu.zip"

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
os.system("wget " + download_path)
os.system("unzip libtorch*.zip")
os.system("rm libtorch*.zip")
