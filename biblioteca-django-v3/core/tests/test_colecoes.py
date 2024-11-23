import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Colecao, Livro, Autor, Categoria

@pytest.fixture
def autor(db):
    return Autor.objects.create(nome='Autor Teste')

@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nome='Categoria Teste')

@pytest.fixture
def usuario1(db):
    return User.objects.create_user(username='user1', password='password123')

@pytest.fixture
def usuario2(db):
    return User.objects.create_user(username='user2', password='password456')

@pytest.fixture
def livro(db, autor, categoria):
    return Livro.objects.create(titulo='Livro Teste', autor=autor, categoria=categoria, publicado_em='2024-01-01')

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def colecao_usuario1(db, usuario1, livro):
    colecao = Colecao.objects.create(nome='Coleção do User1', colecionador=usuario1)
    colecao.livros.add(livro)
    return colecao

@pytest.mark.django_db
def test_criar_colecao_usuario_autenticado(client, usuario1, livro):
    client.force_authenticate(user=usuario1)
    data = {
        'nome': 'Minha Coleção',
        'descricao': 'Descrição da coleção',
        'livros': [livro.id]
    }
    response = client.post('/colecoes/', data)
    print(response.data) 
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['colecionador'] == usuario1.id  # Confirme se o campo 'colecionador' existe

@pytest.mark.django_db
def test_criar_colecao_usuario_nao_autenticado(client, livro):
    data = {
        'nome': 'Coleção não autenticada',
        'descricao': 'Descrição',
        'livros': [livro.id]
    }
    response = client.post('/colecoes/', data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_editar_colecao_apenas_do_colecionador(client, usuario1, usuario2, colecao_usuario1):
    # Tentar editar como outro usuário
    client.force_authenticate(user=usuario2)
    data = {'nome': 'Tentativa de edição'}
    response = client.patch(f'/colecoes/{colecao_usuario1.id}/', data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Editar como colecionador
    client.force_authenticate(user=usuario1)
    data = {'nome': 'Nova Coleção'}
    response = client.patch(f'/colecoes/{colecao_usuario1.id}/', data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['nome'] == 'Nova Coleção'

@pytest.mark.django_db
def test_listagem_colecoes_usuario_autenticado(client, usuario1, colecao_usuario1):
    client.force_authenticate(user=usuario1)
    response = client.get('/colecoes/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_deletar_colecao_apenas_do_colecionador(client, usuario1, usuario2, colecao_usuario1):
    # Tentar deletar como outro usuário
    client.force_authenticate(user=usuario2)
    response = client.delete(f'/colecoes/{colecao_usuario1.id}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Deletar como colecionador
    client.force_authenticate(user=usuario1)
    response = client.delete(f'/colecoes/{colecao_usuario1.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
