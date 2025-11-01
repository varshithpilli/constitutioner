import { useState, useEffect, useRef } from 'react'
import MessageBubble from '../components/MessageBubble'
import ChatInput from '../components/ChatInput'
import { Spinner } from "./ui/spinner"

type Message = {
  role: 'user' | 'assistant'
  content: string
}

type ChatProps = {
  onFirstMessage: (message: string) => void
  hasStarted: boolean
}

export default function Chat({ onFirstMessage, hasStarted }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  const handleSendMessage = async (message: string) => {
    if (!hasStarted) {
      onFirstMessage(message)
    }
    setMessages(prev => [...prev, { role: 'user', content: message }])
    setIsLoading(true)
    setIsStreaming(true)

    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: message })
      })

      const reader = response.body?.getReader()
      if (!reader) throw new Error('No reader available')

      let aiMessage = ''
      let hasReceivedContent = false

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        const chunk = new TextDecoder().decode(value)
        
        // Only process non-empty chunks
        if (chunk.trim()) {
          // Hide loading spinner when first real content arrives
          if (!hasReceivedContent) {
            setIsLoading(false)
            hasReceivedContent = true
          }
          
          aiMessage += chunk
          
          if (hasReceivedContent) {
            setMessages(prev => {
              const lastMessage = prev[prev.length - 1]
              if (lastMessage?.role === 'assistant') {
                return [...prev.slice(0, -1), { role: 'assistant', content: aiMessage }]
              } else {
                return [...prev, { role: 'assistant', content: aiMessage }]
              }
            })
          }
        }
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
      setIsStreaming(false)
    }
  }

  return (
    <div className={`relative transition-all duration-500 ease-in-out
      ${hasStarted 
        ? "h-full flex flex-col gap-2 pb-2" 
        : "h-full flex items-center justify-center"
      }`}>
      {!hasStarted && (
        <h1 className=" sm:text-3xl diplomata-sc-regular text-center tracking-wide text-zinc-100 absolute top-1/3 text-base">
          Constitutioner
        </h1>
      )}
      <div className={`transition-all duration-500 ease-in-out ${
        hasStarted 
          ? "flex-1 overflow-y-auto space-y-4 p-4" 
          : "hidden"
      }`}>
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}
        {isLoading && (
          <div className="flex items-center gap-2 text-zinc-400 pl-4">
            <Spinner className="h-4 w-4" />
            <span className="text-sm">AI is thinking...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className={`transition-all duration-500 ease-in-out ${
        hasStarted ? "" : "w-[600px]"
      }`}>
        <ChatInput onSend={handleSendMessage} disabled={isStreaming} />
      </div>
    </div>
  )
}
