export function AffiliateDisclosure({ partner }: { partner: string }) {
  return (
    <aside aria-label="Affiliate disclosure" style={{ margin: "1.5rem 0 1rem", padding: "1rem 1.25rem", border: "1px solid #bfd3ff", borderLeft: "4px solid #315bd6", borderRadius: 12, background: "#f6f8ff", lineHeight: 1.55 }}>
      <strong>Affiliate disclosure</strong>
      <p style={{ margin: ".35rem 0" }}>This resource contains an affiliate link. If you buy through it, NEPA Learning may earn a commission at no extra cost to you. The educational guidance remains independent.</p>
      <small>Featured partner: {partner}</small>
    </aside>
  );
}
