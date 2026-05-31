const data = window.deliveryStudioData;

const money = (value) => `$${Number(value).toLocaleString()}`;

const statusClass = (decision) => {
  if (decision === "Intervene" || decision === "Ship pilot") return "is-hot";
  if (decision === "Discovery sprint" || decision === "Test") return "is-test";
  return "is-watch";
};

const metricBar = (label, value, suffix = "%", danger = false) => `
  <div class="metric-bar">
    <div class="metric-bar__label">
      <span>${label}</span>
      <b>${value}${suffix}</b>
    </div>
    <div class="bar-track">
      <span class="${danger ? "bar-fill danger" : "bar-fill"}" style="width:${Math.min(value, 100)}%"></span>
    </div>
  </div>
`;

const segmentRows = data.segments.slice(0, 7).map((row) => `
  <tr>
    <td>
      <strong>${row.segment_name}</strong>
      <small>${row.scenario} · ${row.channel}</small>
    </td>
    <td>${row.weekly_orders.toLocaleString()}</td>
    <td>${row.under_25_min_sla_pct}%</td>
    <td>${row.handoff_wait_minutes}</td>
    <td>${row.customer_contact_rate_pct}%</td>
    <td><span class="pill ${statusClass(row.decision)}">${row.decision}</span></td>
  </tr>
`).join("");

const initiativeCards = data.initiatives.map((item, index) => `
  <article class="initiative-card">
    <div class="rank">0${index + 1}</div>
    <div>
      <p class="eyebrow">${item.decision}</p>
      <h3>${item.title}</h3>
      <p>${item.solution}</p>
      <div class="initiative-grid">
        <span><b>${item.opportunity_score}</b> score</span>
        <span><b>${money(item.monthly_value_usd)}</b> monthly value</span>
        <span><b>${item.confidence_pct}%</b> confidence</span>
        <span><b>${item.effort_points}</b> effort points</span>
      </div>
    </div>
  </article>
`).join("");

const requirementRows = data.requirements.map((row) => `
  <tr>
    <td>${row.req_id}</td>
    <td>
      <strong>${row.requirement}</strong>
      <small>${row.acceptance}</small>
    </td>
    <td>${row.metric}</td>
    <td>${row.owner}</td>
  </tr>
`).join("");

const partnerRows = data.partnerPlan.map((row) => `
  <li>
    <b>${row.title}</b>
    <span>${row.partner_touchpoint}</span>
    <small>${row.escalation_rule}</small>
  </li>
`).join("");

const feedbackRows = data.feedback.slice(0, 6).map((row) => `
  <article>
    <span>${row.category}</span>
    <b>${row.theme}</b>
    <em>${row.weekly_mentions} modeled weekly mentions · ${row.severity}</em>
  </article>
`).join("");

document.querySelector("#app").innerHTML = `
  <header class="topbar">
    <a href="#cockpit">Cockpit</a>
    <a href="#business-case">Business case</a>
    <a href="#requirements">Requirements</a>
  </header>

  <main>
    <section class="hero" id="cockpit">
      <div class="hero__copy">
        <p class="eyebrow">Product ops artifact for delivery fulfillment</p>
        <h1>Delivery Fulfillment Experience Optimization Studio</h1>
        <p class="lede">A product-management workspace for turning delivery performance data, user feedback, partner asks, and store operations constraints into a ranked roadmap.</p>
      </div>
      <aside class="decision-brief">
        <span>Current decision</span>
        <h2>${data.topSegment.segment_name}</h2>
        <p>${data.topSegment.scenario} is the highest-priority segment because low SLA, high handoff wait, and weak customer sentiment stack together.</p>
        <a href="#business-case">Review opportunity</a>
      </aside>
    </section>

    <section class="kpi-grid">
      ${data.kpis.map((item) => `
        <article>
          <span>${item.label}</span>
          <strong>${item.value}</strong>
          <em>${item.note}</em>
        </article>
      `).join("")}
    </section>

    <section class="surface surface--split">
      <article class="panel">
        <div class="section-title">
          <p class="eyebrow">Surface 1</p>
          <h2>Operating Cockpit</h2>
        </div>
        <div class="bar-stack">
          ${metricBar("Under-25-minute SLA", data.topSegment.under_25_min_sla_pct)}
          ${metricBar("Order accuracy", data.topSegment.order_accuracy_pct)}
          ${metricBar("Capacity utilization", data.topSegment.capacity_utilization_pct, "%", true)}
          ${metricBar("Sentiment score", data.topSegment.sentiment_score)}
        </div>
      </article>
      <article class="panel queue-panel">
        <div class="section-title">
          <p class="eyebrow">Fulfillment queue</p>
          <h2>Where product action is needed</h2>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Segment</th>
                <th>Orders</th>
                <th>SLA</th>
                <th>Wait</th>
                <th>Contact</th>
                <th>Decision</th>
              </tr>
            </thead>
            <tbody>${segmentRows}</tbody>
          </table>
        </div>
      </article>
    </section>

    <section class="surface" id="business-case">
      <div class="section-title">
        <p class="eyebrow">Surface 2</p>
        <h2>Opportunity Assessment and Business Case</h2>
      </div>
      <div class="business-grid">
        ${initiativeCards}
      </div>
    </section>

    <section class="surface surface--split" id="requirements">
      <article class="panel">
        <div class="section-title">
          <p class="eyebrow">Surface 3</p>
          <h2>PRD Requirements and Acceptance Criteria</h2>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Requirement</th>
                <th>Metric</th>
                <th>Owner</th>
              </tr>
            </thead>
            <tbody>${requirementRows}</tbody>
          </table>
        </div>
      </article>
      <aside class="ops-stack">
        <div class="panel">
          <div class="section-title">
            <p class="eyebrow">Voice of customer</p>
            <h2>Feedback themes</h2>
          </div>
          <div class="feedback-grid">${feedbackRows}</div>
        </div>
        <div class="panel">
          <div class="section-title">
            <p class="eyebrow">Partner ops</p>
            <h2>Decision cadence</h2>
          </div>
          <ul class="partner-list">${partnerRows}</ul>
        </div>
      </aside>
    </section>
  </main>
`;
