# Leads DB (Tier 1)

Shared Postgres for collecting clients/leads across all sites. Runs on the Lubuntu MacBook to avoid a paid cloud DB.

## Tables
- `contacts` — every inbound lead/inquiry (tagged by `source_site`)
- `subscribers` — newsletter / notify-me / waitlist
- `quote_requests` — service-site leads (e.g. sandblasting), flexible `details` JSON

## Run Postgres (Docker, simplest)
```bash
docker run -d --name leads-db \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=leads \
  -p 5432:5432 -v leads_pgdata:/var/lib/postgresql/data \
  postgres:16
```

## Apply the schema
```bash
psql "postgres://postgres:postgres@localhost:5432/leads" -f 001_init_leads.sql
```
(or, with Docker: `docker exec -i leads-db psql -U postgres -d leads < 001_init_leads.sql`)

## Smoke test
```sql
INSERT INTO contacts (email, name, source_site, message)
VALUES ('lead@example.com', 'Test Lead', 'sandblasting', 'Need a quote');

INSERT INTO quote_requests (contact_id, source_site, service, details)
VALUES ((SELECT id FROM contacts ORDER BY created_at DESC LIMIT 1),
        'sandblasting', 'sandblasting',
        '{"size":"2000 sqft","location":"Scranton PA","surface":"steel deck"}');

SELECT source_site, count(*) FROM contacts GROUP BY source_site;
```

## Expose to your sites
- Same machine / LAN: point the site's form handler at `postgres://...@<mac-ip>:5432/leads`.
- Public (forms on Vercel sites): put a tiny API in front, or use **Cloudflare Tunnel** to expose the DB/API without a static IP. Don't expose raw Postgres to the open internet.

Next tier (learning-app users/progress) lives in `services/api/migrations/` when you need it.
