"""
Test configuration and fixtures for STEM Vocacional WebApp
"""
import pytest
import os
import tempfile
import sys

# Add the backend-flask directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_app import create_test_app
from app.models.models import db, Usuario, RespuestaCognitiva, RespuestaEducativa, RespuestaEducativaFamiliar, RespuestaSocioeconomica, RespuestaAutoeficacia
from datetime import datetime


@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    # Create a temporary file for test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    try:
        app = create_test_app(database_uri=f'sqlite:///{db_path}')
        
        # Create the database and tables
        with app.app_context():
            db.create_all()
            yield app
            
    finally:
        # Clean up
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Create a fresh database session for each test."""
    with app.app_context():
        # Clear all tables
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def sample_usuario(db_session):
    """Create a sample user for testing."""
    usuario = Usuario(codigo_estudiante="TEST_USER_001")
    db_session.add(usuario)
    db_session.commit()
    return usuario


@pytest.fixture
def sample_cognitiva_data():
    """Sample data for cognitive responses."""
    return {
        'ptj_fisica': 85.5,
        'ptj_quimica': 78.0,
        'ptj_biologia': 92.3,
        'ptj_matematicas': 88.7,
        'ptj_geografia': 75.2,
        'ptj_historia': 82.1,
        'ptj_filosofia': 79.5,
        'ptj_sociales_ciudadano': 83.2,
        'ptj_ciencias_sociales': 86.4,
        'ptj_lenguaje': 89.3,
        'ptj_lectura_critica': 87.6,
        'ptj_ingles': 72.8,
        'ecaes': 91.2,
        'pga_acumulado': 4.2,
        'promedio_periodo': 4.0
    }


@pytest.fixture
def sample_educativa_data():
    """Sample data for educational responses."""
    return {
        'puntaje_educacion': 4.5,
        'nivel_educativo': 'Universitario',
        'institucion': 'Universidad Nacional'
    }


@pytest.fixture
def sample_educativa_familiar_data():
    """Sample data for educational family responses."""
    return {
        'colegio': 'Colegio San Patricio',
        'ciudad_colegio': 'Bogotá',
        'depto_colegio': 'Cundinamarca',
        'municipio_colegio': 'Bogotá D.C.',
        'fecha_graduacion': '2020-12-15'
    }


@pytest.fixture
def sample_socioeconomica_data():
    """Sample data for socioeconomic responses."""
    return {
        'estrato': '3',
        'becas': 'Ninguna',
        'ceres': 'No',
        'periodo_ingreso': '2023-1',
        'tipo_estudiante': 'Pregrado'
    }


@pytest.fixture
def sample_autoeficacia_data():
    """Sample data for self-efficacy responses."""
    return {
        'creditos_matriculados': 18,
        'creditos_ganadas': 15,
        'creditos_reprobadas': 3,
        'puntos_calidad_pga': 65.5,
        'situacion': 'Activo',
        'estado': 'Regular',
        'nro_materias_aprobadas': 5,
        'nro_materias_reprobadas': 1
    }


@pytest.fixture
def authenticated_headers():
    """Headers for authenticated requests."""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


@pytest.fixture
def api_base_url():
    """Base URL for API endpoints."""
    return '/api'