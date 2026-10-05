import React, { useMemo } from 'react';
import katex from 'katex';

/**
 * KaTeXRenderer renders mathematical formulas safely with katex.
 * Handles strings that contain $$ ... $$ (display), $ ... $ (inline),
 * or pure LaTeX equations.
 */
export default function KaTeXRenderer({ math, block = false, className = '' }) {
  const renderedHtml = useMemo(() => {
    if (!math) return null;

    let text = String(math).trim();
    if (!text) return null;

    // Check if it's already wrapped in $$ or $
    let isBlock = block;
    if (text.startsWith('$$') && text.endsWith('$$')) {
      text = text.slice(2, -2).trim();
      isBlock = true;
    } else if (text.startsWith('$') && text.endsWith('$')) {
      text = text.slice(1, -1).trim();
    }

    try {
      return katex.renderToString(text, {
        displayMode: isBlock,
        throwOnError: false,
        strict: false
      });
    } catch (err) {
      console.warn('KaTeX render error:', err);
      return `<code class="text-amber-400 font-mono text-xs">${text}</code>`;
    }
  }, [math, block]);

  if (!renderedHtml) return null;

  return (
    <div
      className={`katex-wrapper ${block ? 'my-2 overflow-x-auto py-1 text-center' : 'inline-block align-middle'} ${className}`}
      dangerouslySetInnerHTML={{ __html: renderedHtml }}
    />
  );
}
