"use client";

import ReactMarkdown from "react-markdown";

export function MarkdownRenderer({ content }: { content: string }) {
  return (
    <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-a:text-brand-600 dark:prose-headings:text-white dark:prose-p:text-zinc-300 dark:prose-a:text-blue-400">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}
