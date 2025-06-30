/**
 * @jest-environment jsdom
 */
import { login, getCuestionario, saveCuestionario, getDashboard } from '../../api';

// Mock fetch globally
global.fetch = jest.fn();

describe('API Service Functions', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  describe('login function', () => {
    test('should make POST request to login endpoint', async () => {
      const mockResponse = { success: true, user: { id: 1, codigo: 'TEST001' } };
      fetch.mockResolvedValueOnce({
        json: async () => mockResponse
      });

      const result = await login('TEST001');

      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ codigo_estudiante: 'TEST001' })
      });
      expect(result).toEqual(mockResponse);
    });

    test('should handle login errors', async () => {
      const mockError = { success: false, message: 'Invalid credentials' };
      fetch.mockResolvedValueOnce({
        json: async () => mockError
      });

      const result = await login('INVALID');
      expect(result).toEqual(mockError);
    });
  });

  describe('getCuestionario function', () => {
    test('should make GET request to cuestionario endpoint', async () => {
      const mockResponse = { success: true, dimensions: [] };
      fetch.mockResolvedValueOnce({
        json: async () => mockResponse
      });

      const result = await getCuestionario('TEST001');

      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/cuestionario?codigo_estudiante=TEST001', {
        credentials: 'include'
      });
      expect(result).toEqual(mockResponse);
    });

    test('should handle special characters in codigo_estudiante', async () => {
      const mockResponse = { success: true, dimensions: [] };
      fetch.mockResolvedValueOnce({
        json: async () => mockResponse
      });

      await getCuestionario('TEST@001');

      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/cuestionario?codigo_estudiante=TEST%40001', {
        credentials: 'include'
      });
    });
  });

  describe('saveCuestionario function', () => {
    test('should make POST request to save cuestionario', async () => {
      const mockResponse = { success: true, message: 'Saved successfully' };
      const respuestas = { cognitiva: { ptj_fisica: 85 } };
      
      fetch.mockResolvedValueOnce({
        json: async () => mockResponse
      });

      const result = await saveCuestionario('TEST001', respuestas);

      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/cuestionario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ codigo_estudiante: 'TEST001', respuestas })
      });
      expect(result).toEqual(mockResponse);
    });

    test('should handle save errors', async () => {
      const mockError = { success: false, message: 'Validation error' };
      fetch.mockResolvedValueOnce({
        json: async () => mockError
      });

      const result = await saveCuestionario('TEST001', {});
      expect(result).toEqual(mockError);
    });
  });

  describe('getDashboard function', () => {
    test('should make GET request to dashboard endpoint', async () => {
      const mockResponse = { success: true, data: { stats: {} } };
      fetch.mockResolvedValueOnce({
        json: async () => mockResponse
      });

      const result = await getDashboard('TEST001');

      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/dashboard?codigo_estudiante=TEST001', {
        credentials: 'include'
      });
      expect(result).toEqual(mockResponse);
    });

    test('should handle network errors', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));

      await expect(getDashboard('TEST001')).rejects.toThrow('Network error');
    });
  });

  describe('Error handling', () => {
    test('should handle fetch failures gracefully', async () => {
      fetch.mockRejectedValueOnce(new Error('Fetch failed'));

      await expect(login('TEST001')).rejects.toThrow('Fetch failed');
    });

    test('should handle invalid JSON responses', async () => {
      fetch.mockResolvedValueOnce({
        json: async () => { throw new Error('Invalid JSON'); }
      });

      await expect(login('TEST001')).rejects.toThrow('Invalid JSON');
    });
  });
});