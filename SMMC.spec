# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['SMMC.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo.png', '.'),  # Include your logo file
        # Add any other resource files here
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        'PyPDF2',
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
        'reportlab.lib.units',
        'fitz',
        'PIL.Image',
        'threading',
        'tempfile',
        'subprocess',
        'platform',
        'atexit',
        'pathlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas'  # Exclude unused heavy libraries
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyd = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyd,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SMMC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',  # Your converted icon
    version='version.txt'  # Optional version info
)