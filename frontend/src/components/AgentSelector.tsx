"use client";

import { AGENTS, Agent } from "@/lib/agents";
import { clsx } from "clsx";

interface Props {
  selectedAgent: Agent;
  onSelect: (agent: Agent) => void;
}

export default function AgentSelector({ selectedAgent, onSelect }: Props) {
  return (
    <div className="flex flex-col gap-4 p-6 bg-card border-r border-white/10 h-full w-64">
      <h2 className="text-gold font-bold text-lg mb-4">Nexus Agents</h2>
      {AGENTS.map((agent) => (
        <button
          key={agent.id}
          onClick={() => onSelect(agent)}
          className={clsx(
            "flex items-center gap-3 p-4 rounded-xl border transition-all duration-300 text-left",
            selectedAgent.id === agent.id
              ? `${agent.color} bg-white/5 shadow-[0_0_15px_rgba(251,191,36,0.1)]`
              : "border-transparent hover:bg-white/5 text-gray-400"
          )}
        >
          <span className="text-2xl">{agent.icon}</span>
          <div>
            <div className="font-bold text-sm text-white">{agent.name}</div>
            <div className="text-xs opacity-60">{agent.description}</div>
          </div>
        </button>
      ))}
    </div>
  );
}
