On Error Resume Next

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Определяем путь к скрипту
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Переходим в директорию проекта
WshShell.CurrentDirectory = scriptDir

' Путь к python.exe (PyQt6 не работает с pythonw.exe!)
pythonPath = scriptDir & "\venv\Scripts\python.exe"
mainPath = scriptDir & "\main.py"

' Проверка существования файлов
If Not fso.FileExists(pythonPath) Then
    MsgBox "Ошибка: python.exe не найден в venv!" & vbCrLf & vbCrLf & _
           "Путь: " & pythonPath & vbCrLf & vbCrLf & _
           "Запустите install.bat для установки venv", vbCritical, "Hintsage"
    WScript.Quit 1
End If

If Not fso.FileExists(mainPath) Then
    MsgBox "Ошибка: main.py не найден!" & vbCrLf & vbCrLf & _
           "Путь: " & mainPath, vbCritical, "Hintsage"
    WScript.Quit 1
End If

' Запуск БЕЗ окна (0 = скрытый режим, False = не ждать завершения)
Dim cmd
cmd = """" & pythonPath & """ """ & mainPath & """"
WshShell.Run cmd, 0, False

' Проверка что запустилось
WScript.Sleep 2000

' Уведомление о запуске
MsgBox "✅ Hintsage запущен в фоновом режиме!" & vbCrLf & vbCrLf & _
       "⌨️ Горячие клавиши:" & vbCrLf & _
       "  Ctrl+Shift+H - Показать/скрыть окно" & vbCrLf & _
       "  Ctrl+Shift+Q - Распознать речь" & vbCrLf & _
       "  Ctrl+Shift+S - Скриншот + OCR" & vbCrLf & _
       "  Ctrl+Shift+X - Выход" & vbCrLf & vbCrLf & _
       "📝 Логи: logs\hintsage.log", vbInformation, "Hintsage AI (GPU)"

