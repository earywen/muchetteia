import { OpenAIStream, StreamingTextResponse } from "ai";
import OpenAI from "openai";

// Nous utilisons l'OpenAI SDK comme client générique ou nous appelons directement le Nexus Local
export const runtime = "edge";

export async function POST(req: Request) {
  const { messages, agentId } = await req.json();
  const lastMessage = messages[messages.length - 1].content;

  // URL de votre Beelink (configurée dans les variables d'env Vercel)
  const NEXUS_API_URL = process.env.NEXUS_API_URL || "http://[VOTRE-IP]:8000";
  const API_KEY = process.env.LAMUCHETTE_API_KEY;

  try {
    // 1. On envoie la requête au Nexus Local (FastAPI)
    // Pour cet exemple, on simule l'appel à Sirius ou Gripsec
    const response = await fetch(`${NEXUS_API_URL}/${agentId}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY || "",
      },
      body: JSON.stringify({ message: lastMessage }),
    });

    if (!response.ok) {
        throw new Error("Erreur lors de la communication avec le Nexus Local");
    }

    const data = await response.json();
    
    // 2. On transforme la réponse en Stream (ou on la renvoie telle quelle si pas de streaming local)
    // Note: Pour une expérience fluide, le Vercel AI SDK attend un stream.
    // Si votre API locale ne streame pas encore, on crée un stream artificiel à partir du texte.
    
    const stream = new ReadableStream({
      async start(controller) {
        const text = data.reply || data.message || "Je n'ai pas pu obtenir de réponse.";
        const words = text.split(" ");
        for (const word of words) {
          controller.enqueue(word + " ");
          await new Promise((resolve) => setTimeout(resolve, 30)); // Simulation de streaming
        }
        controller.close();
      },
    });

    return new StreamingTextResponse(stream);
  } catch (error) {
    return new Response(JSON.stringify({ error: "Nexus hors ligne ou erreur technique" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
