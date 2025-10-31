import { useState } from 'react'
import { Send } from 'lucide-react'

type ChatInputProps = {
  onSend: (message: string) => void
  disabled?: boolean
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || disabled) return
    
    onSend(input)
    setInput('')
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 px-3 py-3 mb-2 bg-zinc-900/30 backdrop-blur-sm
                 rounded-lg border border-zinc-800/50 vend-sans">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={disabled}
        placeholder="Type your message..."
        className="flex-1 bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-2 
                   focus:outline-none focus:ring-2 focus:ring-orange-700/50 focus:border-orange-700/50
                   placeholder:text-zinc-500 text-zinc-100"
      />
      <button
        type="submit"
        disabled={disabled || !input.trim()}
        className="bg-gradient-to-r from-orange-700 to-orange-800 text-zinc-100 rounded-lg px-4 py-2 
                   disabled:opacity-50 disabled:cursor-not-allowed hover:from-orange-600 hover:to-orange-700
                   transition-all duration-200 shadow-lg"
      >
        <Send size={20} />
      </button>
    </form>
  )
}
