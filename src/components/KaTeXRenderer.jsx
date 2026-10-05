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

  if (!str.includes('$')) {
    return <span className={className}>{str}</span>;
  }

  // Match $$...$$ (block math) first, then $...$ (inline math)
  const regex = /(\$\$[\s\S]*?\$\$|\$[^\$\n]+?\$)/g;
  const parts = [];
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(str)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: 'text', content: str.slice(lastIndex, match.index) });
    }
    const token = match[0];
    if (token.startsWith('$$') && token.endsWith('$$')) {
      parts.push({ type: 'block', content: token.slice(2, -2) });
    } else {
      parts.push({ type: 'inline', content: token.slice(1, -1) });
    }
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < str.length) {
    parts.push({ type: 'text', content: str.slice(lastIndex) });
  }

  return (
    <span className={className}>
      {parts.map((p, i) => {
        if (p.type === 'block') {
          return <KaTeXRenderer key={i} math={p.content} block={true} />;
        }
        if (p.type === 'inline') {
          return <KaTeXRenderer key={i} math={p.content} block={false} className="inline-math px-0.5" />;
        }
        return <span key={i}>{p.content}</span>;
      })}
    </span>
  );
}
