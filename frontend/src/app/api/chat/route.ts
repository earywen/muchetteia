import { StreamingTextResponse } from "ai";

export const runtime = "edge";

export async function POST(req: Request) {
  try {
    const { messages, agentId } = await req.json();
    const lastMessage = messages[messages.length - 1].content;

    const NEXUS_API_URL = process.env.NEXUS_API_URL;
    const API_KEY = process.env.LAMUCHETTE_API_KEY;

    if (!NEXUS_API_URL) {
      throw new Error("NEXUS_API_URL is not defined");
    }

    const response = await fetch(`${NEXUS_API_URL}/${agentId}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": API_KEY || "",
      },
      body: JSON.stringify({ message: lastMessage }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`[Nexus Error] ${response.status}: ${errorText}`);
      throw new Error(`Nexus Local Error ${response.status}`);
    }

    const data = await response.json();
    const text = data.reply || data.message || "Aucune réponse reçue du Nexus.";

    // Formatage au protocole Vercel AI SDK (0:"texte"\n)
    const encoder = new TextEncoder();
    const stream = new ReadableStream({
      async start(controller) {
        // Le format attendu par useChat est 0: "le mot" \n
        const words = text.split(" ");
        for (const word of words) {
          const chunk = `0:${JSON.stringify(word + " ")}\n`;
          controller.enqueue(encoder.encode(chunk));
          await new Promise((resolve) => setTimeout(resolve, 30));
        }
        controller.close();
      },
    });

    return new StreamingTextResponse(stream);
  } catch (error: any) {
    console.error("[Vercel Edge Error]:", error.message);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
