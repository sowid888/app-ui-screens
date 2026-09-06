[app]

# (str) Title of your application
title = Fleet Management System 2600

# (str) Package name
package.name = fleetapp2600

# (str) Package domain (needed for android packaging)
package.domain = org.jamal.fleet

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (file extensions)
source.include_exts = py,png,jpg,kv,atlas,json,yml,yaml,txt,db,mp3,wav

# (list) Source files to exclude (file extensions)
source.exclude_exts = spec

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, .venv, .git, .github

# (str) Application versioning
version = 1.0.0

# (list) Application requirements (تم تحديد الإصدارات المتوافقة لمنع التعارض)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,certifi,chardet,idna

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

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then accept all SDK licenses automatically
android.accept_sdk_license = True

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) The Android architectures to build for
android.archs = arm64-v8a

# (bool) Allow backup of application data
android.allow_backup = True

# (str) Format used to package the app
android.release_artifact = apk
android.debug_artifact = apk


[buildozer]

# (int) Log level (تم التعديل إلى 1 لمنع اقتطاع السجلات في GitHub)
log_level = 1

# (int) Display warning if buildozer is run as root (تم التعطيل لتفادي التوقف)
warn_on_root = 0
