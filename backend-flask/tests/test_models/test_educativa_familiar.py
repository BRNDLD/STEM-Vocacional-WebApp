"""
Unit tests for RespuestaEducativaFamiliar model
"""
import pytest
from datetime import datetime, date
from app.models.models import RespuestaEducativaFamiliar, Usuario, db


class TestRespuestaEducativaFamiliar:
    """Test cases for RespuestaEducativaFamiliar model"""

    def test_create_respuesta_educativa_familiar(self, db_session, sample_usuario, sample_educativa_familiar_data):
        """Test creating a new educational family response"""
        respuesta = RespuestaEducativaFamiliar(
            id_usuario=sample_usuario.id_usuario,
            **sample_educativa_familiar_data
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_resp_edu_fam is not None
        assert respuesta.id_usuario == sample_usuario.id_usuario
        assert respuesta.colegio == sample_educativa_familiar_data['colegio']

    def test_respuesta_educativa_familiar_to_dict(self, db_session, sample_usuario, sample_educativa_familiar_data):
        """Test educational family response to_dict method"""
        respuesta = RespuestaEducativaFamiliar(
            id_usuario=sample_usuario.id_usuario,
            **sample_educativa_familiar_data,
            fecha_respuesta=datetime.now()
        )
        db_session.add(respuesta)
        db_session.commit()
        
        result = respuesta.to_dict()
        
        assert isinstance(result, dict)
        assert result['id_usuario'] == sample_usuario.id_usuario
        assert result['colegio'] == sample_educativa_familiar_data['colegio']
        assert 'fecha_respuesta' in result

    def test_respuesta_educativa_familiar_date_fields(self, db_session, sample_usuario):
        """Test date fields in educational family response"""
        fecha_grad = date(2020, 12, 15)
        now = datetime.now()
        
        respuesta = RespuestaEducativaFamiliar(
            id_usuario=sample_usuario.id_usuario,
            colegio="Test School",
            fecha_graduacion=fecha_grad,
            fecha_respuesta=now
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.fecha_graduacion == fecha_grad
        assert respuesta.fecha_respuesta == now

    def test_respuesta_educativa_familiar_optional_fields(self, db_session, sample_usuario):
        """Test that most fields are optional"""
        respuesta = RespuestaEducativaFamiliar(
            id_usuario=sample_usuario.id_usuario,
            colegio="Test School"  # Only required field
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_resp_edu_fam is not None
        assert respuesta.colegio == "Test School"
        assert respuesta.ciudad_colegio is None