import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"
PAYLOAD = ROOT / "analysis" / "outputs" / "summary.json"

OUT.mkdir(parents=True, exist_ok=True)

INK = "#17201b"
MUTED = "#667267"
GREEN = "#1f6f4a"
MINT = "#d9efe2"
AMBER = "#c77722"
RED = "#b42318"
BLUE = "#2c6f91"
LINE = "#dfe7dc"
BG = "#f5f7f1"
WHITE = "#ffffff"


def font(size, bold=False):
    base = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
    return ImageFont.truetype(base, size)


def rounded(draw, box, fill=WHITE, outline=LINE, radius=14):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def wrap(draw, text, max_width, fnt):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=fnt) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text(draw, xy, value, size=28, fill=INK, bold=False, max_width=None, line_gap=8):
    fnt = font(size, bold)
    x, y = xy
    lines = wrap(draw, value, max_width, fnt) if max_width else [value]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += size + line_gap
    return y


def base(title, eyebrow):
    img = Image.new("RGB", (1400, 900), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1400, 100), fill=WHITE)
    text(draw, (60, 28), eyebrow.upper(), 18, GREEN, True)
    text(draw, (60, 54), title, 34, INK, True)
    return img, draw


def bar(draw, x, y, label, value, color=GREEN):
    text(draw, (x, y), label, 20, MUTED, True)
    text(draw, (x + 500, y), f"{value}%", 20, INK, True)
    draw.rounded_rectangle((x, y + 34, x + 590, y + 52), radius=9, fill="#edf2ea")
    draw.rounded_rectangle((x, y + 34, x + 590 * min(value, 100) / 100, y + 52), radius=9, fill=color)


def cockpit(payload):
    img, draw = base("Operating Cockpit", "Surface 1")
    top = payload["topSegment"]
    rounded(draw, (60, 135, 1320, 310))
    text(draw, (90, 165), "Current decision", 18, AMBER, True)
    text(draw, (90, 198), top["segment_name"], 36, INK, True)
    text(draw, (90, 246), f"{top['scenario']} · {top['channel']} · {top['decision']}", 24, MUTED, False)
    text(draw, (930, 170), str(top["priority_score"]), 66, RED, True)
    text(draw, (930, 244), "priority score", 20, MUTED, True)

    rounded(draw, (60, 340, 680, 790))
    text(draw, (90, 370), "Top segment signal", 28, INK, True)
    bar(draw, 90, 430, "Under-25-minute SLA", top["under_25_min_sla_pct"], BLUE)
    bar(draw, 90, 520, "Order accuracy", top["order_accuracy_pct"], GREEN)
    bar(draw, 90, 610, "Capacity utilization", top["capacity_utilization_pct"], RED)
    bar(draw, 90, 700, "Sentiment score", top["sentiment_score"], AMBER)

    rounded(draw, (720, 340, 1320, 790))
    text(draw, (750, 370), "Fulfillment queue", 28, INK, True)
    y = 430
    for row in payload["segments"][:5]:
        text(draw, (750, y), row["segment_name"], 20, INK, True, 360)
        text(draw, (1150, y), row["decision"], 18, RED if row["decision"] == "Intervene" else BLUE, True)
        text(draw, (750, y + 30), f"SLA {row['under_25_min_sla_pct']}% · wait {row['handoff_wait_minutes']} min · contact {row['customer_contact_rate_pct']}%", 18, MUTED)
        draw.line((750, y + 68, 1285, y + 68), fill=LINE, width=2)
        y += 72
    img.save(OUT / "cockpit.png")


def business_case(payload):
    img, draw = base("Opportunity Assessment and Business Case", "Surface 2")
    cards = payload["initiatives"][:6]
    positions = [(60, 140), (490, 140), (920, 140), (60, 520), (490, 520), (920, 520)]
    for idx, (item, pos) in enumerate(zip(cards, positions), start=1):
        x, y = pos
        rounded(draw, (x, y, x + 380, y + 320))
        draw.rounded_rectangle((x + 24, y + 24, x + 74, y + 74), radius=10, fill=GREEN)
        text(draw, (x + 36, y + 37), f"{idx:02d}", 18, WHITE, True)
        text(draw, (x + 90, y + 24), item["decision"], 16, GREEN, True)
        text(draw, (x + 90, y + 54), item["title"], 25, INK, True, 250, 5)
        text(draw, (x + 24, y + 128), item["solution"], 18, MUTED, False, 320, 6)
        text(draw, (x + 24, y + 238), f"Score {item['opportunity_score']}", 24, INK, True)
        text(draw, (x + 190, y + 238), f"${item['monthly_value_usd']:,}", 24, INK, True)
        text(draw, (x + 24, y + 276), f"{item['confidence_pct']}% confidence · effort {item['effort_points']}", 18, MUTED)
    img.save(OUT / "business-case.png")


def requirements(payload):
    img, draw = base("Requirements and Partner Ops", "Surface 3")
    rounded(draw, (60, 135, 860, 805))
    text(draw, (90, 165), "PRD requirements", 30, INK, True)
    y = 220
    for row in payload["requirements"][:4]:
        text(draw, (90, y), f"{row['req_id']} · {row['metric']}", 18, GREEN, True)
        text(draw, (90, y + 28), row["requirement"], 20, INK, True, 700, 4)
        text(draw, (90, y + 82), row["acceptance"], 18, MUTED, False, 700, 4)
        draw.line((90, y + 132, 825, y + 132), fill=LINE, width=2)
        y += 144

    rounded(draw, (900, 135, 1320, 430))
    text(draw, (930, 165), "Feedback themes", 28, INK, True)
    y = 220
    for row in payload["feedback"][:4]:
        text(draw, (930, y), row["category"], 16, GREEN, True)
        text(draw, (930, y + 24), row["theme"], 19, INK, True, 330)
        y += 54

    rounded(draw, (900, 455, 1320, 805))
    text(draw, (930, 485), "Partner cadence", 28, INK, True)
    y = 540
    for row in payload["partnerPlan"][:4]:
        text(draw, (930, y), row["title"], 18, INK, True, 330)
        text(draw, (930, y + 27), row["partner_touchpoint"], 17, GREEN, True)
        y += 70
    img.save(OUT / "requirements.png")


def main():
    payload = json.loads(PAYLOAD.read_text())
    cockpit(payload)
    business_case(payload)
    requirements(payload)
    print("Rendered README images to docs/images.")


if __name__ == "__main__":
    main()
