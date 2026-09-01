[app]

# (str) Title of your application
title = Fleet Management System 2600

# (str) Package name
package.name = fleetapp2600

# (str) Package domain (needed for android packaging)
package.domain = org.jamal.fleet

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json,yml,yaml,txt,db,mp3,wav

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, .venv, .git, .github

# (str) Application versioning
version = 1.0.0

# (list) Application requirements (تم تحديد إصدارات مستقرة لتفادي خطأ cython/cgl)
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,urllib3,certifi,chardet,idna

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
android.presplash_color = #1A0000

# (list) Permissions
android.permissions = INTERNET,RECORD_AUDIO,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 25b

# (bool) Accept all SDK licenses automatically
android.accept_sdk_license = True

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) The Android architectures to build for
android.archs = arm64-v8a

# (bool) Allow backup of application data
android.allow_backup = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
