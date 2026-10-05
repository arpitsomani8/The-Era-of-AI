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

/**
 * MathText renders text containing inline LaTeX expressions wrapped in $...$
 * as rich KaTeX formulas, while keeping the rest as regular text.
 */
export function MathText({ text, className = '' }) {
  if (!text) return null;
  const str = String(text);

  // If no math markers, render as-is
  if (!str.includes('$')) {
    return <span className={className}>{str}</span>;
  }

  // Split string by $ delimiters
  const segments = str.split('$');

  return (
    <span className={className}>
      {segments.map((segment, index) => {
        // Odd index means it was inside $...$
        if (index % 2 === 1) {
          if (!segment.trim()) return null;
          return (
            <KaTeXRenderer
              key={index}
              math={segment}
              block={false}
              className="inline-math px-0.5"
            />
          );
        }
        return segment;
      })}
    </span>
  );
}
