[app]

# (str) Title of your application
title = منظومة 2600

# (str) Package name
package.name = truckapp2600

# (str) Package domain
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,ttf

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,arabic_reshaper,python-bidi,requests

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK licenses
android.accept_sdk_license = True

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) The Android architectures to build for
android.archs = arm64-v8a

# [تثبيت الفرع المستقر لمنع مشاكل Python 3.14]
p4a.branch = v2024.01.21

[buildozer]

# رفع مستوى السجل لتفكيك الأخطاء بدقة
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 0