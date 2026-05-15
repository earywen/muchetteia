import { StreamingTextResponse } from "ai";

export const runtime = "edge";

export async function POST(req: Request) {
  try {
    const { messages, agentId } = await req.json();
    const lastMessage = messages[messages.length - 1].content;

    const NEXUS_API_URL = process.env.NEXUS_API_URL;
    const API_KEY = process.env.LAMUCHETTE_API_KEY;

    console.log(`[Nexus] Calling ${agentId} at ${NEXUS_API_URL}`);

    if (!NEXUS_API_URL) {
      throw new Error("NEXUS_API_URL is not defined in environment variables");
    }

    const response = await fetch(`${NEXUS_API_URL}/${agentId}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY || "",
      },
      body: JSON.stringify({ message: lastMessage }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`[Nexus Error] ${response.status}: ${errorText}`);
      throw new Error(`Nexus Local a répondu avec une erreur ${response.status}`);
    }

    const data = await response.json();
    const text = data.reply || data.message || "Aucune réponse reçue du Nexus.";

    // Stream artificiel pour le Vercel AI SDK
    const stream = new ReadableStream({
      async start(controller) {
        const words = text.split(" ");
        for (const word of words) {
          controller.enqueue(word + " ");
          await new Promise((resolve) => setTimeout(resolve, 20));
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
