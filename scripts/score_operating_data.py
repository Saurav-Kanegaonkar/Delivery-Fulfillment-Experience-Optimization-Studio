import csv
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"
SRC = ROOT / "src"

random.seed(42)

SEGMENTS = [
    {
        "segment_id": "SEG01",
        "name": "Peak espresso rush delivery",
        "scenario": "Morning rush",
        "channel": "Third-party marketplace",
        "owner": "Store operations",
        "baseline_orders": 920,
        "capacity": 88,
        "food_attach": 0.47,
        "prep": 9.4,
        "wait": 4.2,
        "delivery": 10.7,
        "accuracy": 96.8,
        "sentiment": 69,
    },
    {
        "segment_id": "SEG02",
        "name": "Owned-app delivery handoff",
        "scenario": "Morning rush",
        "channel": "Owned app delivery",
        "owner": "Digital product",
        "baseline_orders": 640,
        "capacity": 82,
        "food_attach": 0.52,
        "prep": 8.7,
        "wait": 3.5,
        "delivery": 10.3,
        "accuracy": 97.6,
        "sentiment": 74,
    },
    {
        "segment_id": "SEG03",
        "name": "Food-heavy lunch bundles",
        "scenario": "Lunch",
        "channel": "Third-party marketplace",
        "owner": "Menu operations",
        "baseline_orders": 710,
        "capacity": 76,
        "food_attach": 0.68,
        "prep": 10.8,
        "wait": 3.9,
        "delivery": 11.2,
        "accuracy": 95.9,
        "sentiment": 66,
    },
    {
        "segment_id": "SEG04",
        "name": "Suburban drive-thru collision",
        "scenario": "Morning rush",
        "channel": "Mixed digital",
        "owner": "Store operations",
        "baseline_orders": 860,
        "capacity": 91,
        "food_attach": 0.41,
        "prep": 9.8,
        "wait": 5.1,
        "delivery": 11.0,
        "accuracy": 96.1,
        "sentiment": 63,
    },
    {
        "segment_id": "SEG05",
        "name": "Driver arrival before make-ready",
        "scenario": "All-day",
        "channel": "Third-party marketplace",
        "owner": "Delivery partnerships",
        "baseline_orders": 560,
        "capacity": 73,
        "food_attach": 0.44,
        "prep": 8.1,
        "wait": 6.4,
        "delivery": 10.5,
        "accuracy": 97.0,
        "sentiment": 61,
    },
    {
        "segment_id": "SEG06",
        "name": "High-rise courier dwell",
        "scenario": "Urban core",
        "channel": "Third-party marketplace",
        "owner": "Delivery partnerships",
        "baseline_orders": 430,
        "capacity": 69,
        "food_attach": 0.39,
        "prep": 7.9,
        "wait": 4.8,
        "delivery": 14.0,
        "accuracy": 97.4,
        "sentiment": 65,
    },
    {
        "segment_id": "SEG07",
        "name": "Cold beverage customization",
        "scenario": "Afternoon",
        "channel": "Owned app delivery",
        "owner": "Digital product",
        "baseline_orders": 510,
        "capacity": 70,
        "food_attach": 0.31,
        "prep": 8.5,
        "wait": 2.9,
        "delivery": 10.1,
        "accuracy": 94.8,
        "sentiment": 62,
    },
    {
        "segment_id": "SEG08",
        "name": "Late-day promotion spike",
        "scenario": "Promotion",
        "channel": "Third-party marketplace",
        "owner": "Growth partnerships",
        "baseline_orders": 780,
        "capacity": 94,
        "food_attach": 0.36,
        "prep": 11.2,
        "wait": 5.7,
        "delivery": 11.5,
        "accuracy": 95.4,
        "sentiment": 58,
    },
    {
        "segment_id": "SEG09",
        "name": "Low-volume cafe delivery",
        "scenario": "All-day",
        "channel": "Third-party marketplace",
        "owner": "Store operations",
        "baseline_orders": 260,
        "capacity": 54,
        "food_attach": 0.29,
        "prep": 6.9,
        "wait": 2.1,
        "delivery": 9.7,
        "accuracy": 98.3,
        "sentiment": 82,
    },
    {
        "segment_id": "SEG10",
        "name": "Airport and campus pickup zones",
        "scenario": "Travel hub",
        "channel": "Mixed digital",
        "owner": "Store operations",
        "baseline_orders": 390,
        "capacity": 81,
        "food_attach": 0.43,
        "prep": 9.5,
        "wait": 5.6,
        "delivery": 12.5,
        "accuracy": 96.5,
        "sentiment": 60,
    },
]

INITIATIVES = [
    {
        "initiative_id": "OPP01",
        "title": "Capacity-aware delivery promise",
        "segments": ["SEG01", "SEG04", "SEG08"],
        "problem": "Delivery promises do not consistently reflect store load during peak or promotion windows.",
        "solution": "Throttle or shift quoted ready times when cafe, mobile, drive-thru, and delivery queues exceed capacity.",
        "effort": 8,
        "confidence": 0.78,
        "partner_complexity": 0.44,
        "order_lift": 2.8,
        "refund_reduction": 0.34,
        "labor_minutes_saved": 116,
        "rollout": "Pilot in high-volume morning and promotion stores",
    },
    {
        "initiative_id": "OPP02",
        "title": "Driver-arrival pacing signal",
        "segments": ["SEG05", "SEG06", "SEG10"],
        "problem": "Couriers often arrive before the order is sealed, creating dwell time and counter congestion.",
        "solution": "Send partner platforms a make-ready signal that releases drivers closer to actual handoff time.",
        "effort": 7,
        "confidence": 0.74,
        "partner_complexity": 0.62,
        "order_lift": 1.8,
        "refund_reduction": 0.22,
        "labor_minutes_saved": 92,
        "rollout": "Partner integration test with two courier platforms",
    },
    {
        "initiative_id": "OPP03",
        "title": "Food bundle readiness checklist",
        "segments": ["SEG03", "SEG01"],
        "problem": "Food-heavy delivery bundles increase missing-item contacts and remake work.",
        "solution": "Add a packaging confirmation step for food items and bag-level label checks.",
        "effort": 4,
        "confidence": 0.82,
        "partner_complexity": 0.22,
        "order_lift": 1.2,
        "refund_reduction": 0.41,
        "labor_minutes_saved": 71,
        "rollout": "Launch as standard work in food-heavy cafes",
    },
    {
        "initiative_id": "OPP04",
        "title": "Customization risk guardrail",
        "segments": ["SEG07", "SEG02"],
        "problem": "Complex customized beverages have higher defect and negative feedback rates in delivery.",
        "solution": "Flag high-risk builds, simplify delivery-specific modifier defaults, and add packout verification.",
        "effort": 6,
        "confidence": 0.69,
        "partner_complexity": 0.35,
        "order_lift": 1.5,
        "refund_reduction": 0.29,
        "labor_minutes_saved": 64,
        "rollout": "A/B test on cold beverage delivery orders",
    },
    {
        "initiative_id": "OPP05",
        "title": "Partner exception weekly review",
        "segments": ["SEG05", "SEG08", "SEG10"],
        "problem": "Partner asks and escalations arrive faster than teams can separate urgent defects from noise.",
        "solution": "Create a weekly operating review that classifies exceptions by SLA, defect cost, and owner.",
        "effort": 3,
        "confidence": 0.86,
        "partner_complexity": 0.28,
        "order_lift": 0.7,
        "refund_reduction": 0.18,
        "labor_minutes_saved": 130,
        "rollout": "Standardize across product, operations, and partner management",
    },
    {
        "initiative_id": "OPP06",
        "title": "Delivery shelf zoning guide",
        "segments": ["SEG04", "SEG06", "SEG10"],
        "problem": "Physical handoff zones are inconsistent, especially where mobile pickup and delivery share space.",
        "solution": "Define shelf zones, courier pickup cues, and exception handling by store format.",
        "effort": 5,
        "confidence": 0.71,
        "partner_complexity": 0.31,
        "order_lift": 1.0,
        "refund_reduction": 0.17,
        "labor_minutes_saved": 83,
        "rollout": "Store-format playbook with before and after measurement",
    },
]

REQUIREMENTS = [
    {
        "req_id": "REQ01",
        "initiative_id": "OPP01",
        "requirement": "Calculate a live delivery promise adjustment from channel queue, labor capacity, and make-line load.",
        "acceptance": "Quoted delivery-ready time shifts when capacity utilization exceeds 88% for 15 minutes.",
        "metric": "Under-25-minute SLA",
        "owner": "Digital product",
    },
    {
        "req_id": "REQ02",
        "initiative_id": "OPP01",
        "requirement": "Expose a capacity reason code in the partner operations digest.",
        "acceptance": "Every adjusted promise includes a source reason and recovery owner.",
        "metric": "Escalations with owner",
        "owner": "Store operations",
    },
    {
        "req_id": "REQ03",
        "initiative_id": "OPP02",
        "requirement": "Publish make-ready event timing to delivery partners for eligible orders.",
        "acceptance": "Partner receives make-ready signal within 60 seconds of bag seal scan.",
        "metric": "Courier wait minutes",
        "owner": "Delivery partnerships",
    },
    {
        "req_id": "REQ04",
        "initiative_id": "OPP03",
        "requirement": "Add food item confirmation before delivery bag handoff.",
        "acceptance": "Bag cannot be marked ready until required food items are confirmed.",
        "metric": "Missing-item contact rate",
        "owner": "Menu operations",
    },
    {
        "req_id": "REQ05",
        "initiative_id": "OPP04",
        "requirement": "Flag high-risk customization combinations on delivery orders.",
        "acceptance": "The top 20 high-defect modifier combinations receive a packout alert.",
        "metric": "Order accuracy",
        "owner": "Digital product",
    },
    {
        "req_id": "REQ06",
        "initiative_id": "OPP05",
        "requirement": "Create a weekly partner exception packet with decision status.",
        "acceptance": "At least 95% of partner asks are classified as ship, test, defer, or monitor.",
        "metric": "Partner request aging",
        "owner": "Partner management",
    },
    {
        "req_id": "REQ07",
        "initiative_id": "OPP06",
        "requirement": "Attach store-format handoff instructions to each pilot store.",
        "acceptance": "Each pilot store has a documented shelf zone and courier pickup cue.",
        "metric": "Handoff wait minutes",
        "owner": "Store operations",
    },
]


def clamp(value, low, high):
    return max(low, min(high, value))


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_daily_metrics():
    rows = []
    start = date(2026, 1, 5)
    for day_offset in range(84):
        current = start + timedelta(days=day_offset)
        weekday_multiplier = 1.12 if current.weekday() < 5 else 0.86
        for seg in SEGMENTS:
            promo_multiplier = 1.18 if seg["scenario"] == "Promotion" and current.weekday() in [3, 4] else 1.0
            rush_multiplier = 1.1 if seg["scenario"] == "Morning rush" and current.weekday() < 5 else 1.0
            noise = random.normalvariate(1.0, 0.07)
            orders = max(60, round(seg["baseline_orders"] * weekday_multiplier * promo_multiplier * rush_multiplier * noise))
            prep = clamp(random.normalvariate(seg["prep"], 0.75), 5.5, 13.8)
            wait = clamp(random.normalvariate(seg["wait"], 0.85), 1.2, 8.5)
            delivery = clamp(random.normalvariate(seg["delivery"], 1.1), 7.5, 17.5)
            total_time = prep + wait + delivery
            sla = clamp(100 - max(0, total_time - 21) * 5.7 + random.normalvariate(0, 2.0), 54, 98.5)
            accuracy = clamp(random.normalvariate(seg["accuracy"], 0.75), 92, 99.4)
            refund_rate = clamp((100 - accuracy) * 0.18 + max(0, total_time - 25) * 0.11 + random.normalvariate(0.15, 0.05), 0.12, 2.9)
            contact_rate = clamp((100 - sla) * 0.035 + (100 - accuracy) * 0.11 + random.normalvariate(0.18, 0.06), 0.25, 4.8)
            cancel_rate = clamp(max(0, wait - 4) * 0.22 + random.normalvariate(0.35, 0.09), 0.08, 2.7)
            capacity = clamp(random.normalvariate(seg["capacity"], 5.5), 43, 99)
            sentiment = clamp(random.normalvariate(seg["sentiment"], 5.0) - max(0, total_time - 25) * 1.4, 35, 92)
            rows.append(
                {
                    "date": current.isoformat(),
                    "segment_id": seg["segment_id"],
                    "orders": orders,
                    "avg_ticket_usd": round(random.normalvariate(18.8 if seg["channel"] != "Owned app delivery" else 20.1, 1.3), 2),
                    "food_attach_rate_pct": round(clamp(random.normalvariate(seg["food_attach"] * 100, 3.5), 18, 76), 1),
                    "prep_minutes": round(prep, 1),
                    "handoff_wait_minutes": round(wait, 1),
                    "delivery_minutes": round(delivery, 1),
                    "under_25_min_sla_pct": round(sla, 1),
                    "order_accuracy_pct": round(accuracy, 1),
                    "refund_rate_pct": round(refund_rate, 2),
                    "customer_contact_rate_pct": round(contact_rate, 2),
                    "partner_cancel_rate_pct": round(cancel_rate, 2),
                    "capacity_utilization_pct": round(capacity, 1),
                    "sentiment_score": round(sentiment, 1),
                }
            )
    return rows


def summarize_segments(daily_rows):
    grouped = {seg["segment_id"]: [] for seg in SEGMENTS}
    for row in daily_rows:
        grouped[row["segment_id"]].append(row)

    summary_rows = []
    for seg in SEGMENTS:
        rows = grouped[seg["segment_id"]]
        orders = sum(int(r["orders"]) for r in rows)
        avg = lambda key: sum(float(r[key]) for r in rows) / len(rows)
        sla_gap = max(0, 92 - avg("under_25_min_sla_pct"))
        accuracy_gap = max(0, 98 - avg("order_accuracy_pct"))
        wait_gap = max(0, avg("handoff_wait_minutes") - 3.2)
        capacity_drag = max(0, avg("capacity_utilization_pct") - 78)
        cx_drag = (100 - avg("sentiment_score")) / 100
        priority_score = (
            sla_gap * 1.6
            + accuracy_gap * 5.8
            + wait_gap * 6.4
            + capacity_drag * 0.9
            + avg("customer_contact_rate_pct") * 4.1
            + cx_drag * 18
        )
        weekly_orders = orders / 12
        estimated_weekly_drag = weekly_orders * (avg("refund_rate_pct") / 100) * 18.5 + weekly_orders * avg("customer_contact_rate_pct") / 100 * 3.4
        summary_rows.append(
            {
                "segment_id": seg["segment_id"],
                "segment_name": seg["name"],
                "scenario": seg["scenario"],
                "channel": seg["channel"],
                "owner": seg["owner"],
                "weekly_orders": round(weekly_orders),
                "under_25_min_sla_pct": round(avg("under_25_min_sla_pct"), 1),
                "order_accuracy_pct": round(avg("order_accuracy_pct"), 1),
                "handoff_wait_minutes": round(avg("handoff_wait_minutes"), 1),
                "capacity_utilization_pct": round(avg("capacity_utilization_pct"), 1),
                "customer_contact_rate_pct": round(avg("customer_contact_rate_pct"), 2),
                "sentiment_score": round(avg("sentiment_score"), 1),
                "estimated_weekly_drag_usd": round(estimated_weekly_drag),
                "priority_score": round(priority_score, 1),
                "decision": "Intervene" if priority_score >= 48 else "Test" if priority_score >= 34 else "Monitor",
            }
        )
    return sorted(summary_rows, key=lambda row: row["priority_score"], reverse=True)


def score_initiatives(segment_rows):
    segment_lookup = {row["segment_id"]: row for row in segment_rows}
    rows = []
    for item in INITIATIVES:
        target_segments = [segment_lookup[seg_id] for seg_id in item["segments"]]
        weekly_orders = sum(int(row["weekly_orders"]) for row in target_segments)
        baseline_drag = sum(int(row["estimated_weekly_drag_usd"]) for row in target_segments)
        avg_priority = sum(float(row["priority_score"]) for row in target_segments) / len(target_segments)
        gross_monthly_value = baseline_drag * item["refund_reduction"] * 4.33 + weekly_orders * item["order_lift"] / 100 * 4.33 * 18.9
        labor_value = item["labor_minutes_saved"] * 4.33 * 0.42
        confidence_adjusted_value = (gross_monthly_value + labor_value) * item["confidence"]
        complexity_penalty = 1 + item["partner_complexity"] + item["effort"] / 16
        opportunity_score = confidence_adjusted_value / complexity_penalty / 100
        rows.append(
            {
                "initiative_id": item["initiative_id"],
                "title": item["title"],
                "problem": item["problem"],
                "solution": item["solution"],
                "target_segments": ", ".join(item["segments"]),
                "weekly_orders_in_scope": round(weekly_orders),
                "baseline_weekly_drag_usd": round(baseline_drag),
                "expected_order_lift_pct": item["order_lift"],
                "expected_refund_reduction_pct": round(item["refund_reduction"] * 100),
                "labor_minutes_saved_weekly": item["labor_minutes_saved"],
                "confidence_pct": round(item["confidence"] * 100),
                "effort_points": item["effort"],
                "partner_complexity": "High" if item["partner_complexity"] > 0.55 else "Medium" if item["partner_complexity"] > 0.3 else "Low",
                "monthly_value_usd": round(confidence_adjusted_value),
                "opportunity_score": round(opportunity_score, 1),
                "rollout_recommendation": item["rollout"],
                "decision": "Ship pilot" if opportunity_score >= 55 else "Discovery sprint" if opportunity_score >= 35 else "Monitor",
                "avg_segment_priority": round(avg_priority, 1),
            }
        )
    return sorted(rows, key=lambda row: row["opportunity_score"], reverse=True)


def generate_feedback(segment_rows):
    themes = [
        ("Delivery arrived later than quoted", "Promise accuracy"),
        ("Courier waited at counter", "Partner handoff"),
        ("Missing food item", "Packaging accuracy"),
        ("Drink customization missed", "Make accuracy"),
        ("Order not sealed clearly", "Packaging trust"),
        ("Driver could not identify pickup shelf", "Store wayfinding"),
    ]
    rows = []
    for idx, segment in enumerate(segment_rows, start=1):
        for theme, category in themes[:4 if segment["priority_score"] > 38 else 2]:
            volume = round((100 - float(segment["sentiment_score"])) * random.uniform(4.0, 7.0))
            rows.append(
                {
                    "feedback_id": f"FB{idx:02d}{len(rows) + 1:03d}",
                    "segment_id": segment["segment_id"],
                    "category": category,
                    "theme": theme,
                    "weekly_mentions": max(8, volume),
                    "severity": "High" if volume > 180 else "Medium" if volume > 95 else "Low",
                    "product_question": "Should we change the promise, handoff, packaging, or requirement before scaling?",
                }
            )
    return rows


def make_partner_plan(initiative_rows):
    rows = []
    for item in initiative_rows:
        if item["decision"] == "Ship pilot":
            cadence = "Weekly launch review"
            escalation = "SLA miss above 8% or partner cancel rate above 1.5%"
        elif item["decision"] == "Discovery sprint":
            cadence = "Two-week discovery review"
            escalation = "Unowned requirement, unclear metric, or partner dependency blocked"
        else:
            cadence = "Monthly monitor"
            escalation = "Feedback severity moves to high"
        rows.append(
            {
                "initiative_id": item["initiative_id"],
                "title": item["title"],
                "partner_touchpoint": cadence,
                "ops_owner": "Store operations" if "capacity" in item["problem"].lower() or "counter" in item["problem"].lower() else "Delivery partnerships",
                "decision_packet": f"{item['decision']} with {item['confidence_pct']}% confidence",
                "escalation_rule": escalation,
                "next_review": "2026-04-17",
            }
        )
    return rows


def make_app_payload(segment_rows, initiative_rows, feedback_rows, partner_rows):
    top = segment_rows[0]
    total_weekly_orders = sum(int(row["weekly_orders"]) for row in segment_rows)
    avg_sla = sum(float(row["under_25_min_sla_pct"]) * int(row["weekly_orders"]) for row in segment_rows) / total_weekly_orders
    avg_accuracy = sum(float(row["order_accuracy_pct"]) * int(row["weekly_orders"]) for row in segment_rows) / total_weekly_orders
    top_initiative = initiative_rows[0]
    return {
        "kpis": [
            {"label": "Weekly delivery orders modeled", "value": f"{total_weekly_orders:,}", "note": "synthetic operating baseline"},
            {"label": "Under-25-minute SLA", "value": f"{avg_sla:.1f}%", "note": "weighted by orders"},
            {"label": "Order accuracy", "value": f"{avg_accuracy:.1f}%", "note": "bag and make quality"},
            {"label": "Top monthly value", "value": f"${int(top_initiative['monthly_value_usd']):,}", "note": top_initiative["title"]},
        ],
        "topSegment": top,
        "segments": segment_rows,
        "initiatives": initiative_rows,
        "requirements": REQUIREMENTS,
        "feedback": feedback_rows[:10],
        "partnerPlan": partner_rows,
    }


def main():
    DATA.mkdir(exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    SRC.mkdir(exist_ok=True)

    daily_rows = generate_daily_metrics()
    segment_rows = summarize_segments(daily_rows)
    initiative_rows = score_initiatives(segment_rows)
    feedback_rows = generate_feedback(segment_rows)
    partner_rows = make_partner_plan(initiative_rows)
    payload = make_app_payload(segment_rows, initiative_rows, feedback_rows, partner_rows)

    write_csv(DATA / "delivery_segments.csv", SEGMENTS, list(SEGMENTS[0].keys()))
    write_csv(DATA / "daily_metrics.csv", daily_rows, list(daily_rows[0].keys()))
    write_csv(DATA / "feedback_themes.csv", feedback_rows, list(feedback_rows[0].keys()))
    write_csv(DATA / "requirements_backlog.csv", REQUIREMENTS, list(REQUIREMENTS[0].keys()))
    write_csv(OUTPUTS / "fulfillment_priority_queue.csv", segment_rows, list(segment_rows[0].keys()))
    write_csv(OUTPUTS / "initiative_business_case.csv", initiative_rows, list(initiative_rows[0].keys()))
    write_csv(OUTPUTS / "partner_ops_plan.csv", partner_rows, list(partner_rows[0].keys()))
    write_csv(OUTPUTS / "prd_requirements.csv", REQUIREMENTS, list(REQUIREMENTS[0].keys()))
    (OUTPUTS / "summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (SRC / "app_data.js").write_text("window.deliveryStudioData = " + json.dumps(payload, indent=2) + ";\n", encoding="utf-8")

    print(f"Generated {len(daily_rows):,} daily rows across {len(SEGMENTS)} fulfillment segments.")
    print(f"Top segment: {payload['topSegment']['segment_name']} with priority {payload['topSegment']['priority_score']}.")
    print(f"Top initiative: {initiative_rows[0]['title']} with score {initiative_rows[0]['opportunity_score']}.")


if __name__ == "__main__":
    main()
