import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Copy } from 'lucide-react'

type MessageProps = {
  message: {
    role: 'user' | 'assistant'
    content: string
  }
}

export default function MessageBubble({ message }: MessageProps) {
  const handleCopy = () => {
    navigator.clipboard.writeText(message.content)
  }

  return (
    <div className={`group flex flex-col gap-1.5 w-fit max-w-[80%] vend-sans 
      ${message.role === 'user' ? "ml-auto items-end" : "items-start"}`}>
      <div className={`w-full rounded-2xl px-3 py-2 shadow-sm
        ${message.role === 'user' 
          ? "bg-gradient-to-br from-orange-700/70 to-orange-800/70 border border-orange-600/10" 
          : "bg-gradient-to-br from-zinc-800/70 to-zinc-900/70 border border-zinc-700/10"
        }`}>
        <div className="prose prose-invert prose-zinc max-w-none
                      prose-p:leading-relaxed prose-p:my-1
                      prose-pre:bg-zinc-900/30 prose-pre:border prose-pre:border-zinc-800/20
                      prose-code:text-orange-300">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
      
      <button
        onClick={handleCopy}
        className="opacity-0 group-hover:opacity-100 flex items-center gap-2
                 transition-all duration-200
                 text-s px-2 py-1 hover:cursor-pointer"
      >
        <Copy size={12} />
      </button>
    </div>
  )
}
