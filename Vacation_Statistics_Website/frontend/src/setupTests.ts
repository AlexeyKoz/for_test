import '@testing-library/jest-dom';

// Polyfill ResizeObserver for Recharts' ResponsiveContainer in JSDOM
class MockResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}

(global as any).ResizeObserver = (global as any).ResizeObserver || MockResizeObserver;

// Lightly mock ResponsiveContainer to avoid ResizeObserver dependency
jest.mock('recharts', () => {
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const Original = jest.requireActual('recharts');
  // Require React inside the factory to satisfy Jest's scope rules
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const React = require('react');
  const ResponsiveContainer = ({ children }: { children: any }) =>
    React.createElement('div', { style: { width: '800px', height: '400px' } }, children);
  return { ...Original, ResponsiveContainer };
});


