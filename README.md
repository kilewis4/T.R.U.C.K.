# T.R.U.C.K
## Packaging the System Into an .exe
We use pyinstaller to get all of the necessary dependencies


> pip install pyinstaller \


Next we run pyinstaller through main so it knows what it needs to put into the exe.


> pyinstaller --onefile --add-data "Data\employee_data_02_04_2025.csv;Data" --add-data "Data\Unloader_103.json;Data" --add-data "Data\Unloader_1278.json;Data" --add-data "Data\Unloader_13586.json;Data" --add-data "Data\Unloader_Time_Reference.json;Data" --add-data "src\templates\TruckEntry.html;src\templates" src\GUI.py


This will put the exe in a folder called dist. Keep in mind that "your_module" in this command should be the relative path to your main file.
