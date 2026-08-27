[app]
title = منظومة 2600
package.name = truckapp2600
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,ttf

version = 1.0.0

# كافة شاشات المشروع والمكتبات المطلوبة للتشغيل ودعم العربية
requirements = python3,kivy,arabic_reshaper,python-bidi,requests

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_build_errors = 1