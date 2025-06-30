"""
Integration tests for Usuario routes
"""
import pytest
import json
from app.models.models import Usuario, db


class TestUsuarioRoutes:
    """Test cases for Usuario API routes"""

    def test_get_all_usuarios_empty(self, client):
        """Test getting all users when none exist"""
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data'] == []
        assert data['count'] == 0

    def test_create_usuario_success(self, client):
        """Test creating a new user successfully"""
        data = {'codigo_estudiante': 'TEST001'}
        response = client.post('/api/usuarios', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['data']['codigo_estudiante'] == 'TEST001'

    def test_create_usuario_missing_codigo(self, client):
        """Test creating user without codigo_estudiante"""
        data = {}
        response = client.post('/api/usuarios', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False

    def test_create_usuario_duplicate_codigo(self, client, db_session):
        """Test creating user with duplicate codigo_estudiante"""
        # Create first user
        usuario = Usuario(codigo_estudiante='TEST001')
        db_session.add(usuario)
        db_session.commit()
        
        # Try to create another with same codigo
        data = {'codigo_estudiante': 'TEST001'}
        response = client.post('/api/usuarios', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 409  # Conflict
        response_data = json.loads(response.data)
        assert response_data['success'] is False

    def test_get_usuario_by_id_success(self, client, sample_usuario):
        """Test getting user by ID successfully"""
        response = client.get(f'/api/usuarios/{sample_usuario.id_usuario}')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['data']['id_usuario'] == sample_usuario.id_usuario

    def test_get_usuario_by_id_not_found(self, client):
        """Test getting user by non-existing ID"""
        response = client.get('/api/usuarios/99999')
        
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False

    def test_get_usuario_by_codigo_success(self, client, sample_usuario):
        """Test getting user by codigo successfully"""
        response = client.get(f'/api/usuarios/codigo/{sample_usuario.codigo_estudiante}')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['data']['codigo_estudiante'] == sample_usuario.codigo_estudiante

    def test_get_usuario_by_codigo_not_found(self, client):
        """Test getting user by non-existing codigo"""
        response = client.get('/api/usuarios/codigo/NONEXISTENT')
        
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False

    def test_delete_usuario_success(self, client, sample_usuario):
        """Test deleting user successfully"""
        response = client.delete(f'/api/usuarios/{sample_usuario.id_usuario}')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True

    def test_delete_usuario_not_found(self, client):
        """Test deleting non-existing user"""
        response = client.delete('/api/usuarios/99999')
        
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False

    def test_get_all_usuarios_with_data(self, client, db_session):
        """Test getting all users when data exists"""
        # Create test users
        usuarios = [
            Usuario(codigo_estudiante='TEST001'),
            Usuario(codigo_estudiante='TEST002'),
            Usuario(codigo_estudiante='TEST003')
        ]
        
        for usuario in usuarios:
            db_session.add(usuario)
        db_session.commit()
        
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']) == 3
        assert data['count'] == 3

    def test_invalid_json_request(self, client):
        """Test sending invalid JSON"""
        response = client.post('/api/usuarios', 
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400