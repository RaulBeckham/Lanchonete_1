def test_deve_cancelar_pedido_com_sucesso(client):
    client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 1, "desconto_percentual": 10.0})

    pedido_response = client.post(
        "/lanchonete/pedidos",
        json={"cpf": "11122233344", "cod_produto": 1, "qtd_max_produtos": 10}
    )
    assert pedido_response.status_code == 200
    cod_pedido = pedido_response.json()["codigo"]

    response = client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    assert response.status_code == 200

    data = response.json()
    assert data["ok"] is True
    assert data["mensagem"] == "Pedido cancelado com sucesso"

def test_nao_deve_cancelar_pedido_inexistente(client):
    response = client.post("/lanchonete/pedidos/999/cancelar")

    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "Pedido não encontrado ou não pode ser cancelado"

def test_nao_deve_cancelar_pedido_finalizado(client):
    client.post("/clientes", json={"cpf": "22233344455", "nome": "Cliente Y"})
    client.post("/produtos", json={"codigo": 2, "valor": 20.0, "tipo": 2, "desconto_percentual": 0.0})

    pedido_response = client.post(
        "/lanchonete/pedidos",
        json={"cpf": "22233344455", "cod_produto": 2, "qtd_max_produtos": 10}
    )
    assert pedido_response.status_code == 200
    cod_pedido = pedido_response.json()["codigo"]

    finalizar_response = client.post(f"/lanchonete/pedidos/{cod_pedido}/finalizar")
    assert finalizar_response.status_code == 200

    response = client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Pedido não encontrado ou não pode ser cancelado"

def test_deve_listar_pedidos_cancelados(client):
    client.post("/clientes", json={"cpf": "33344455566", "nome": "Cliente Z"})
    client.post("/produtos", json={"codigo": 3, "valor": 15.0, "tipo": 1, "desconto_percentual": 5.0})

    pedido_response = client.post(
        "/lanchonete/pedidos",
        json={"cpf": "33344455566", "cod_produto": 3, "qtd_max_produtos": 10}
    )
    assert pedido_response.status_code == 200
    cod_pedido = pedido_response.json()["codigo"]

    cancelar_response = client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")
    assert cancelar_response.status_code == 200

    response = client.get("/lanchonete/pedidos/cancelados")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["esta_cancelado"] is True