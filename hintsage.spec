# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller спецификация для Hintsage
One-file сборка с GPU поддержкой
"""

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

block_cipher = None

# ============================================================================
# СБОР ЗАВИСИМОСТЕЙ
# ============================================================================

# Основные зависимости
datas = []
binaries = []
hiddenimports = []

# 1. Конфигурация
datas += [
    ('config.example.yaml', '.'),
    ('config.yaml', '.'),
]

# 2. Модели Vosk (если есть)
if os.path.exists('models'):
    datas += [('models', 'models')]

# 3. Data директории
for folder in ['data/screenshots', 'data/sessions', 'logs']:
    os.makedirs(folder, exist_ok=True)
    datas += [(folder, folder)]

# 4. PyQt6 зависимости
tmp_ret = collect_all('PyQt6')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# 5. EasyOCR (модели и данные)
tmp_ret = collect_all('easyocr')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# 6. Faster-Whisper
hiddenimports += collect_submodules('faster_whisper')
hiddenimports += collect_submodules('ctranslate2')

# 7. CUDA библиотеки (для GPU)
hiddenimports += [
    'torch',
    'torch.cuda',
    'torch._C',
    'torch._six',
    'torchvision',
]

# 8. Vosk
hiddenimports += ['vosk']

# 9. Другие зависимости
hiddenimports += [
    'openai',
    'keyboard',
    'pynput',
    'sounddevice',
    'pyaudio',
    'numpy',
    'cv2',
    'PIL',
    'pytesseract',
    'nltk',
    'transformers',
    'requests',
    'aiohttp',
    'yaml',
    'cryptography',
    'loguru',
]

# 10. Наши модули
hiddenimports += [
    'modules.config_manager',
    'modules.llm_integration',
    'modules.context_manager',
    'modules.audio_capture',
    'modules.stt',
    'modules.question_detector',
    'modules.ui_overlay',
    'modules.security',
    'modules.screenshot_ocr',
    'modules.prompt_templates',
    'modules.parallel',
    'modules.parallel.request_queue',
    'modules.parallel.utils',
]

# ============================================================================
# ANALYSIS
# ============================================================================

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Исключаем ненужные модули для уменьшения размера
        'matplotlib',
        'scipy',
        'pandas',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ============================================================================
# PYZ (Python ZIP)
# ============================================================================

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# ============================================================================
# EXE (Executable)
# ============================================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Hintsage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Сжатие UPX (уменьшает размер на ~30%)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # БЕЗ КОНСОЛИ (для silent запуска)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # TODO: добавить иконку
    version_file=None,  # TODO: добавить версию
)

# ============================================================================
# ДОПОЛНИТЕЛЬНО: COLLECT (для debug режима)
# ============================================================================
# Раскомментируйте если нужна многофайловая сборка:
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='Hintsage'
# )

