import sys
from cx_Freeze import setup, Executable

build_exe_options = dict(
       include_files=['images/']
)

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="XD",
       version="1.0",
       description="XDrive",
       author="galaxbomb",
       options = dict(build_exe=build_exe_options),
       executables=[Executable("mainUI.py", base=base)])
