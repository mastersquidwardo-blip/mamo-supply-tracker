function fmt(n) {
  if (n == null || Number.isNaN(n)) return "—";
  return Math.round(n).toLocaleString("en-US");
}

function row(source, boxes, role) {
  const tr = document.createElement("tr");
  const b = boxes == null ? '<span class="blank">unknown / guess only</span>' : fmt(boxes);
  tr.innerHTML = `<td>${source}</td><td>${b}</td><td>${role}</td>`;
  return tr;
}

async function boot() {
  const res = await fetch("site/snapshot.json");
  const d = await res.json();
  const r = d.results;
  const i = d.inputs;
  const k = d.knobs;
  const hid = d.hidden_channels;
  const rh = d.results_with_hidden;
  const g = d.gmr;
  const wp = d.working_print || {};

  document.getElementById("proven").textContent = fmt(r.proven_sold) + "+";
  document.getElementById("sold").textContent = fmt(r.estimated_sold);
  document.getElementById("sold-band").textContent =
    `Band ${fmt(r.estimated_sold_low)} – ${fmt(r.estimated_sold_high)} · visible evidence only`;

  // Headline print = working ~450k
  const printHeadline = wp.americas != null ? wp.americas : r.estimated_print;
  document.getElementById("print").textContent = "~" + fmt(printHeadline);
  document.getElementById("print-band").textContent =
    `Working print · ~1 GMR per ${fmt(wp.boxes_per_gmr || 250)} boxes · US ~${fmt(wp.us_approx || r.us_print)}`;

  const onlineOnly = r.estimated_print_online_only;
  const note = document.getElementById("online-only-note");
  if (note && onlineOnly != null) {
    note.textContent =
      `Online-only estimated print (no hidden doors): ${fmt(onlineOnly)} ` +
      `(band ${fmt(r.estimated_print_online_only_low)} – ${fmt(r.estimated_print_online_only_high)}; US ~${fmt(r.us_print_online_only)}). ` +
      `Kept as a footnote — not the headline.`;
  }

  if (rh) {
    const sh = document.getElementById("sold-hidden");
    const ph = document.getElementById("print-hidden");
    if (sh) sh.textContent = fmt(rh.estimated_sold);
    if (ph) ph.textContent = fmt(rh.estimated_print);
  }

  document.getElementById("meta").textContent =
    `Snapshot ${d.snapshot_date} · street ${d.street_date} (day ${d.days_since_street}) · confidence ${d.confidence} · TCGPlayer market $${d.tcgplayer_box_market} vs MSRP $${d.msrp}`;

  const sources = document.getElementById("sources");
  sources.appendChild(row("Target (first-party badge)", i.mass_first_party, "Proven — mostly online signal"));
  sources.appendChild(row("TCGPlayer sealed", r.tcgplayer_boxes_seen, "Proven hobby"));
  sources.appendChild(row("Amazon marketplace", r.amazon_marketplace_boxes_seen, "Proven hobby (counts)"));
  sources.appendChild(row("Amazon.com first-party", i.amazon_first_party, "Proven mass"));
  sources.appendChild(row("Walmart", null, "No sold badge — labeled guess below"));
  sources.appendChild(row("GameStop", null, "No sold badge — labeled guess below"));
  sources.appendChild(row("Best Buy", null, "In-store heavy — labeled guess below"));

  const hiddenBody = document.getElementById("hidden-doors");
  if (hid && hiddenBody) {
    hiddenBody.appendChild(row("Target with in-store lift", hid.target_total_with_instore, `From ${fmt(hid.target_online)} online @ ${hid.defaults.target_online_share} online share`));
    for (const door of hid.doors) {
      hiddenBody.appendChild(
        row(
          door.name,
          door.total,
          `Online ${fmt(door.online)} / in-store ${fmt(door.in_store)} · ${Math.round(door.vs_target * 100)}% of Target total`
        )
      );
    }
    hiddenBody.appendChild(row("Other mass doors", hid.other_mass, "Regional / missed"));
    hiddenBody.appendChild(row("Hidden mass add-on", hid.hidden_mass_total, "Guess layer only"));
  }

  const knobs = document.getElementById("knobs");
  const knobRows = [
    ["Mass coverage (missed doors)", k.mass_coverage, "1.15 – 1.25"],
    ["TCGPlayer share of remaining hobby", (k.tcgplayer_hobby_share * 100).toFixed(0) + "%", "20% – 30%"],
    ["Marketplace overlap cushion", (k.marketplace_overlap_cushion * 100).toFixed(0) + "%", "3% – 5%"],
    ["Unsold still in channel", (k.unsold_in_channel * 100).toFixed(0) + "%", "print layer only"],
    ["Target online share", hid?.defaults?.target_online_share || "55%", "lifts badge for in-store"],
    ["Walmart vs Target", hid?.defaults?.walmart_vs_target || "75%", "labeled guess"],
    ["GameStop vs Target", hid?.defaults?.gamestop_vs_target || "15%", "labeled guess"],
    ["Best Buy vs Target", hid?.defaults?.best_buy_vs_target || "25%", "in-store heavy"],
    ["Working print", "~" + fmt(wp.americas || 450000), "1,800 serials × ~250 boxes"],
  ];
  for (const [name, val, band] of knobRows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${name}</td><td>${val}</td><td>${band}</td>`;
    knobs.appendChild(tr);
  }

  if (g) {
    document.getElementById("gmr-confirmed").textContent = fmt(g.confirmed_americas_serials);
    const opened = g.implied_boxes_opened_mid_450k != null ? g.implied_boxes_opened_mid_450k : g.implied_boxes_opened_mid;
    document.getElementById("gmr-opened").textContent = fmt(opened);
    document.getElementById("gmr-band").textContent =
      `Band ${fmt(g.implied_boxes_opened_low)} – ${fmt(g.implied_boxes_opened_high)} (if ${Math.round((g.public_report_share_mid || 0.25) * 100)}% of pulls go public; boxes opened, not sealed sold)`;
    document.getElementById("gmr-rate").textContent =
      `≈ 1 GMR per ${fmt(wp.boxes_per_gmr || g.boxes_per_gmr_at_450k || 250)} boxes at the ~450k working print`;
  }

  const notes = document.getElementById("notes");
  for (const n of d.notes) {
    const li = document.createElement("li");
    li.textContent = n;
    notes.appendChild(li);
  }
}

boot().catch((err) => {
  document.getElementById("meta").textContent = "Could not load snapshot.json — check Pages path.";
  console.error(err);
});
