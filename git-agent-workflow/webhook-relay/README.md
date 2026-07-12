This is the only piece of glue outside GitHub and Linear. Linear webhooks can only push
event data to a URL, they can't call another API directly, so this small relay sits in
between: Linear calls it, it decides whether the event matters, then it calls GitHub.

Deploy this as a Cloudflare Worker (or paste the same logic into any serverless function,
the shape is identical everywhere).

Setup:
1. `npm create cloudflare@latest` and pick "Hello World Worker", or reuse an existing one.
2. Replace the generated `src/index.js` with `worker.js` from this folder.
3. Set these as Worker secrets (`wrangler secret put NAME`):
   - GITHUB_TOKEN     a fine-grained PAT with repository_dispatch permission
   - GITHUB_OWNER     your GitHub username or org
   - GITHUB_REPO      the repo name
   - TRIGGER_STATUS   the Linear status name that should fire the pipeline, e.g. "Ready for dev"
4. Deploy with `wrangler deploy`, copy the resulting URL.
5. In Linear, go to Settings > API > Webhooks, add a webhook pointing at that URL,
   subscribe to "Issues".

That's it. No database, no queue, just a stateless relay.
