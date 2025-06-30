"""
Unit tests for RespuestaCognitiva model
"""
import pytest
from datetime import datetime
from app.models.models import RespuestaCognitiva, Usuario, db


class TestRespuestaCognitiva:
    """Test cases for RespuestaCognitiva model"""

    def test_create_respuesta_cognitiva(self, db_session, sample_usuario, sample_cognitiva_data):
        """Test creating a new cognitive response"""
        respuesta = RespuestaCognitiva(
            id_usuario=sample_usuario.id_usuario,
            **sample_cognitiva_data
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_resp_cognitiva is not None
        assert respuesta.id_usuario == sample_usuario.id_usuario
        assert float(respuesta.ptj_fisica) == sample_cognitiva_data['ptj_fisica']

    def test_respuesta_cognitiva_to_dict(self, db_session, sample_usuario, sample_cognitiva_data):
        """Test cognitive response to_dict method"""
        respuesta = RespuestaCognitiva(
            id_usuario=sample_usuario.id_usuario,
            **sample_cognitiva_data,
            fecha_respuesta=datetime.now()
        )
        db_session.add(respuesta)
        db_session.commit()
        
        result = respuesta.to_dict()
        
        assert isinstance(result, dict)
        assert result['id_usuario'] == sample_usuario.id_usuario
        assert result['ptj_fisica'] == sample_cognitiva_data['ptj_fisica']
        assert result['ptj_quimica'] == sample_cognitiva_data['ptj_quimica']
        assert 'fecha_respuesta' in result

    def test_respuesta_cognitiva_foreign_key(self, db_session, sample_cognitiva_data):
        """Test foreign key relationship with existing user"""
        # First create a user
        usuario = Usuario(codigo_estudiante="TEST_FK_USER")
        db_session.add(usuario)
        db_session.commit()
        
        # Create response with valid foreign key
        respuesta = RespuestaCognitiva(
            id_usuario=usuario.id_usuario,
            **sample_cognitiva_data
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_usuario == usuario.id_usuario

    def test_respuesta_cognitiva_numeric_fields(self, db_session, sample_usuario):
        """Test numeric field validation"""
        respuesta = RespuestaCognitiva(
            id_usuario=sample_usuario.id_usuario,
            ptj_fisica=95.5,
            ptj_quimica=88.2,
            ecaes=75.0
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert float(respuesta.ptj_fisica) == 95.5
        assert float(respuesta.ptj_quimica) == 88.2
        assert float(respuesta.ecaes) == 75.0

    def test_respuesta_cognitiva_optional_fields(self, db_session, sample_usuario):
        """Test that most fields are optional"""
        respuesta = RespuestaCognitiva(
            id_usuario=sample_usuario.id_usuario,
            ptj_fisica=85.0  # Only one field
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_resp_cognitiva is not None
        assert float(respuesta.ptj_fisica) == 85.0
        assert respuesta.ptj_quimica is None

    def test_respuesta_cognitiva_dates(self, db_session, sample_usuario):
        """Test date fields"""
        now = datetime.now()
        respuesta = RespuestaCognitiva(
            id_usuario=sample_usuario.id_usuario,
            ptj_fisica=85.0,
            fecha_respuesta=now,
            fecha_actualizacion=now
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.fecha_respuesta == now
        assert respuesta.fecha_actualizacion == now