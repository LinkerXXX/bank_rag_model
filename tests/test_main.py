import sys
import os

# --- Настройка путей для импорта ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
# -----------------------------------

def test_check_environment_runs():
    """Тест: функция запускается без ошибок"""
    try:
        from main import check_environment
        check_environment()
        assert True
    except Exception as e:
        assert False, f"Функция упала с ошибкой: {e}"

def test_python_version_is_3x():
    """Тест: версия Python 3.x"""
    assert sys.version_info.major == 3, "Требуется Python 3.x"