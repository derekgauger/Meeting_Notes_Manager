import PyInstaller.__main__

PyInstaller.__main__.run([
   'mnm.py',
   '--onefile',
   '--windowed',
   "--icon=mnm.ico"
])