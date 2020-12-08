if not "%~0"=="%~dp0.\%~nx0" (
    start /min cmd /c,"%~dp0.\%~nx0" %*
    exit
)

cd C:\Users\User\microscope-controller
PowerShell -command "conda activate microscope; python StackingSystem_Controller.py"
