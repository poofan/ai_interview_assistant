Dim objShell
Set objShell = CreateObject("WScript.Shell")

' Путь к .exe файлу (можно изменить)
exePath = objShell.CurrentDirectory & "\dist\Hintsage.exe"

' Запуск без окна (windowStyle = 0)
objShell.Run Chr(34) & exePath & Chr(34), 0, False

Set objShell = Nothing

