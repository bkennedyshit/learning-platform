export * from "./auth/index.js";
export * from "./config.js";
export * from "./db.js";
export * from "./learning/index.js";
export * from "./practice/index.js";
export * from "./rag/index.js";
export * from "./tutor/index.js";
export * from "./tts/index.js";
export * from "./compliance/index.js";
export * from "./affiliate/index.js";
export * from "./agent/index.js";
export * as http from "./http/index.js";
export * as agentContract from "@learning-platform/agent-contract";

// `ModalityStage` is exported by both ./learning and ./agent (memory); the two
// declarations are identical. Re-export explicitly to resolve the ambiguity.
export type { ModalityStage } from "./learning/index.js";
