import pytest
from domain.produto import Produto
from domain.cliente import Cliente

def test_produto_valor_negativo():
    with pytest.raises(ValueError):
        Produto(codigo=1, valor=-5, tipo=1)


def test_post_cliente_com_cpf_vazio(client):
    r = client.post("/cliente", json={"cpf": "", "nome": "X"})
    assert r.status_code == 400