[app]
title = SecureVaultX
package.name = securevaultx
package.domain = org.securevaultx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
source.exclude_dirs = .git,.venv,venv,bin,__pycache__
version = 1.0.0
requirements = python3==3.12.9,hostpython3==3.12.9,kivy==2.3.1,cryptography==42.0.8
orientation = portrait
fullscreen = 0
icon.filename = assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

android.api = 34
android.minapi = 23
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
p4a.branch = master
android.permissions =
