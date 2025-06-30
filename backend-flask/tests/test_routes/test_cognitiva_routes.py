"""
Integration tests for Cognitiva routes
"""
import pytest
import json
from app.models.models import Usuario, RespuestaCognitiva, db


class TestCognitivaRoutes:
    """Test cases for Cognitiva API routes"""

    def test_get_all_cognitiva_empty(self, client):
        """Test getting all cognitive responses when none exist"""
        response = client.get('/api/cognitiva')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data'] == []

    def test_create_cognitiva_success(self, client, sample_usuario, sample_cognitiva_data):
        """Test creating a new cognitive response successfully"""
        data = {
            'id_usuario': sample_usuario.id_usuario,
            **sample_cognitiva_data
        }
        response = client.post('/api/cognitiva', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['data']['id_usuario'] == sample_usuario.id_usuario

    def test_create_cognitiva_missing_usuario(self, client, sample_cognitiva_data):
        """Test creating cognitive response without user ID"""
        data = sample_cognitiva_data  # No id_usuario
        response = client.post('/api/cognitiva', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False

    def test_create_cognitiva_invalid_usuario(self, client, sample_cognitiva_data):
        """Test creating cognitive response with non-existing user"""
        data = {
            'id_usuario': 99999,  # Non-existing user
            **sample_cognitiva_data
        }
        response = client.post('/api/cognitiva', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False

    def test_update_cognitiva_success(self, client, db_session, sample_usuario, sample_cognitiva_data):
        """Test updating an existing cognitive response"""
        # Create initial response
        respuesta = RespuestaCognitiva(
            id_usuario=sample_usuario.id_usuario,
            ptj_fisica=80.0
        )
        db_session.add(respuesta)
        db_session.commit()
        
        # Update with new data
        updated_data = {
            'id_usuario': sample_usuario.id_usuario,
            'ptj_fisica': 90.0,
            'ptj_quimica': 85.0
        }
        response = client.post('/api/cognitiva', 
                             data=json.dumps(updated_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['success'] is True

    def test_get_all_cognitiva_with_data(self, client, db_session):
        """Test getting all cognitive responses with data"""
        # Create test users and responses
        usuarios = [
            Usuario(codigo_estudiante='TEST001'),
            Usuario(codigo_estudiante='TEST002')
        ]
        
        for usuario in usuarios:
            db_session.add(usuario)
        db_session.commit()
        
        # Create cognitive responses
        respuestas = [
            RespuestaCognitiva(id_usuario=usuarios[0].id_usuario, ptj_fisica=85.0),
            RespuestaCognitiva(id_usuario=usuarios[1].id_usuario, ptj_fisica=90.0)
        ]
        
        for respuesta in respuestas:
            db_session.add(respuesta)
        db_session.commit()
        
        response = client.get('/api/cognitiva')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']) == 2

    def test_create_cognitiva_partial_data(self, client, sample_usuario):
        """Test creating cognitive response with partial data"""
        data = {
            'id_usuario': sample_usuario.id_usuario,
            'ptj_fisica': 85.5,
            'ptj_quimica': 78.0
            # Only some fields
        }
        response = client.post('/api/cognitiva', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['data']['ptj_fisica'] == 85.5
        assert response_data['data']['ptj_quimica'] == 78.0

    def test_invalid_json_cognitiva(self, client):
        """Test sending invalid JSON to cognitive endpoint"""
        response = client.post('/api/cognitiva', 
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400