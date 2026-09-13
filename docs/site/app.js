function fmt(n) {
  if (n == null || Number.isNaN(n)) return "—";
  return Math.round(n).toLocaleString("en-US");
}

function row(source, boxes, role) {
  const tr = document.createElement("tr");
  const b = boxes == null ? '<span class="blank">unknown</span>' : fmt(boxes);
  tr.innerHTML = `<td>${source}</td><td>${b}</td><td>${role}</td>`;
  return tr;
}

async function boot() {
  const res = await fetch("site/snapshot.json");
  const d = await res.json();
  const r = d.results;
  const i = d.inputs;
  const k = d.knobs;

  document.getElementById("proven").textContent = fmt(r.proven_sold) + "+";
  document.getElementById("sold").textContent = fmt(r.estimated_sold);
  document.getElementById("print").textContent = fmt(r.estimated_print);
  document.getElementById("sold-band").textContent =
    `Band ${fmt(r.estimated_sold_low)} – ${fmt(r.estimated_sold_high)} · main number`;
  document.getElementById("print-band").textContent =
    `Band ${fmt(r.estimated_print_low)} – ${fmt(r.estimated_print_high)} · US ~${fmt(r.us_print)}`;

  document.getElementById("meta").textContent =
    `Snapshot ${d.snapshot_date} · street ${d.street_date} (day ${d.days_since_street}) · confidence ${d.confidence} · TCGPlayer market $${d.tcgplayer_box_market} vs MSRP $${d.msrp}`;

  const sources = document.getElementById("sources");
  sources.appendChild(row("Target (first-party)", i.mass_first_party, "Mass — proven"));
  sources.appendChild(row("TCGPlayer sealed", r.tcgplayer_boxes_seen, "Hobby — proven"));
  sources.appendChild(row("Amazon marketplace", r.amazon_marketplace_boxes_seen, "Hobby — proven (counts)"));
  sources.appendChild(row("Amazon.com first-party", i.amazon_first_party, "Mass"));
  sources.appendChild(row("Walmart", i.walmart, "No sold count yet"));
  sources.appendChild(row("GameStop", i.gamestop, "No sold count yet"));

  const knobs = document.getElementById("knobs");
  const knobRows = [
    ["Mass coverage (missed doors)", k.mass_coverage, "1.15 – 1.25"],
    ["TCGPlayer share of remaining hobby", (k.tcgplayer_hobby_share * 100).toFixed(0) + "%", "20% – 30%"],
    ["Marketplace overlap cushion", (k.marketplace_overlap_cushion * 100).toFixed(0) + "%", "3% – 5%"],
    ["Unsold still in channel", (k.unsold_in_channel * 100).toFixed(0) + "%", "print layer only"],
    ["US share of Americas print", (k.us_share_of_americas * 100).toFixed(0) + "%", "downstream"],
  ];
  for (const [name, val, band] of knobRows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${name}</td><td>${val}</td><td>${band}</td>`;
    knobs.appendChild(tr);
  }

  const notes = document.getElementById("notes");
  for (const n of d.notes) {
    const li = document.createElement("li");
    li.textContent = n;
    notes.appendChild(li);
  }
  if (d.gmr) {
    const li = document.createElement("li");
    li.innerHTML = `<strong>Grand Master Rare:</strong> Americas lock ${d.gmr.americas_lock.toLocaleString("en-US")}. At this print estimate ≈ 1 per ${d.gmr.implied_boxes_per_gmr_at_estimated_print} boxes. Status: ${d.gmr.status}.`;
    notes.appendChild(li);
  }

}

boot().catch((err) => {
  document.getElementById("meta").textContent = "Could not load snapshot.json — check Pages path.";
  console.error(err);
});
