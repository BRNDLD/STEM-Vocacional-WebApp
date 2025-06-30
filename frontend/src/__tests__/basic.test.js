/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom';

describe('Basic React Testing', () => {
  test('can render a simple component', () => {
    const TestComponent = () => <div>Hello Test</div>;
    const { getByText } = render(<TestComponent />);
    expect(getByText('Hello Test')).toBeInTheDocument();
  });

  test('React testing library is working', () => {
    expect(true).toBe(true);
  });
});