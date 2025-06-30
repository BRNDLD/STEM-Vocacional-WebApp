/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock react-router-dom Link component completely
jest.mock('react-router-dom', () => ({
  Link: ({ children, to, ...props }) => <a href={to} {...props}>{children}</a>
}));

import LandingPage from '../../components/LandingPage';

describe('LandingPage Component', () => {
  test('renders landing page with title', () => {
    render(<LandingPage />);
    
    // Check if the main title is rendered
    expect(screen.getByText(/STEM Vocacional/i)).toBeInTheDocument();
  });

  test('renders all dimension cards', () => {
    render(<LandingPage />);
    
    // Check if all 4 dimension cards are present
    expect(screen.getByText(/Cognitiva/i)).toBeInTheDocument();
    expect(screen.getByText(/Educativa/i)).toBeInTheDocument();
    expect(screen.getByText(/Socioeconómica/i)).toBeInTheDocument();
    expect(screen.getByText(/Autoeficacia/i)).toBeInTheDocument();
  });

  test('renders card descriptions', () => {
    render(<LandingPage />);
    
    // Check if card descriptions are present
    expect(screen.getByText(/Evalúa tus habilidades académicas/i)).toBeInTheDocument();
    expect(screen.getByText(/Analiza tu contexto educativo/i)).toBeInTheDocument();
    expect(screen.getByText(/Comprende tu situación socioeconómica/i)).toBeInTheDocument();
    expect(screen.getByText(/Mide tu confianza en tus capacidades/i)).toBeInTheDocument();
  });

  test('component renders without crashing', () => {
    render(<LandingPage />);
    
    // Test that the main container exists
    const mainContainer = screen.getByText(/STEM Vocacional/i).closest('div');
    expect(mainContainer).toBeInTheDocument();
  });

  test('renders navigation button', () => {
    render(<LandingPage />);
    
    // Look for the "Comenzar evaluación" button or link
    const startButton = screen.getByText(/Comenzar evaluación/i);
    expect(startButton).toBeInTheDocument();
  });
});