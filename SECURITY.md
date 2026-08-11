# Security

Do not report credentials, private user data, or exploitable details in a public issue. Send a concise report to the project owner through the contact method listed on the repository profile.

Self-hosters are responsible for securing their own Ollama endpoint, database, object storage, environment files, and deployed application. Do not expose Ollama or Postgres directly to the public internet. Put authentication and a private network or tunnel in front of services that need remote access.

The tutor must remain server-side. Provider keys belong in environment variables and must never be sent to browser code.
