[app]
title = NTH POS
package.name = nthpos
package.domain = in.newtrendhost
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3,kivy==2.3.1
orientation = landscape
fullscreen = 0
android.permissions = INTERNET,CAMERA,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN
android.api = 35
android.minapi = 24
android.ndk = 27c
android.archs = arm64-v8a
android.accept_sdk_license = True
icon.filename = %(source.dir)s/assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
