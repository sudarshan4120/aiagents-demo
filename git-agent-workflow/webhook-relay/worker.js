export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("expected POST", { status: 405 });
    }

    const payload = await request.json();

    // Linear sends { action, type, data, ... } for every workspace event.
    // We only care about issues moving into the trigger status.
    if (payload.type !== "Issue") {
      return new Response("ignored, not an issue event", { status: 200 });
    }

    const issue = payload.data;
    const statusName = issue?.state?.name;

    if (statusName !== env.TRIGGER_STATUS) {
      return new Response(`ignored, status is "${statusName}"`, { status: 200 });
    }

    const dispatchResponse = await fetch(
      `https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/dispatches`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${env.GITHUB_TOKEN}`,
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          event_type: "linear-ticket-ready",
          client_payload: { ticket_key: issue.identifier },
        }),
      }
    );

    if (!dispatchResponse.ok) {
      const errorText = await dispatchResponse.text();
      return new Response(`GitHub dispatch failed: ${errorText}`, { status: 502 });
    }

    return new Response(`dispatched ${issue.identifier}`, { status: 200 });
  },
};
