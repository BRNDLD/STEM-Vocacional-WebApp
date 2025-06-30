"""
Unit tests for RespuestaSocioeconomica model
"""
import pytest
from datetime import datetime
from app.models.models import RespuestaSocioeconomica, Usuario, db


class TestRespuestaSocioeconomica:
    """Test cases for RespuestaSocioeconomica model"""

    def test_create_respuesta_socioeconomica(self, db_session, sample_usuario, sample_socioeconomica_data):
        """Test creating a new socioeconomic response"""
        respuesta = RespuestaSocioeconomica(
            id_usuario=sample_usuario.id_usuario,
            **sample_socioeconomica_data
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_resp_socio is not None
        assert respuesta.id_usuario == sample_usuario.id_usuario
        assert respuesta.estrato == sample_socioeconomica_data['estrato']

    def test_respuesta_socioeconomica_to_dict(self, db_session, sample_usuario, sample_socioeconomica_data):
        """Test socioeconomic response to_dict method"""
        respuesta = RespuestaSocioeconomica(
            id_usuario=sample_usuario.id_usuario,
            **sample_socioeconomica_data,
            fecha_respuesta=datetime.now()
        )
        db_session.add(respuesta)
        db_session.commit()
        
        result = respuesta.to_dict()
        
        assert isinstance(result, dict)
        assert result['id_usuario'] == sample_usuario.id_usuario
        assert result['estrato'] == sample_socioeconomica_data['estrato']
        assert result['becas'] == sample_socioeconomica_data['becas']
        assert 'fecha_respuesta' in result

    def test_respuesta_socioeconomica_optional_fields(self, db_session, sample_usuario):
        """Test that most fields are optional"""
        respuesta = RespuestaSocioeconomica(
            id_usuario=sample_usuario.id_usuario,
            estrato="2"  # Only one field
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.id_resp_socio is not None
        assert respuesta.estrato == "2"
        assert respuesta.becas is None

    def test_respuesta_socioeconomica_all_fields(self, db_session, sample_usuario):
        """Test creating response with all fields"""
        now = datetime.now()
        respuesta = RespuestaSocioeconomica(
            id_usuario=sample_usuario.id_usuario,
            estrato="3",
            becas="Beca Ejemplo",
            ceres="Ceres Test",
            periodo_ingreso="202301",
            tipo_estudiante="PRIMERA VEZ",
            fecha_respuesta=now,
            fecha_actualizacion=now
        )
        db_session.add(respuesta)
        db_session.commit()
        
        assert respuesta.estrato == "3"
        assert respuesta.becas == "Beca Ejemplo"
        assert respuesta.ceres == "Ceres Test"
        assert respuesta.periodo_ingreso == "202301"
        assert respuesta.tipo_estudiante == "PRIMERA VEZ"
        assert respuesta.fecha_respuesta == now
        assert respuesta.fecha_actualizacion == now