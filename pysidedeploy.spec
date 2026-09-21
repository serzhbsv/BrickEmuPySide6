[app]
# Название приложения
title = BrickEmu
# Директория проекта (родительская для main.py)
project_dir = .
# Главный файл
input_file = main.py
# Куда складывать результат
exec_directory = .
# Иконка
icon = assets/icon.png

[python]
# Путь к Python (в CI подставится автоматически)
python_path =
# Пакеты для Android
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]
# QML файлы (если есть — добавь через запятую)
qml_files =
# Исключённые QML плагины
excluded_qml_plugins =
# Qt плагины (для Android не обязательно)
plugins =

[android]
# Пути к колёсам (подставляются через --wheel-pyside и --wheel-shiboken)
wheel_pyside =
# Плагины для копирования в libs
plugins =

[buildozer]
# Режим сборки: debug или release
mode = debug
# Директория recipe (оставь пустой)
recipe_dir =
# Доп. JAR файлы
jars_dir =
