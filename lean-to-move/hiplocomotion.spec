# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['hiplocomotion.py'],
             pathex=['G:\\vr test stuff\\Tracker-Driver\\hip_locomotion'],
             binaries=[('G:\\Python\\Python396\\Lib\\site-packages\\openvr\\libopenvr_api_64.dll','.\\openvr')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='hiplocomotion',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='hiplocomotion')
