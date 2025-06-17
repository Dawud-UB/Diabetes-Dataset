# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['diabetes_gui_app.py'],
    pathex=[],
    binaries=[],
    datas=[('svm_diabetes_model.pkl', '.'), ('C:\\Users\\dawud\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\imblearn\\VERSION.txt', 'imblearn')],
    hiddenimports=['imblearn.pipeline'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='diabetes_gui_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
