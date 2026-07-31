import React from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

// Remove model "thinking" blocks that some providers leak into the answer
function stripThinking(text) {
  if (!text) return ''
  return text
    .replace(/<think>[\s\S]*?<\/think>/gi, '')
    .replace(/<scratchpad>[\s\S]*?<\/scratchpad>/gi, '')
    .trim()
}

const components = {
  p: ({ node, ...props }) => (
    <p className="my-2 leading-relaxed" {...props} />
  ),
  h1: ({ node, ...props }) => (
    <h1 className="text-lg font-semibold mt-3 mb-2" {...props} />
  ),
  h2: ({ node, ...props }) => (
    <h2 className="text-base font-semibold mt-3 mb-2" {...props} />
  ),
  h3: ({ node, ...props }) => (
    <h3 className="text-sm font-semibold mt-3 mb-2" {...props} />
  ),
  ul: ({ node, ...props }) => (
    <ul className="list-disc pl-5 my-2 space-y-1" {...props} />
  ),
  ol: ({ node, ...props }) => (
    <ol className="list-decimal pl-5 my-2 space-y-1" {...props} />
  ),
  li: ({ node, ...props }) => <li className="leading-relaxed" {...props} />,
  strong: ({ node, ...props }) => (
    <strong className="font-semibold" {...props} />
  ),
  em: ({ node, ...props }) => <em className="italic" {...props} />,
  code: ({ node, inline, ...props }) =>
    inline ? (
      <code
        className="bg-surface/80 text-accent-muted px-1.5 py-0.5 rounded font-mono text-xs"
        {...props}
      />
    ) : (
      <code className="block bg-surface text-text-primary p-3 rounded-lg font-mono text-xs overflow-x-auto" {...props} />
    ),
  pre: ({ node, ...props }) => (
    <pre className="bg-surface border border-surface-border rounded-lg p-3 overflow-x-auto my-2" {...props} />
  ),
  blockquote: ({ node, ...props }) => (
    <blockquote className="border-l-2 border-accent/40 pl-3 italic text-text-secondary my-2" {...props} />
  ),
  a: ({ node, ...props }) => (
    <a className="text-accent hover:text-accent-hover underline underline-offset-2" {...props} />
  ),
  table: ({ node, ...props }) => (
    <div className="overflow-x-auto my-3">
      <table className="w-full text-xs border border-surface-border rounded" {...props} />
    </div>
  ),
  th: ({ node, ...props }) => (
    <th className="bg-surface-border/40 text-left font-semibold px-2 py-1 border border-surface-border" {...props} />
  ),
  td: ({ node, ...props }) => (
    <td className="px-2 py-1 border border-surface-border align-top" {...props} />
  ),
  hr: ({ node, ...props }) => (
    <hr className="my-4 border-surface-border" {...props} />
  ),
}

export default function MarkdownRenderer({ children, className = '' }) {
  return (
    <div className={`text-text-primary ${className}`}>
      <ReactMarkdown components={components} remarkPlugins={[remarkGfm]}>
        {stripThinking(children)}
      </ReactMarkdown>
    </div>
  )
}
