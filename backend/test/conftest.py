import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from models.repositorio import RepositorioEmMemoria
from services.cadastro_service import CadastroService


@pytest.fixture
def service():
    return CadastroService(RepositorioEmMemoria())
