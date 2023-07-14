import App from './components/App.js';
import React from 'react';
import { createRoot } from 'react-dom/client';

// ReactDom.render is deprecated in react 18

// this is a good way to render elements
const root = createRoot(document.getElementById('root'));
root.render( 
    <React.StrictMode>
    <App />
    </React.StrictMode>
);