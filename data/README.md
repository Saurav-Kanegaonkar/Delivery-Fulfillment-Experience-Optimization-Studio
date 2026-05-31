# Data Sources

This project uses synthetic operating data for a large coffeehouse and restaurant delivery program. The data is not real company performance.

The generation script models public delivery and store-operations patterns:

- Delivery is available across eligible company-operated stores through owned and third-party channels.
- Delivery orders are modeled as higher-ticket orders than in-store purchases, with food attachment as a key complexity driver.
- Average end-to-end delivery promises are centered near a 25-minute customer expectation.
- Store capacity, courier timing, food bundle complexity, pickup shelf design, and order customization affect SLA, accuracy, refunds, and feedback.

Files:

- `delivery_segments.csv`: 10 fulfillment scenarios with owner, channel, capacity, and baseline assumptions.
- `daily_metrics.csv`: 840 segment-day rows across 12 weeks.
- `feedback_themes.csv`: modeled customer feedback categories and weekly mention counts.
- `requirements_backlog.csv`: PRD requirements, acceptance criteria, metric, and owner.

Derived outputs in `analysis/outputs`:

- `fulfillment_priority_queue.csv`: ranked delivery segments by SLA gap, accuracy gap, handoff wait, capacity pressure, customer contact rate, and sentiment.
- `initiative_business_case.csv`: product opportunities scored by value, confidence, effort, and partner complexity.
- `partner_ops_plan.csv`: partner and operations review cadence for each opportunity.
- `prd_requirements.csv`: requirements table for the product-management surface.
- `summary.json`: data payload used by the static web artifact.
