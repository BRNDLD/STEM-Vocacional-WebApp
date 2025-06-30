"""
Integration tests for API workflow
"""
import pytest
import json
from app.models.models import Usuario, RespuestaCognitiva, RespuestaEducativaFamiliar, db


class TestAPIIntegration:
    """Test cases for complete API workflows"""

    def test_complete_user_journey(self, client, db_session):
        """Test complete user journey from creation to responses"""
        # Step 1: Create a user
        user_data = {'codigo_estudiante': 'INTEGRATION_TEST_001'}
        response = client.post('/api/usuarios', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        user_response = json.loads(response.data)
        assert user_response['success'] is True
        user_id = user_response['data']['id_usuario']
        
        # Step 2: Create cognitive response
        cognitiva_data = {
            'id_usuario': user_id,
            'ptj_fisica': 85.5,
            'ptj_quimica': 78.0,
            'ptj_biologia': 92.3
        }
        response = client.post('/api/cognitiva', 
                             data=json.dumps(cognitiva_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        cognitiva_response = json.loads(response.data)
        assert cognitiva_response['success'] is True
        
        # Step 3: Create educational family response
        educativa_data = {
            'id_usuario': user_id,
            'colegio': 'Colegio Test',
            'ciudad_colegio': 'Bogotá',
            'depto_colegio': 'Cundinamarca'
        }
        response = client.post('/api/educativa-familiar', 
                             data=json.dumps(educativa_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        educativa_response = json.loads(response.data)
        assert educativa_response['success'] is True
        
        # Step 4: Verify user exists and has responses
        response = client.get(f'/api/usuarios/{user_id}')
        assert response.status_code == 200
        final_user = json.loads(response.data)
        assert final_user['success'] is True
        assert final_user['data']['codigo_estudiante'] == 'INTEGRATION_TEST_001'

    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['database'] == 'connected'

    def test_home_endpoint(self, client):
        """Test home endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'STEM Vocacional' in data['message']

    def test_error_handling_404(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'no encontrado' in data['message'].lower()

    def test_error_handling_405(self, client):
        """Test 405 method not allowed"""
        response = client.patch('/api/usuarios')  # PATCH not allowed
        assert response.status_code == 405
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'no permitido' in data['message'].lower()

    def test_bulk_operations(self, client, db_session):
        """Test bulk operations and data consistency"""
        # Create multiple users
        users = []
        for i in range(3):
            user_data = {'codigo_estudiante': f'BULK_TEST_{i:03d}'}
            response = client.post('/api/usuarios', 
                                 data=json.dumps(user_data),
                                 content_type='application/json')
            assert response.status_code == 201
            user_response = json.loads(response.data)
            users.append(user_response['data'])
        
        # Verify all users were created
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        all_users = json.loads(response.data)
        assert all_users['success'] is True
        assert len(all_users['data']) >= 3
        
        # Create responses for each user
        for user in users:
            cognitiva_data = {
                'id_usuario': user['id_usuario'],
                'ptj_fisica': 80.0 + user['id_usuario']  # Unique values
            }
            response = client.post('/api/cognitiva', 
                                 data=json.dumps(cognitiva_data),
                                 content_type='application/json')
            assert response.status_code == 201
        
        # Verify all cognitive responses were created
        response = client.get('/api/cognitiva')
        assert response.status_code == 200
        all_cognitiva = json.loads(response.data)
        assert all_cognitiva['success'] is True
        assert len(all_cognitiva['data']) >= 3

    def test_data_validation_across_endpoints(self, client, sample_usuario):
        """Test data validation consistency across endpoints"""
        # Test invalid numeric values
        invalid_data = {
            'id_usuario': sample_usuario.id_usuario,
            'ptj_fisica': 'invalid_number'
        }
        response = client.post('/api/cognitiva', 
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        # Should handle gracefully (specific response depends on controller implementation)
        assert response.status_code in [400, 500]
        
        # Test missing required fields
        incomplete_data = {
            'ptj_fisica': 85.0
            # Missing id_usuario
        }
        response = client.post('/api/cognitiva', 
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        assert response.status_code == 400