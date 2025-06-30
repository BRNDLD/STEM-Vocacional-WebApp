"""
Unit tests for Usuario model
"""
import pytest
from app.models.models import Usuario, db


class TestUsuario:
    """Test cases for Usuario model"""

    def test_create_usuario(self, db_session):
        """Test creating a new usuario"""
        usuario = Usuario(codigo_estudiante="TEST001")
        db_session.add(usuario)
        db_session.commit()
        
        assert usuario.id_usuario is not None
        assert usuario.codigo_estudiante == "TEST001"

    def test_usuario_unique_constraint(self, db_session):
        """Test that codigo_estudiante must be unique"""
        # Create first usuario
        usuario1 = Usuario(codigo_estudiante="TEST001")
        db_session.add(usuario1)
        db_session.commit()
        
        # Try to create another with same codigo_estudiante
        usuario2 = Usuario(codigo_estudiante="TEST001")
        db_session.add(usuario2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_usuario_to_dict(self, db_session):
        """Test usuario to_dict method"""
        usuario = Usuario(codigo_estudiante="TEST001")
        db_session.add(usuario)
        db_session.commit()
        
        result = usuario.to_dict()
        
        assert isinstance(result, dict)
        assert result['id_usuario'] == usuario.id_usuario
        assert result['codigo_estudiante'] == "TEST001"

    def test_usuario_codigo_estudiante_required(self, db_session):
        """Test that codigo_estudiante is required"""
        usuario = Usuario()  # No codigo_estudiante
        db_session.add(usuario)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_usuario_string_representation(self, db_session):
        """Test usuario string representation"""
        usuario = Usuario(codigo_estudiante="TEST001")
        db_session.add(usuario)
        db_session.commit()
        
        # Even without __str__ method, should be able to convert to string
        assert str(usuario) is not None