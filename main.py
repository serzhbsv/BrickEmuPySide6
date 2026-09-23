import sys
import os
import glob

print("[DEBUG] main.py started", flush=True)

from PySide6 import QtWidgets
print("[DEBUG] PySide6 imported", flush=True)

from ui import Window
print("[DEBUG] Window imported", flush=True)


def find_brick_files():
    """Ищет .brick файлы в директории приложения на Android"""
    search_dirs = [
        os.environ.get("ANDROID_ARGUMENT", ""),
        os.path.join(os.environ.get("ANDROID_ARGUMENT", ""), "assets"),
        os.path.join(os.environ.get("ANDROID_ARGUMENT", ""), "ui"),
        ".",
    ]
    for d in search_dirs:
        if not d:
            continue
        files = glob.glob(os.path.join(d, "*.brick"))
        if files:
            print(f"[DEBUG] Found .brick files in {d}: {files}", flush=True)
            return files
    print("[DEBUG] No .brick files found", flush=True)
    return []


def main():
    print("[DEBUG] main() called", flush=True)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("BrickEmuPy")

    window = Window()
    print("[DEBUG] Window created", flush=True)
    window.show()
    print("[DEBUG] Window shown", flush=True)

    # Автозагрузка первого .brick файла
    brick_files = find_brick_files()
    if brick_files:
        print(f"[DEBUG] Auto-loading: {brick_files[0]}", flush=True)
        window._load_game(brick_files[0])

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
