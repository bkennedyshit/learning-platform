const ATT_URL = "https://alnk.to/3JaXrf2";

export function AffiliateOffer() {
  return (
    <aside aria-label="AT&T advertisement" style={{ position: "relative", overflow: "hidden", margin: "0 0 2rem", padding: "1.5rem", border: "1px solid #60bde8", borderRadius: 16, background: "linear-gradient(110deg,#0057b8,#0676ce 55%,#00a8e0)", color: "#fff", boxShadow: "0 18px 50px rgba(0,87,184,.2)" }}>
      <div aria-hidden="true" style={{ position: "absolute", width: 190, height: 190, right: -45, top: -95, border: "22px solid rgba(255,255,255,.1)", borderRadius: "50%" }} />
      <div style={{ position: "relative", display: "flex", alignItems: "center", justifyContent: "space-between", gap: "1.5rem", flexWrap: "wrap" }}>
        <div style={{ flex: "1 1 360px" }}>
          <div style={{ color: "rgba(255,255,255,.78)", fontSize: ".72rem", fontWeight: 800, letterSpacing: ".14em", textTransform: "uppercase" }}>Advertisement · Affiliate partner</div>
          <div style={{ marginTop: ".35rem", fontSize: "1.8rem", fontWeight: 900 }}>AT&amp;T Wireless</div>
          <p style={{ margin: ".35rem 0 0", lineHeight: 1.55, color: "rgba(255,255,255,.92)" }}>Compare current coverage, hotspot, device, eligibility, and full plan terms for remote learning.</p>
        </div>
        <a href={ATT_URL} target="_blank" rel="sponsored nofollow noopener noreferrer" style={{ display: "inline-block", padding: ".8rem 1.2rem", borderRadius: 999, background: "#fff", color: "#0057b8", fontWeight: 800, textDecoration: "none" }}>Compare current offers →</a>
      </div>
    </aside>
  );
}
