import {
  parse,
  validate,
  type ObjectSchema,
  type SchemaNode,
  type ValidationResult
} from "./schema.js";
import {
  ACCOUNT_ROLES,
  APPROVAL_ACTIONS,
  APPROVAL_STATUSES,
  ARTIFACT_AUTHORS,
  ARTIFACT_EXPORT_FORMATS,
  ARTIFACT_KINDS,
  JOB_STATUSES,
  PLAN_STEP_STATUSES,
  SESSION_STATUSES,
  TOOL_CATEGORIES,
  TRACE_EVENT_TYPES,
  TURN_AUTHORS,
  type AgentSession,
  type ApprovalRequest,
  type Artifact,
  type ConversationTurn,
  type Job,
  type JobProgressEvent,
  type Plan,
  type StructuredError,
  type ToolCall,
  type ToolResult,
  type TraceEvent
} from "./types.js";

const nonEmptyString: SchemaNode = { type: "string", minLength: 1 };
const isoDate: SchemaNode = { type: "string", minLength: 1, pattern: "^\\d{4}-\\d{2}-\\d{2}T" };
const stringArray: SchemaNode = { type: "array", items: { type: "string", minLength: 1 } };
const ratio: SchemaNode = { type: "number", min: 0, max: 1 };

/** A schema descriptor is itself an opaque object at the wire boundary. */
const schemaNodeSchema: SchemaNode = { type: "object", properties: {}, additionalProperties: true };
const opaqueObject: SchemaNode = { type: "object", properties: {}, additionalProperties: true };

export const structuredErrorSchema: ObjectSchema = {
  type: "object",
  required: ["code", "message", "retryable"],
  properties: {
    code: nonEmptyString,
    message: { type: "string" },
    retryable: { type: "boolean" },
    details: opaqueObject
  }
};

export const agentSessionSchema: ObjectSchema = {
  type: "object",
  required: ["id", "accountId", "role", "status", "createdAt", "updatedAt"],
  properties: {
    id: nonEmptyString,
    accountId: nonEmptyString,
    role: { type: "string", enum: ACCOUNT_ROLES },
    status: { type: "string", enum: SESSION_STATUSES },
    goalId: nonEmptyString,
    lessonId: nonEmptyString,
    summary: { type: "string" },
    createdAt: isoDate,
    updatedAt: isoDate
  }
};

const citationSchema: SchemaNode = {
  type: "object",
  required: ["lessonId"],
  properties: {
    lessonId: nonEmptyString,
    passageId: nonEmptyString
  }
};

export const conversationTurnSchema: ObjectSchema = {
  type: "object",
  required: ["id", "sessionId", "index", "author", "content", "createdAt"],
  properties: {
    id: nonEmptyString,
    sessionId: nonEmptyString,
    index: { type: "number", integer: true, min: 0 },
    author: { type: "string", enum: TURN_AUTHORS },
    content: { type: "string" },
    createdAt: isoDate,
    artifactIds: stringArray,
    citations: { type: "array", items: citationSchema }
  }
};

export const toolDefinitionSchema: ObjectSchema = {
  type: "object",
  required: ["name", "category", "description", "inputSchema", "outputSchema"],
  properties: {
    name: nonEmptyString,
    category: { type: "string", enum: TOOL_CATEGORIES },
    description: { type: "string" },
    inputSchema: schemaNodeSchema,
    outputSchema: schemaNodeSchema,
    requiredRole: { type: "string", enum: ACCOUNT_ROLES },
    idempotent: { type: "boolean" }
  }
};

export const toolCallSchema: ObjectSchema = {
  type: "object",
  required: ["id", "sessionId", "toolName", "input", "createdAt"],
  properties: {
    id: nonEmptyString,
    sessionId: nonEmptyString,
    toolName: nonEmptyString,
    input: { type: "unknown" },
    idempotencyKey: nonEmptyString,
    createdAt: isoDate
  }
};

export const toolResultSchema: ObjectSchema = {
  type: "object",
  required: ["callId", "toolName", "ok", "startedAt", "finishedAt"],
  properties: {
    callId: nonEmptyString,
    toolName: nonEmptyString,
    ok: { type: "boolean" },
    output: { type: "unknown" },
    error: structuredErrorSchema,
    startedAt: isoDate,
    finishedAt: isoDate
  }
};

const planStepSchema: SchemaNode = {
  type: "object",
  required: ["id", "description", "status"],
  properties: {
    id: nonEmptyString,
    description: { type: "string" },
    status: { type: "string", enum: PLAN_STEP_STATUSES },
    toolName: nonEmptyString
  }
};

export const planSchema: ObjectSchema = {
  type: "object",
  required: ["id", "sessionId", "goal", "revision", "steps", "createdAt"],
  properties: {
    id: nonEmptyString,
    sessionId: nonEmptyString,
    goal: { type: "string" },
    revision: { type: "number", integer: true, min: 0 },
    steps: { type: "array", items: planStepSchema },
    createdAt: isoDate
  }
};

export const jobSchema: ObjectSchema = {
  type: "object",
  required: ["id", "sessionId", "kind", "status", "progress", "createdAt", "updatedAt"],
  properties: {
    id: nonEmptyString,
    sessionId: nonEmptyString,
    kind: nonEmptyString,
    status: { type: "string", enum: JOB_STATUSES },
    progress: ratio,
    createdAt: isoDate,
    updatedAt: isoDate,
    resultArtifactIds: stringArray,
    error: structuredErrorSchema
  }
};

export const jobProgressEventSchema: ObjectSchema = {
  type: "object",
  required: ["jobId", "progress", "at"],
  properties: {
    jobId: nonEmptyString,
    progress: ratio,
    message: { type: "string" },
    at: isoDate
  }
};

const artifactExportSchema: SchemaNode = {
  type: "object",
  required: ["format", "dataUri", "fallback"],
  properties: {
    format: { type: "string", enum: ARTIFACT_EXPORT_FORMATS },
    dataUri: nonEmptyString,
    fallback: { type: "boolean" }
  }
};

export const artifactSchema: ObjectSchema = {
  type: "object",
  required: [
    "id",
    "version",
    "kind",
    "title",
    "description",
    "altText",
    "source",
    "sanitizedSource",
    "lessonIds",
    "conceptIds",
    "createdBy",
    "createdAt"
  ],
  properties: {
    id: nonEmptyString,
    version: { type: "number", integer: true, min: 1 },
    kind: { type: "string", enum: ARTIFACT_KINDS },
    title: nonEmptyString,
    description: { type: "string" },
    altText: nonEmptyString,
    source: { type: "string" },
    sanitizedSource: { type: "string" },
    lessonIds: stringArray,
    conceptIds: stringArray,
    createdBy: { type: "string", enum: ARTIFACT_AUTHORS },
    provider: nonEmptyString,
    createdAt: isoDate,
    exports: { type: "array", items: artifactExportSchema }
  }
};

export const approvalRequestSchema: ObjectSchema = {
  type: "object",
  required: ["id", "action", "status", "artifactId", "requestedBy", "version", "createdAt"],
  properties: {
    id: nonEmptyString,
    action: { type: "string", enum: APPROVAL_ACTIONS },
    status: { type: "string", enum: APPROVAL_STATUSES },
    artifactId: nonEmptyString,
    requestedBy: nonEmptyString,
    version: { type: "number", integer: true, min: 1 },
    createdAt: isoDate,
    sessionId: nonEmptyString,
    decidedBy: nonEmptyString,
    decidedAt: isoDate,
    reason: { type: "string" },
    provenance: opaqueObject
  }
};

export const traceEventSchema: ObjectSchema = {
  type: "object",
  required: ["id", "sessionId", "seq", "type", "at", "summary"],
  properties: {
    id: nonEmptyString,
    sessionId: nonEmptyString,
    seq: { type: "number", integer: true, min: 0 },
    type: { type: "string", enum: TRACE_EVENT_TYPES },
    at: isoDate,
    summary: { type: "string" },
    data: opaqueObject
  }
};

/* ----------------------------- typed helpers ---------------------------- */

export const validateAgentSession = (v: unknown): ValidationResult => validate(agentSessionSchema, v);
export const validateConversationTurn = (v: unknown): ValidationResult => validate(conversationTurnSchema, v);
export const validateToolDefinition = (v: unknown): ValidationResult => validate(toolDefinitionSchema, v);
export const validateToolCall = (v: unknown): ValidationResult => validate(toolCallSchema, v);
export const validateToolResult = (v: unknown): ValidationResult => validate(toolResultSchema, v);
export const validatePlan = (v: unknown): ValidationResult => validate(planSchema, v);
export const validateJob = (v: unknown): ValidationResult => validate(jobSchema, v);
export const validateJobProgressEvent = (v: unknown): ValidationResult => validate(jobProgressEventSchema, v);
export const validateArtifact = (v: unknown): ValidationResult => validate(artifactSchema, v);
export const validateApprovalRequest = (v: unknown): ValidationResult => validate(approvalRequestSchema, v);
export const validateStructuredError = (v: unknown): ValidationResult => validate(structuredErrorSchema, v);
export const validateTraceEvent = (v: unknown): ValidationResult => validate(traceEventSchema, v);

export const parseAgentSession = (v: unknown): AgentSession => parse(agentSessionSchema, v, "AgentSession");
export const parseConversationTurn = (v: unknown): ConversationTurn =>
  parse(conversationTurnSchema, v, "ConversationTurn");
export const parseToolCall = (v: unknown): ToolCall => parse(toolCallSchema, v, "ToolCall");
export const parseToolResult = (v: unknown): ToolResult => parse(toolResultSchema, v, "ToolResult");
export const parsePlan = (v: unknown): Plan => parse(planSchema, v, "Plan");
export const parseJob = (v: unknown): Job => parse(jobSchema, v, "Job");
export const parseJobProgressEvent = (v: unknown): JobProgressEvent =>
  parse(jobProgressEventSchema, v, "JobProgressEvent");
export const parseArtifact = (v: unknown): Artifact => parse(artifactSchema, v, "Artifact");
export const parseApprovalRequest = (v: unknown): ApprovalRequest =>
  parse(approvalRequestSchema, v, "ApprovalRequest");
export const parseStructuredError = (v: unknown): StructuredError =>
  parse(structuredErrorSchema, v, "StructuredError");
export const parseTraceEvent = (v: unknown): TraceEvent => parse(traceEventSchema, v, "TraceEvent");
