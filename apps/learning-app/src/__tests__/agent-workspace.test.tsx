import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ModalityLoop from "../components/ModalityLoop";
import AgentWorkspace from "../components/AgentWorkspace";

const ISO = "2026-09-01T00:00:00.000Z";

function turnView() {
  return {
    session: { id: "s1", accountId: "a", role: "b2c_learner", status: "active", createdAt: ISO, updatedAt: ISO },
    turns: [
      { id: "t1", sessionId: "s1", index: 0, author: "learner", content: "What is an eigenvalue?", createdAt: ISO },
      {
        id: "t2",
        sessionId: "s1",
        index: 1,
        author: "agent",
        content: "An eigenvalue scales its eigenvector.",
        createdAt: ISO,
        artifactIds: ["art1"],
        citations: [{ lessonId: "lesson-eigenvalues", passageId: "eig-p1" }]
      }
    ],
    plan: {
      id: "p1",
      sessionId: "s1",
      goal: "g",
      revision: 1,
      steps: [{ id: "st1", description: "Read the current lesson", status: "done" }],
      createdAt: ISO
    },
    currentStep: { id: "st1", description: "Read the current lesson", status: "done" },
    toolSummaries: [{ toolName: "tutor.explain", ok: true, summary: "Prepared a grounded explanation" }],
    citations: [{ lessonId: "lesson-eigenvalues", passageId: "eig-p1" }],
    artifacts: [
      {
        id: "art1",
        version: 1,
        kind: "svg",
        title: "Eigen diagram",
        description: "",
        altText: "eigen diagram",
        source: "<svg/>",
        sanitizedSource:
          '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect x="4" y="4" width="32" height="32"/></svg>',
        lessonIds: ["lesson-eigenvalues"],
        conceptIds: ["eigenvalues"],
        createdBy: "agent",
        createdAt: ISO,
        exports: [{ format: "svg", dataUri: "data:image/svg+xml;utf8,x", fallback: false }]
      }
    ],
    whyNext: "I ran tutor.explain to ground my answer in your lesson."
  };
}

function jsonResponse(status: number, body: unknown) {
  return { ok: status < 400, status, json: async () => body } as unknown as Response;
}

describe("offline lesson reading", () => {
  it("renders static lesson content without any agent/API call", () => {
    render(
      <ModalityLoop
        title="Eigenvalues"
        htmlContent="<p>An eigenvalue lesson body.</p>"
        textContent="An eigenvalue lesson body."
        isProgramming={false}
      />
    );
    expect(screen.getByText("Eigenvalues")).toBeTruthy();
    expect(screen.getByText("An eigenvalue lesson body.")).toBeTruthy();
  });
});

describe("AgentWorkspace", () => {
  beforeEach(() => {
    vi.stubGlobal("confirm", () => true);
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("renders a session response: reply, plan, tool activity, why-next, artifact", async () => {
    const fetchMock = vi.fn(async (url: string | URL | Request) => {
      const u = String(url);
      if (u.endsWith("/v1/agent/sessions")) {
        return jsonResponse(201, { session: turnView().session, resumed: false });
      }
      if (u.includes("/turns")) {
        return jsonResponse(200, turnView());
      }
      return jsonResponse(404, { error: { message: "no route" } });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AgentWorkspace context={{ title: "Eigenvalues", text: "body", lessonId: "lesson-eigenvalues" }} />);

    fireEvent.change(screen.getByLabelText("Message the tutor"), {
      target: { value: "What is an eigenvalue?" }
    });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => expect(screen.getByText("An eigenvalue scales its eigenvector.")).toBeTruthy());
    expect(screen.getByTestId("plan")).toBeTruthy();
    expect(screen.getByText("Read the current lesson")).toBeTruthy();
    expect(screen.getByText("Prepared a grounded explanation")).toBeTruthy();
    expect(screen.getByTestId("why-next").textContent).toContain("tutor.explain");
    expect(screen.getByTestId("artifact-card")).toBeTruthy();
    expect(screen.getByTestId("safe-svg")).toBeTruthy();
  });

  it("shows a recoverable error with retry when the agent is unavailable", async () => {
    const fetchMock = vi.fn(async () => {
      throw new Error("network down");
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AgentWorkspace context={{ title: "Eigenvalues", text: "body" }} />);
    fireEvent.change(screen.getByLabelText("Message the tutor"), { target: { value: "hi" } });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => expect(screen.getByTestId("error")).toBeTruthy());
    expect(screen.getByText("Retry")).toBeTruthy();
  });

  it("cancelling an in-flight turn aborts the request and does not overwrite state", async () => {
    const fetchMock = vi.fn((url: string | URL | Request, init?: RequestInit) => {
      const u = String(url);
      if (u.endsWith("/v1/agent/sessions")) {
        return Promise.resolve(jsonResponse(201, { session: turnView().session, resumed: false }));
      }
      if (u.includes("/turns")) {
        // Pending until the AbortSignal fires, mirroring a real slow fetch.
        return new Promise<Response>((_resolve, reject) => {
          const signal = init?.signal;
          if (signal) {
            signal.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")));
          }
        });
      }
      return Promise.resolve(jsonResponse(404, { error: { message: "no route" } }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AgentWorkspace context={{ title: "Eigenvalues", text: "body", lessonId: "lesson-eigenvalues" }} />);
    fireEvent.change(screen.getByLabelText("Message the tutor"), {
      target: { value: "What is an eigenvalue?" }
    });
    fireEvent.click(screen.getByText("Send"));

    const cancelBtn = await screen.findByText("Cancel");
    fireEvent.click(cancelBtn);

    await waitFor(() => expect(screen.getByTestId("error").textContent).toContain("Cancelled"));
    // A late/aborted response must never render the agent reply.
    expect(screen.queryByText("An eigenvalue scales its eigenvector.")).toBeNull();
  });
});
