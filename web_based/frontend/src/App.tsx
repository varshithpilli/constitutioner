import { useState } from 'react'
import Chat from './components/Chat'



export default function App() {
  const [hasStarted, setHasStarted] = useState(false)

  const handleFirstMessage = (message: string) => {
    setHasStarted(true)
    console.log(message);
  }

  return (

    <div className="min-h-screen w-full relative">
  {/* Background gradient at bottom */}
  <div className="absolute inset-0 bg-gradient-to-b from-zinc-900 to-zinc-950 -z-10" />

  {/* Grid overlay */}
  <div
    className="absolute inset-0 pointer-events-none z-0"
    style={{
      backgroundImage: `
        linear-gradient(to right, rgba(211, 211, 211, 0.1) 0.1px, transparent 1px),
        linear-gradient(to bottom, rgba(211, 211, 211, 0.1) 0.1px, transparent 1px)
      `,
      backgroundSize: "90px 90px",
    }}
  />

  {/* Main content (header + chat) */}
  <div className="relative min-h-screen h-screen overflow-hidden text-zinc-100">
    <header
      className={`relative border-b border-zinc-800/50 p-4 backdrop-blur-sm bg-zinc-900/30
        transition-all duration-500 ease-in-out ${!hasStarted && 'opacity-0'}`}
    >
      <h1 className="text-xl font-light text-center tracking-wide text-zinc-100 diplomata-sc-regular">
        Constitutioner
      </h1>
    </header>

    <main className="mx-auto w-[95%] sm:w-[85%] md:w-[75%] lg:w-[65%] h-[calc(100%-4rem)] relative">
      <Chat onFirstMessage={handleFirstMessage} hasStarted={hasStarted} />
    </main>
  </div>
</div>


  )
}
