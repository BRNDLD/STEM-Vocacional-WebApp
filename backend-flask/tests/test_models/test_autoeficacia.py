"""
Unit tests for RespuestaAutoeficacia model
"""
import pytest
from datetime import datetime
from app.models.models import RespuestaAutoeficacia, Usuario, db


class TestRespuestaAutoeficacia:
    """Test cases for RespuestaAutoeficacia model"""

    def test_create_respuesta_autoeficacia(self, db_session, sample_usuario, sample_autoeficacia_data):
        """Test creating a new self-efficacy response"""
        respuesta = RespuestaAutoeficacia(
            id_usuario=sample_usuario.id_usuario,
            **sample_autoeficacia_data
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_resp_auto is not None
        assert respuesta.id_usuario == sample_usuario.id_usuario
        assert respuesta.creditos_matriculados == sample_autoeficacia_data['creditos_matriculados']

    def test_respuesta_autoeficacia_to_dict(self, db_session, sample_usuario, sample_autoeficacia_data):
        """Test self-efficacy response to_dict method"""
        respuesta = RespuestaAutoeficacia(
            id_usuario=sample_usuario.id_usuario,
            **sample_autoeficacia_data,
            fecha_respuesta=datetime.now()
        )
        db_session.add(respuesta)
        db_session.commit()
        
        result = respuesta.to_dict()
        
        assert isinstance(result, dict)
        assert result['id_usuario'] == sample_usuario.id_usuario
        assert result['creditos_matriculados'] == sample_autoeficacia_data['creditos_matriculados']
        assert result['creditos_ganadas'] == sample_autoeficacia_data['creditos_ganadas']
        assert 'fecha_respuesta' in result

    def test_respuesta_autoeficacia_numeric_fields(self, db_session, sample_usuario):
        """Test numeric field validation"""
        respuesta = RespuestaAutoeficacia(
            id_usuario=sample_usuario.id_usuario,
            creditos_matriculados=20,
            creditos_ganadas=18,
            creditos_reprobadas=2,
            puntos_calidad_pga=75.5,
            nro_materias_aprobadas=8,
            nro_materias_reprobadas=1
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.creditos_matriculados == 20
        assert respuesta.creditos_ganadas == 18
        assert respuesta.creditos_reprobadas == 2
        assert float(respuesta.puntos_calidad_pga) == 75.5
        assert respuesta.nro_materias_aprobadas == 8
        assert respuesta.nro_materias_reprobadas == 1

    def test_respuesta_autoeficacia_string_fields(self, db_session, sample_usuario):
        """Test string field values"""
        respuesta = RespuestaAutoeficacia(
            id_usuario=sample_usuario.id_usuario,
            situacion="ACTIVO",
            estado="REGULAR"
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.situacion == "ACTIVO"
        assert respuesta.estado == "REGULAR"

    def test_respuesta_autoeficacia_optional_fields(self, db_session, sample_usuario):
        """Test that fields are optional"""
        respuesta = RespuestaAutoeficacia(
            id_usuario=sample_usuario.id_usuario,
            creditos_matriculados=15  # Only one field
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_resp_auto is not None
        assert respuesta.creditos_matriculados == 15
        assert respuesta.creditos_ganadas is None
        assert respuesta.situacion is None