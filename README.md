# T.R.U.C.K
## Packaging the System Into an .exe
We use pyinstaller to get all of the necessary dependencies


> pip install pyinstaller \


Next we run pyinstaller through main so it knows what it needs to put into the exe.


> pyinstaller --onefile your_module/main.py


This will put the exe in a folder called dist. Keep in mind that "your_module" in this command should be the relative path to your main file.
