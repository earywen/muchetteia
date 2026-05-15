"use client";

import { useState } from "react";
import { AGENTS, Agent } from "@/lib/agents";
import AgentSelector from "@/components/AgentSelector";
import ChatBox from "@/components/ChatBox";

export default function Home() {
  const [selectedAgent, setSelectedAgent] = useState<Agent>(AGENTS[0]);

  return (
    <main className="flex h-screen w-full overflow-hidden">
      {/* Sidebar Selector */}
      <AgentSelector 
        selectedAgent={selectedAgent} 
        onSelect={(agent) => setSelectedAgent(agent)} 
      />

      {/* Main Chat Interface */}
      <ChatBox agent={selectedAgent} />
    </main>
  );
}
