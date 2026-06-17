import { NextRequest } from "next/server";

export const runtime = "nodejs";

// Provider switch:
//   TUTOR_PROVIDER=local  -> local Ollama (OpenAI-compatible), free, no cloud bill
//   TUTOR_PROVIDER=gemini -> Gemini API (required for the contest's deployed app)
// Defaults to gemini when a key is present, otherwise local.
const PROVIDER =
  process.env.TUTOR_PROVIDER || (process.env.GEMINI_API_KEY ? "gemini" : "local");

const GEMINI_MODEL = process.env.GEMINI_MODEL || "gemini-3.5-flash";
const OLLAMA_URL = process.env.OLLAMA_URL || "http://localhost:11434/v1";
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || "llama3:8b";

interface TutorBody {
  question?: string;
  lessonTitle?: string;
  lessonText?: string;
}

function buildSystem(title: string | undefined, context: string): string {
  return (
    `You are a patient, precise tutor for the lesson "${title ?? "this lesson"}". ` +
    `Answer the student's question using ONLY the lesson content provided below. ` +
    `Explain in clear, plain language with short steps and concrete examples. ` +
    `If the answer is not contained in the lesson, say you can't find it in this lesson and suggest what to review instead — do not invent facts.\n\n` +
    `LESSON CONTENT:\n"""\n${context}\n"""`
  );
}

async function askLocal(system: string, question: string) {
  const res = await fetch(`${OLLAMA_URL}/chat/completions`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      model: OLLAMA_MODEL,
      messages: [
        { role: "system", content: system },
        { role: "user", content: question },
      ],
      temperature: 0.2,
      max_tokens: 800,
      stream: false,
    }),
  });
  if (!res.ok) {
    const detail = (await res.text()).slice(0, 300);
    return { ok: false, detail };
  }
  const data = await res.json();
  const answer = (data?.choices?.[0]?.message?.content || "").trim();
  return { ok: true, answer };
}

async function askGemini(system: string, question: string) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return { ok: false, detail: "missing GEMINI_API_KEY" };
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${apiKey}`;
  const init = {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      systemInstruction: { parts: [{ text: system }] },
      contents: [{ role: "user", parts: [{ text: question }] }],
      generationConfig: { temperature: 0.2, maxOutputTokens: 800 },
    }),
  };
  let detail = "";
  for (let attempt = 0; attempt < 3; attempt++) {
    const res = await fetch(url, init);
    if (res.ok) {
      const data = await res.json();
      const answer =
        data?.candidates?.[0]?.content?.parts?.map((p: { text?: string }) => p.text || "").join("").trim() || "";
      return { ok: true, answer };
    }
    detail = (await res.text()).slice(0, 300);
    if (res.status === 503 || res.status === 429) {
      await new Promise((r) => setTimeout(r, 600 * (attempt + 1)));
      continue;
    }
    break;
  }
  return { ok: false, detail };
}

export async function POST(req: NextRequest) {
  let body: TutorBody;
  try {
    body = (await req.json()) as TutorBody;
  } catch {
    return Response.json({ answer: "Invalid request.", grounded: false }, { status: 400 });
  }

  const question = (body.question || "").trim();
  if (!question) {
    return Response.json({ answer: "Ask a question about this lesson.", grounded: false });
  }

  const system = buildSystem(body.lessonTitle, (body.lessonText || "").slice(0, 8000));

  try {
    const result = PROVIDER === "local" ? await askLocal(system, question) : await askGemini(system, question);

    if (!result.ok) {
      const hint =
        PROVIDER === "local"
          ? "The local tutor isn't responding — is Ollama running?"
          : "The tutor is busy right now — give it a second and try again.";
      return Response.json({ answer: hint, grounded: false, provider: PROVIDER, error: result.detail }, { status: 200 });
    }

    return Response.json({
      answer: result.answer || "I couldn't generate a response for that.",
      grounded: true,
      provider: PROVIDER,
    });
  } catch (e) {
    return Response.json(
      { answer: "The tutor is unavailable right now. Please try again shortly.", grounded: false, provider: PROVIDER },
      { status: 200 }
    );
  }
}
