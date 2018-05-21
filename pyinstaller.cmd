SET pyinstaller_exe=venv\Scripts\pyinstaller.exe
SET data=--add-data=res\icon.ico;res --add-data=res\next.png;res --add-data=res\play.png;res --add-data=algovis_ru.qm;.
%pyinstaller_exe% --onedir --icon=res\icon.ico %data% --noconsole --clean AlgoVis.py