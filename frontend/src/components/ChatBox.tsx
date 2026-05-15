"use client";

import { useChat } from "ai/react";
import ReactMarkdown from "react-markdown";
import { Agent } from "@/lib/agents";
import { useRef, useEffect } from "react";
import { Paperclip, Send } from "lucide-react";
import { clsx } from "clsx";

interface Props {
  agent: Agent;
}

export default function ChatBox({ agent }: Props) {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
    body: { agentId: agent.id },
  });

  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    if (file.type === "text/csv" || file.type.includes("text") || file.name.endsWith(".csv")) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result as string;
        // On remplit l'input avec le contenu du fichier pour l'envoyer à l'IA
        handleInputChange({ target: { value: `[Fichier: ${file.name}]\n\nVoici le contenu du fichier pour analyse :\n${content}` } } as any);
      };
      reader.readAsText(file);
    } else {
      alert("Format de fichier non supporté. Veuillez envoyer un CSV ou un fichier texte.");
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-full flex-1 bg-background relative overflow-hidden">
      {/* Background Magic Glow */}
      <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-gold/5 blur-[120px] rounded-full pointer-events-none" />
      
      {/* Messages Area */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-8 space-y-6 scroll-smooth">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-4 opacity-40">
            <span className="text-6xl">{agent.icon}</span>
            <p className="text-xl italic font-serif">Comment puis-je vous aider aujourd'hui, Mathilde ?</p>
          </div>
        )}
        {messages.map((m) => (
          <div key={m.id} className={clsx("flex", m.role === "user" ? "justify-end" : "justify-start")}>
            <div className={clsx(
              "max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap",
              m.role === "user" 
                ? "bg-gold text-background font-medium rounded-br-none" 
                : "bg-white/5 border border-white/10 text-gray-200 rounded-bl-none"
            )}>
              {m.role === "user" ? (
                m.content
              ) : (
                <ReactMarkdown 
                  components={{
                    p: ({children}) => <p className="mb-2 last:mb-0">{children}</p>,
                    ul: ({children}) => <ul className="list-disc ml-4 mb-2">{children}</ul>,
                    ol: ({children}) => <ol className="list-decimal ml-4 mb-2">{children}</ol>,
                    li: ({children}) => <li className="mb-1">{children}</li>,
                    strong: ({children}) => <strong className="text-gold font-bold">{children}</strong>
                  }}
                >
                  {m.content}
                </ReactMarkdown>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white/5 border border-white/10 p-4 rounded-2xl rounded-bl-none text-xs text-gold animate-pulse">
              {agent.name} analyse les données...
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-8 pt-0">
        <form onSubmit={handleSubmit} className="relative group">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
            accept=".csv,.txt"
          />
          <input
            value={input}
            onChange={handleInputChange}
            placeholder={`Message à ${agent.name}...`}
            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-14 pr-14 text-sm focus:outline-none focus:border-gold/50 transition-all placeholder:text-gray-600"
          />
          <button 
            type="button" 
            onClick={handleFileClick}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gold transition-colors"
          >
            <Paperclip size={20} />
          </button>
          <button 
            type="submit" 
            disabled={!input.trim()}
            className="absolute right-4 top-1/2 -translate-y-1/2 p-2 bg-gold rounded-xl text-background hover:scale-105 active:scale-95 disabled:opacity-30 disabled:scale-100 transition-all shadow-[0_0_15px_rgba(251,191,36,0.3)]"
          >
            <Send size={18} />
          </button>
        </form>
        <p className="text-[10px] text-center mt-3 text-gray-600 uppercase tracking-widest font-bold">
          Nexus Intelligence — La Muchette
        </p>
      </div>
    </div>
  );
}
