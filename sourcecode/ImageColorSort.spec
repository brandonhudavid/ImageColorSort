# -*- mode: python -*-

block_cipher = None


a = Analysis(['ImageColorSort.py'],
             pathex=['/Users/brandonhudavid/Documents/GitHub/ImageColorSort/sourcecode'],
             binaries=[],
             datas=[('bd_icon.ico', '.'), ('bd_bg.gif', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ImageColorSort',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='bd.icns')
app = BUNDLE(exe,
             name='ImageColorSort.app',
             icon='bd.icns',
             bundle_identifier=None)
