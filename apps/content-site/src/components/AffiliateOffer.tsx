const ATT_URL = "https://alnk.to/3JaXrf2";

export function AffiliateOffer() {
  return (
    <aside aria-label="AT&T advertisement" style={{ margin: "0 0 2rem" }}>
      <div style={{ marginBottom: ".5rem", color: "#64748b", fontSize: ".68rem", fontWeight: 800, letterSpacing: ".14em", textAlign: "center", textTransform: "uppercase" }}>Advertisement · Affiliate partner</div>
      <a href={ATT_URL} target="_blank" rel="sponsored nofollow noopener noreferrer" style={{ display: "block", width: "fit-content", maxWidth: "100%", margin: "0 auto", overflow: "hidden", borderRadius: 8 }}>
        <img src="https://cdn.avantlink.com/banners/85cbb310-8273-4bb9-9350-8b256144dd8d.png" width="398" height="264" alt="AT&amp;T wireless advertisement" style={{ display: "block", maxWidth: "100%", height: "auto" }} />
      </a>
    </aside>
  );
}
