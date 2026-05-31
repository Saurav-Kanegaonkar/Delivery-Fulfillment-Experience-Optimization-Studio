-- Data quality checks for the delivery fulfillment artifact.

select
  segment_id,
  count(*) as row_count,
  min(date) as first_date,
  max(date) as last_date
from daily_metrics
group by segment_id
having count(*) <> 84;

select
  segment_id,
  date,
  under_25_min_sla_pct,
  order_accuracy_pct,
  capacity_utilization_pct
from daily_metrics
where under_25_min_sla_pct not between 0 and 100
   or order_accuracy_pct not between 0 and 100
   or capacity_utilization_pct not between 0 and 100;

select
  initiative_id,
  title,
  opportunity_score,
  decision
from initiative_business_case
order by opportunity_score desc;

select
  req_id,
  initiative_id,
  metric,
  owner
from prd_requirements
where acceptance is null
   or metric is null
   or owner is null;
