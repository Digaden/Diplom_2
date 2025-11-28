import sys
import pathlib
import pytest
from utils.urls import BASE_URL  # Импортируем BASE_URL из нового модуля

# Если нужно, добавьте корень проекта в sys.path (на случай нестандартной конфигурации запуска)
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))