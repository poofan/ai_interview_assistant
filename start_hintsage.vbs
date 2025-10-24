Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d C:\git\ai_interview_assistant && .\venv\Scripts\python.exe main.py", 0, False

