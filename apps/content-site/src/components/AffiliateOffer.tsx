const ATT_URL = "https://alnk.to/3JaXrf2";

export function AffiliateOffer() {
  return (
    <aside aria-label="AT&T affiliate partner" style={{ margin: "0 0 2rem", padding: "1.25rem", border: "1px solid #d9deea", borderRadius: 12, background: "#fff" }}>
      <div style={{ color: "#315bd6", fontSize: ".75rem", fontWeight: 800, letterSpacing: ".08em", textTransform: "uppercase" }}>Affiliate partner</div>
      <h2 style={{ margin: ".4rem 0", fontSize: "1.25rem" }}>Compare a plan for remote learning</h2>
      <p style={{ margin: "0 0 1rem", lineHeight: 1.6 }}>Verify coverage at home and school, hotspot limits, device eligibility, fees, and current offer terms directly with AT&T before switching.</p>
      <a href={ATT_URL} target="_blank" rel="sponsored nofollow noopener noreferrer" style={{ color: "#244bb8", fontWeight: 700 }}>Compare current AT&T offers →</a>
    </aside>
  );
}
