export type Agent = {
  id: string;
  name: string;
  icon: string;
  description: string;
  color: string;
};

export const AGENTS: Agent[] = [
  {
    id: "sirius",
    name: "Sirius",
    icon: "🦉",
    description: "Expert SEO & Visibilité",
    color: "border-blue-500",
  },
  {
    id: "gripsec",
    name: "Gripsec",
    icon: "💰",
    description: "Garde-Manger & Rentabilité",
    color: "border-gold",
  },
];
