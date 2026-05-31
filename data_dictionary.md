# Data Dictionary

## `data/delivery_segments.csv`

- `segment_id`: Stable fulfillment segment key.
- `name`: Delivery scenario label used in the product artifact.
- `scenario`: Operating context such as morning rush, promotion, or travel hub.
- `channel`: Owned app delivery, third-party marketplace, or mixed digital.
- `owner`: Primary accountable team.
- `baseline_orders`: Synthetic baseline weekly demand before daily variation.
- `capacity`: Modeled store capacity pressure.
- `food_attach`: Modeled share of orders that include food.
- `prep`, `wait`, `delivery`: Baseline minutes for make, handoff, and courier travel.
- `accuracy`: Baseline order accuracy percent.
- `sentiment`: Baseline customer sentiment score.

## `data/daily_metrics.csv`

- `date`: Modeled operating date.
- `segment_id`: Segment key.
- `orders`: Modeled daily delivery orders.
- `avg_ticket_usd`: Modeled average ticket.
- `food_attach_rate_pct`: Percent of orders containing food.
- `prep_minutes`: Average make-line preparation time.
- `handoff_wait_minutes`: Courier wait or handoff dwell time.
- `delivery_minutes`: Courier travel time.
- `under_25_min_sla_pct`: Share of orders modeled below 25 minutes.
- `order_accuracy_pct`: Share of orders with no make or packout defect.
- `refund_rate_pct`: Percent of orders refunded or credited.
- `customer_contact_rate_pct`: Percent of orders generating support or negative feedback.
- `partner_cancel_rate_pct`: Partner cancellation or courier reassignment rate.
- `capacity_utilization_pct`: Store fulfillment capacity usage.
- `sentiment_score`: Modeled customer feedback score.

## `analysis/outputs/initiative_business_case.csv`

- `initiative_id`: Product opportunity key.
- `title`: Product or operational change name.
- `problem`: User, partner, or operations pain point.
- `solution`: Proposed product or process intervention.
- `target_segments`: Segments in scope.
- `weekly_orders_in_scope`: Modeled order volume affected.
- `baseline_weekly_drag_usd`: Estimated weekly refund and contact drag.
- `expected_order_lift_pct`: Modeled delivery order lift after improvement.
- `expected_refund_reduction_pct`: Expected refund reduction.
- `labor_minutes_saved_weekly`: Estimated weekly labor minutes returned.
- `confidence_pct`: Confidence estimate based on metric clarity and execution path.
- `effort_points`: Relative product and operations effort.
- `partner_complexity`: Low, medium, or high dependency level.
- `monthly_value_usd`: Confidence-adjusted modeled value.
- `opportunity_score`: Prioritization score after complexity and effort penalty.
- `rollout_recommendation`: Suggested pilot or rollout path.
- `decision`: Ship pilot, discovery sprint, or monitor.
