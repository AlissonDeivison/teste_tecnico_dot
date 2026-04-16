"""
Testes de integração para os endpoints de livros.
Testa o fluxo completo: requisição -> endpoint -> service -> repository -> banco.
"""

class TestCreateBook:
    """Testes para POST /api/v1/books/"""

    def test_create_book_success(self, client):
        """Deve cadastrar um livro com sucesso."""
        book_data = {
            "titulo": "O Avesso da Pele",
            "autor": "Jeferson Tenório",
            "data_publicacao": "2020-08-20",
            "resumo": "Uma narrativa contundente sobre relações familiares, identidade e racismo estrutural no Brasil."
        }

        response = client.post("/api/v1/books/", json=book_data)

        assert response.status_code == 201
        data = response.json()
        assert data["titulo"] == book_data["titulo"]
        assert data["autor"] == book_data["autor"]
        assert "id" in data  # UUID gerado automaticamente

    def test_create_book_without_resumo(self, client):
        """Deve cadastrar livro sem resumo (campo opcional)."""
        book_data = {
            "titulo": "Salvar o Fogo",
            "autor": "Itamar Vieira Junior",
            "data_publicacao": "2023-04-14"
        }

        response = client.post("/api/v1/books/", json=book_data)

        assert response.status_code == 201
        assert response.json()["resumo"] is None

    def test_create_book_invalid_data(self, client):
        """Deve retornar 422 para dados inválidos."""
        book_data = {
            "titulo": "",  # Título vazio não permitido
            "autor": "Aline Bei",
            "data_publicacao": "2021-01-01"
        }

        response = client.post("/api/v1/books/", json=book_data)

        assert response.status_code == 422


class TestSearchByTitulo:
    """Testes para GET /api/v1/books/search/titulo"""

    def test_search_by_titulo_found(self, client):
        """Deve encontrar livros pelo título."""
        # Cadastra livro primeiro
        client.post("/api/v1/books/", json={
            "titulo": "Torto Arado",
            "autor": "Itamar Vieira Junior",
            "data_publicacao": "2019-08-16"
        })

        response = client.get("/api/v1/books/search/titulo?titulo=Torto")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Torto" in data[0]["titulo"]

    def test_search_by_titulo_not_found(self, client):
        """Deve retornar lista vazia se não encontrar."""
        response = client.get("/api/v1/books/search/titulo?titulo=NaoExiste")

        assert response.status_code == 200
        assert response.json() == []

    def test_search_by_titulo_pagination(self, client):
        """Deve respeitar paginação."""
        # Cadastra 3 livros
        for i in range(3):
            client.post("/api/v1/books/", json={
                "titulo": f"A Pediatra {i}",
                "autor": "Andréa del Fuego",
                "data_publicacao": "2021-08-15"
            })

        response = client.get("/api/v1/books/search/titulo?titulo=Pediatra&limit=2")

        assert response.status_code == 200
        assert len(response.json()) == 2


class TestSearchByAutor:
    """Testes para GET /api/v1/books/search/autor"""

    def test_search_by_autor_found(self, client):
        """Deve encontrar livros pelo autor."""
        client.post("/api/v1/books/", json={
            "titulo": "Tudo é Rio",
            "autor": "Carla Madeira",
            "data_publicacao": "2014-04-10"
        })

        response = client.get("/api/v1/books/search/autor?autor=Madeira")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Madeira" in data[0]["autor"]

    def test_search_by_autor_case_insensitive(self, client):
        """Busca deve ser case-insensitive."""
        client.post("/api/v1/books/", json={
            "titulo": "O Som do Rugido da Onça",
            "autor": "Micheliny Verunschk",
            "data_publicacao": "2021-02-12"
        })

        response = client.get("/api/v1/books/search/autor?autor=micheliny verunschk")

        assert response.status_code == 200
        assert len(response.json()) == 1