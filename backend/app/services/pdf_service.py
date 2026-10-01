"""
TripGenius — Publication-Grade Structured PDF Itinerary Generator.

Generates beautifully formatted, multi-page vector PDF travel documents
leveraging ReportLab and Pillow (PIL) for image optimization, with exact
coverage of the 5 core sections:
1. Day-by-Day Timeline
2. Stays & Food (with Google ratings)
3. Cost Breakdown (including Rental Vehicle Pricing Intelligence)
4. Weather & Packing Intelligence
5. Eco & Sustainability Report
"""

import re
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ----------------------------------------------------
# UNICODE FONT REGISTRATION (NATIVE RUPEE SYMBOL SUPPORT)
# ----------------------------------------------------
MAIN_FONT = "Helvetica"
MAIN_FONT_BOLD = "Helvetica-Bold"
HAS_UNICODE_RUPEE = False


def _init_pdf_fonts():
    global MAIN_FONT, MAIN_FONT_BOLD, HAS_UNICODE_RUPEE
    # TrueType fonts supporting Unicode & Indian Rupee symbol (U+20B9)
    candidates = [
        ("SegoeUI", Path("C:/Windows/Fonts/segoeui.ttf"), "SegoeUI-Bold", Path("C:/Windows/Fonts/segoeuib.ttf")),
        ("NotoSans", Path("C:/Windows/Fonts/NotoSans-Regular.ttf"), "NotoSans-Bold", Path("C:/Windows/Fonts/NotoSans-Bold.ttf")),
        ("Roboto", Path("C:/Windows/Fonts/Roboto-Regular.ttf"), "Roboto-Bold", Path("C:/Windows/Fonts/Roboto-Bold_2.ttf")),
        ("DejaVuSans", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), "DejaVuSans-Bold", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")),
    ]
    for reg_name, reg_path, bold_name, bold_path in candidates:
        if reg_path.exists() and bold_path.exists():
            try:
                pdfmetrics.registerFont(TTFont(reg_name, str(reg_path)))
                pdfmetrics.registerFont(TTFont(bold_name, str(bold_path)))
                MAIN_FONT = reg_name
                MAIN_FONT_BOLD = bold_name
                HAS_UNICODE_RUPEE = True
                break
            except Exception:
                continue


_init_pdf_fonts()


def sanitize_pdf_text(text: Any) -> str:
    """
    Cleans text for ReportLab PDF rendering:
    1. If the registered font does not support native Rupee, fall back to 'Rs. '.
    2. Strips multi-byte color emojis that cause black boxes/tofu (■) in PDF output.
    """
    if not text:
        return ""
    str_val = str(text)
    if not HAS_UNICODE_RUPEE:
        str_val = str_val.replace("₹", "Rs. ")

    # Strip emoji Unicode ranges that lack glyphs in standard vector font tables
    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff"  # Supplemental Multilingual Plane (emojis)
        "\u2600-\u27bf"           # Miscellaneous Symbols & Dingbats
        "\ufe00-\ufe0f"           # Variation Selectors
        "\u200d"                  # Zero-width joiner
        "]+",
        flags=re.UNICODE,
    )
    cleaned = emoji_pattern.sub("", str_val)
    return re.sub(r" +", " ", cleaned).strip()


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw 'Page X of Y' and branded footer.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        self.setFont(MAIN_FONT, 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Top Header on pages > 1
        if self._pageNumber > 1:
            self.drawString(
                54, 750, "Trip Geni AI Travel Studio  •  Personalized Travel Plan"
            )
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Running Bottom Footer on all pages
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        self.drawString(
            54,
            32,
            "Trip Geni  |  Confidential Traveler Itinerary  |  tripgeni.ai",
        )
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


class TripPDFGenerator:
    """
    Constructs an elegant, publication-quality PDF from TripGenius trip data.
    """

    PRIMARY_COLOR = colors.HexColor("#0284C7")  # Sky 600
    PRIMARY_DARK = colors.HexColor("#0F172A")  # Slate 900
    ACCENT_TEAL = colors.HexColor("#0D9488")  # Teal 600
    ACCENT_AMBER = colors.HexColor("#D97706")  # Amber 600
    TEXT_DARK = colors.HexColor("#1E293B")  # Slate 800
    TEXT_MUTED = colors.HexColor("#64748B")  # Slate 500
    BG_LIGHT = colors.HexColor("#F8FAFC")  # Slate 50
    BORDER_LIGHT = colors.HexColor("#E2E8F0")  # Slate 200

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._init_custom_styles()

    def _init_custom_styles(self):
        self.title_style = ParagraphStyle(
            "DocTitle",
            parent=self.styles["Heading1"],
            fontName=MAIN_FONT_BOLD,
            fontSize=22,
            leading=26,
            textColor=self.PRIMARY_DARK,
            spaceAfter=4,
        )

        self.subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=self.styles["Normal"],
            fontName=MAIN_FONT,
            fontSize=10,
            leading=14,
            textColor=self.TEXT_MUTED,
            spaceAfter=12,
        )

        self.section_heading = ParagraphStyle(
            "SectionHeading",
            parent=self.styles["Heading2"],
            fontName=MAIN_FONT_BOLD,
            fontSize=13,
            leading=16,
            textColor=self.PRIMARY_COLOR,
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True,
        )

        self.sub_heading = ParagraphStyle(
            "SubHeading",
            parent=self.styles["Heading3"],
            fontName=MAIN_FONT_BOLD,
            fontSize=10.5,
            leading=13,
            textColor=self.PRIMARY_DARK,
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True,
        )

        self.body_style = ParagraphStyle(
            "DocBody",
            parent=self.styles["Normal"],
            fontName=MAIN_FONT,
            fontSize=9,
            leading=12.5,
            textColor=self.TEXT_DARK,
            spaceAfter=4,
        )

        self.body_bold = ParagraphStyle(
            "DocBodyBold",
            parent=self.body_style,
            fontName=MAIN_FONT_BOLD,
        )

        self.meta_badge = ParagraphStyle(
            "MetaBadge",
            parent=self.styles["Normal"],
            fontName=MAIN_FONT_BOLD,
            fontSize=8.5,
            leading=11,
            textColor=self.PRIMARY_DARK,
            alignment=TA_CENTER,
        )

        self.meta_label = ParagraphStyle(
            "MetaLabel",
            parent=self.styles["Normal"],
            fontName=MAIN_FONT,
            fontSize=7.5,
            leading=10,
            textColor=self.TEXT_MUTED,
            alignment=TA_CENTER,
        )

    def _find_destination_image(
        self, destination: str, image_url: str | None = None
    ) -> Path | None:
        """
        Search frontend public/destinations directory for destination image.
        Supports explicit image_url from client, destination keyword mapping,
        direct filename matching, and guaranteed fallback to travel.jpg.
        """
        candidates = [
            Path(__file__).resolve().parents[3] / "frontend" / "public" / "destinations",
            Path(__file__).resolve().parents[2] / "frontend" / "public" / "destinations",
            Path.cwd() / "frontend" / "public" / "destinations",
            Path.cwd().parent / "frontend" / "public" / "destinations",
            Path("d:/tripgenius/frontend/public/destinations"),
        ]

        # 1. If client provided explicit image_url (e.g. "/destinations/varanasi.jpg" or "travel.jpg")
        if image_url:
            filename = Path(str(image_url).strip()).name
            for folder in candidates:
                if folder.exists():
                    p = folder / filename
                    if p.exists():
                        return p

        # 2. Check destination substrings and aliases (matching itineraryHelper.ts)
        dest_lower = (destination or "").lower()

        keyword_map = [
            (["varanasi", "kashi", "banaras", "benares", "assi"], "varanasi.jpg"),
            (["ooty", "nilgiri"], "ooty.jpg"),
            (["varkala"], "varkala.jpg"),
            (["delhi", "newdelhi"], "delhi.jpg"),
            (["munnar"], "munnar.jpg"),
            (["goa"], "goa.jpg"),
            (["paris", "france"], "paris.jpg"),
            (["tokyo", "japan"], "tokyo.jpg"),
            (["bali", "indonesia"], "bali.jpg"),
            (["dubai", "uae"], "dubai.jpg"),
            (["thenkasi", "tenkasi", "courtallam", "kutralam"], "thenkasi.jpg"),
            (["coorg", "madikeri", "kodagu"], "coorg.jpg"),
            (["kodaikanal", "kodai"], "kodaikanal.jpg"),
            (["alleppey", "alappuzha"], "alleppey.jpg"),
            (["wayanad"], "wayanad.jpg"),
            (["mysore", "mysuru"], "mysore.jpg"),
            (["hampi"], "hampi.jpg"),
            (["gokarna"], "gokarna.jpg"),
            (["thekkady"], "thekkady.jpg"),
            (["kovalam"], "kovalam.jpg"),
            (["manali"], "manali.jpg"),
        ]

        for keywords, target_file in keyword_map:
            if any(k in dest_lower for k in keywords):
                for folder in candidates:
                    if folder.exists():
                        p = folder / target_file
                        if p.exists():
                            return p

        # 3. Direct filename match
        clean_name = re.sub(r"[^\w]", "", dest_lower)
        for folder in candidates:
            if not folder.exists():
                continue
            for ext in [".jpg", ".jpeg", ".png"]:
                p = folder / f"{clean_name}{ext}"
                if p.exists():
                    return p
                # Check first word
                words = dest_lower.split()
                if words:
                    p2 = folder / f"{words[0]}{ext}"
                    if p2.exists():
                        return p2

        # 4. Universal high-resolution travel photography fallback
        for folder in candidates:
            if folder.exists():
                travel_p = folder / "travel.jpg"
                if travel_p.exists():
                    return travel_p

        return None

    def _process_cover_image(self, img_path: Path) -> BytesIO | None:
        """
        Uses Pillow (PIL) to crop and scale the image to a crisp 504x150 banner
        with optimized JPEG compression.
        """
        try:
            with PILImage.open(img_path) as im:
                im = im.convert("RGB")
                target_w, target_h = 1008, 300  # 2x for sharp print resolution
                orig_w, orig_h = im.size

                target_ratio = target_w / target_h
                orig_ratio = orig_w / orig_h

                if orig_ratio > target_ratio:
                    new_w = int(orig_h * target_ratio)
                    offset_x = (orig_w - new_w) // 2
                    im = im.crop((offset_x, 0, offset_x + new_w, orig_h))
                else:
                    new_h = int(orig_w / target_ratio)
                    offset_y = (orig_h - new_h) // 2
                    im = im.crop((0, offset_y, orig_w, offset_y + new_h))

                im = im.resize((target_w, target_h), PILImage.Resampling.LANCZOS)

                buffer = BytesIO()
                im.save(buffer, format="JPEG", quality=88, optimize=True)
                buffer.seek(0)
                return buffer
        except Exception:
            return None

    def _generate_fallback_banner(self, destination: str) -> BytesIO:
        """Generates an elegant dark gradient banner image with Pillow if no photo is on disk."""
        from PIL import ImageDraw
        w, h = 1008, 260
        base = PILImage.new("RGB", (w, h), (15, 23, 42))  # Slate 900
        draw = ImageDraw.Draw(base)
        for x in range(w):
            pct = x / w
            r = int(14 + (20 - 14) * pct)
            g = int(165 + (184 - 165) * pct)
            b = int(233 + (166 - 233) * pct)
            draw.line([(x, h - 8), (x, h)], fill=(r, g, b))
        
        # Decorative accents
        draw.ellipse([w - 200, -70, w + 70, 200], outline=(30, 41, 59), width=2)
        draw.ellipse([w - 140, -30, w + 30, 140], outline=(56, 189, 248), width=1)

        buffer = BytesIO()
        base.save(buffer, format="JPEG", quality=90)
        buffer.seek(0)
        return buffer

    def build_pdf(self, trip: dict[str, Any]) -> bytes:
        """Generates the full PDF byte stream from trip data."""
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54,
        )

        story = []

        # ----------------------------------------------------
        # 0. HEADER & COVER IMAGE
        # ----------------------------------------------------
        destination = trip.get("destination", "Destination")
        img_url = trip.get("image_url") or trip.get("cover_image")
        img_path = self._find_destination_image(destination, img_url)
        cover_buffer = None
        if img_path:
            cover_buffer = self._process_cover_image(img_path)
        if not cover_buffer:
            cover_buffer = self._generate_fallback_banner(destination)

        if cover_buffer:
            story.append(Image(cover_buffer, width=504, height=125))
            story.append(Spacer(1, 10))

        # Title and Description
        trip_title = trip.get("trip_title") or f"{destination} AI Travel Itinerary"
        story.append(Paragraph(trip_title, self.title_style))

        desc = (
            trip.get("destination_summary")
            or trip.get("itinerary_summary")
            or f"Meticulously curated bespoke journey to {destination} powered by Trip Geni AI."
        )
        story.append(Paragraph(desc, self.subtitle_style))

        # Key Metrics Strip (Table)
        duration_days = trip.get("duration_days", 3)
        travelers = trip.get("travelers_count", 1)
        budget = trip.get("budget", trip.get("estimated_trip_cost", 0))
        eco_score = trip.get("sustainability_score", 85)
        co2_footprint = trip.get("carbon_footprint_estimate", 25)
        travel_style = (trip.get("travel_style") or "Leisure").title()

        metrics_data = [
            [
                Paragraph(f"{duration_days} Days", self.meta_badge),
                Paragraph(f"{travelers} Traveler{'s' if travelers > 1 else ''}", self.meta_badge),
                Paragraph(f"₹{int(budget):,}", self.meta_badge),
                Paragraph(travel_style, self.meta_badge),
                Paragraph(f"{eco_score}/100 Eco", self.meta_badge),
                Paragraph(f"{co2_footprint} kg CO₂", self.meta_badge),
            ],
            [
                Paragraph("Duration", self.meta_label),
                Paragraph("Party Size", self.meta_label),
                Paragraph("Est. Budget", self.meta_label),
                Paragraph("Travel Style", self.meta_label),
                Paragraph("Sustainability", self.meta_label),
                Paragraph("Carbon Footprint", self.meta_label),
            ],
        ]

        metrics_table = Table(metrics_data, colWidths=[84] * 6)
        metrics_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), self.BG_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, self.BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, self.BORDER_LIGHT),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ])
        )
        story.append(metrics_table)
        story.append(Spacer(1, 14))

        # ----------------------------------------------------
        # SECTION 1: DAY-BY-DAY TIMELINE
        # ----------------------------------------------------
        story.append(HRFlowable(width="100%", thickness=1, color=self.PRIMARY_COLOR, spaceAfter=8))
        story.append(Paragraph("1. Day-by-Day Timeline", self.section_heading))

        itinerary = trip.get("ai_itinerary", [])
        if not isinstance(itinerary, list) or len(itinerary) == 0:
            try:
                from app.services.ai_service import get_ai_service
                offline_plan = get_ai_service().generate_offline_trip_plan(
                    destination=destination,
                    duration_days=duration_days,
                    budget=trip.get("budget", 25000),
                    interests=trip.get("interests", ["Sightseeing"]),
                    travelers_count=trip.get("travelers_count", 2),
                    travel_style=trip.get("travel_style", "Balanced"),
                    transportation_mode=trip.get("transportation_mode", "Car"),
                    preferred_accommodation=trip.get("preferred_accommodation", "Standard Hotel"),
                )
                itinerary = offline_plan.get("ai_itinerary", [])
            except Exception:
                itinerary = []

        if isinstance(itinerary, list) and len(itinerary) > 0:
            for idx, day_info in enumerate(itinerary, start=1):
                day_num = day_info.get("day_number") or day_info.get("day") or idx
                day_title = day_info.get("title") or f"Day {day_num}: Exploring {destination}"
                day_theme = day_info.get("theme") or ""
                day_desc = day_info.get("description") or ""

                day_header_text = f"<b>Day {day_num}: {day_title}</b>"
                if day_theme:
                    day_header_text += f" &nbsp;<i>({day_theme})</i>"

                day_elements = [
                    Spacer(1, 4),
                    Paragraph(day_header_text, self.sub_heading),
                ]
                if day_desc:
                    day_elements.append(Paragraph(day_desc, self.body_style))

                # Slots: morning, afternoon, evening
                slot_rows = []
                for slot_name, slot_label in [
                    ("morning", '<font color="#0284C7">&bull;</font> Morning'),
                    ("afternoon", '<font color="#0284C7">&bull;</font> Afternoon'),
                    ("evening", '<font color="#0284C7">&bull;</font> Evening'),
                    ("night", '<font color="#0284C7">&bull;</font> Night'),
                ]:
                    slot_content = day_info.get(slot_name)
                    if slot_content:
                        if isinstance(slot_content, dict):
                            act_title = sanitize_pdf_text(slot_content.get("activity") or slot_content.get("title") or "")
                            act_desc = sanitize_pdf_text(slot_content.get("description") or "")
                            act_loc = sanitize_pdf_text(slot_content.get("location") or "")
                            act_time = slot_content.get("time") or ""

                            details = f"<b>{act_title}</b>"
                            if act_time:
                                details = f"[{act_time}] " + details
                            if act_loc:
                                details += f" • <i>{act_loc}</i>"
                            if act_desc:
                                details += f"<br/>{act_desc}"
                            slot_rows.append([
                                Paragraph(f"<b>{slot_label}</b>", self.body_bold),
                                Paragraph(details, self.body_style),
                            ])
                        elif isinstance(slot_content, str):
                            slot_rows.append([
                                Paragraph(f"<b>{slot_label}</b>", self.body_bold),
                                Paragraph(sanitize_pdf_text(slot_content), self.body_style),
                            ])

                # Generic activities list fallback
                activities = day_info.get("activities", [])
                if not slot_rows and activities:
                    for a_idx, act in enumerate(activities, start=1):
                        act_text = act if isinstance(act, str) else act.get("activity", str(act))
                        slot_rows.append([
                            Paragraph(f'<b><font color="#0284C7">&bull;</font> Activity {a_idx}</b>', self.body_bold),
                            Paragraph(sanitize_pdf_text(act_text), self.body_style),
                        ])

                if slot_rows:
                    slot_table = Table(slot_rows, colWidths=[90, 414])
                    slot_table.setStyle(
                        TableStyle([
                            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
                            ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#F1F5F9")),
                            ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ])
                    )
                    day_elements.append(slot_table)

                story.append(KeepTogether(day_elements))
                story.append(Spacer(1, 6))
        else:
            # Fallback if itinerary list empty
            story.append(
                Paragraph(
                    f"Day-by-day sightseeing highlights across {destination} with paced morning, afternoon, and evening exploration.",
                    self.body_style,
                )
            )

        story.append(Spacer(1, 10))

        # ----------------------------------------------------
        # SECTION 2: STAYS & FOOD (ACCOMMODATIONS & DINING)
        # ----------------------------------------------------
        story.append(HRFlowable(width="100%", thickness=1, color=self.PRIMARY_COLOR, spaceAfter=8))
        story.append(Paragraph("2. Stays & Regional Dining", self.section_heading))

        hotels = trip.get("recommended_hotels", [])
        restaurants = trip.get("recommended_restaurants", [])
        cuisines = trip.get("local_cuisines", [])
        beverages = trip.get("beverages_to_try", [])

        stays_table_data = []

        if hotels:
            stays_table_data.append([
                Paragraph("<b>Recommended Stays</b>", self.body_bold),
                Paragraph("<br/>".join([f"• {h}" for h in hotels[:4]]), self.body_style),
            ])
        if restaurants:
            stays_table_data.append([
                Paragraph("<b>Regional Dining & Eateries</b>", self.body_bold),
                Paragraph("<br/>".join([f"• {r}" for r in restaurants[:4]]), self.body_style),
            ])
        if cuisines:
            stays_table_data.append([
                Paragraph("<b>Must-Try Cuisines</b>", self.body_bold),
                Paragraph(", ".join(cuisines[:8]), self.body_style),
            ])
        if beverages:
            stays_table_data.append([
                Paragraph("<b>Signature Beverages</b>", self.body_bold),
                Paragraph(", ".join(beverages[:6]), self.body_style),
            ])

        if stays_table_data:
            stays_table = Table(stays_table_data, colWidths=[130, 374])
            stays_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), self.BG_LIGHT),
                    ("BOX", (0, 0), (-1, -1), 0.5, self.BORDER_LIGHT),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, self.BORDER_LIGHT),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ])
            )
            story.append(KeepTogether(stays_table))

        story.append(Spacer(1, 10))

        # ----------------------------------------------------
        # SECTION 3: COST BREAKDOWN & RENTAL VEHICLE PRICING
        # ----------------------------------------------------
        story.append(HRFlowable(width="100%", thickness=1, color=self.PRIMARY_COLOR, spaceAfter=8))
        story.append(Paragraph("3. Cost Breakdown & Transportation Rental Intelligence", self.section_heading))

        est_total = float(trip.get("estimated_trip_cost") or trip.get("budget") or 0)
        acc_cost = float(trip.get("accommodation_cost") or (est_total * 0.40))
        food_cost = float(trip.get("food_cost") or (est_total * 0.25))
        trans_cost = float(trip.get("transportation_cost") or (est_total * 0.20))
        misc_cost = float(trip.get("miscellaneous_cost") or (est_total - (acc_cost + food_cost + trans_cost)))

        cost_rows = [
            [Paragraph("<b>Expense Category</b>", self.body_bold), Paragraph("<b>Estimated Allocation</b>", self.body_bold), Paragraph("<b>Percentage</b>", self.body_bold)],
            [Paragraph("Accommodations & Stays", self.body_style), Paragraph(f"₹{int(acc_cost):,}", self.body_style), Paragraph(f"{round((acc_cost/est_total)*100 if est_total else 40)}%", self.body_style)],
            [Paragraph("Food & Regional Dining", self.body_style), Paragraph(f"₹{int(food_cost):,}", self.body_style), Paragraph(f"{round((food_cost/est_total)*100 if est_total else 25)}%", self.body_style)],
            [Paragraph("Transportation & Local Mobility", self.body_style), Paragraph(f"₹{int(trans_cost):,}", self.body_style), Paragraph(f"{round((trans_cost/est_total)*100 if est_total else 20)}%", self.body_style)],
            [Paragraph("Sightseeing, Activities & Misc", self.body_style), Paragraph(f"₹{int(misc_cost):,}", self.body_style), Paragraph(f"{round((misc_cost/est_total)*100 if est_total else 15)}%", self.body_style)],
            [Paragraph("<b>Total Estimated Budget</b>", self.body_bold), Paragraph(f"<b>₹{int(est_total):,}</b>", self.body_bold), Paragraph("<b>100%</b>", self.body_bold)],
        ]

        cost_table = Table(cost_rows, colWidths=[240, 140, 124])
        cost_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
                ("BOX", (0, 0), (-1, -1), 0.5, self.BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, self.BORDER_LIGHT),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(cost_table)

        # Rental Vehicle Callout Card
        rental_details = trip.get("rental_details")
        trans_mode = trip.get("transportation_mode") or ""

        if rental_details and rental_details.get("is_rental"):
            story.append(Spacer(1, 6))
            rental_callout_data = [
                [
                    Paragraph("<b>Rental Vehicle Rate Intelligence</b>", self.body_bold),
                    Paragraph(
                        f"<b>{rental_details.get('vehicle_type')}</b> ({rental_details.get('example_models')})<br/>"
                        f"• <b>Base Rental:</b> ~₹{rental_details.get('daily_rate'):,}/day × {rental_details.get('rental_days')} days = "
                        f"<b>₹{rental_details.get('total_rental_cost'):,}</b><br/>"
                        f"• <b>Estimated Fuel & Tolls:</b> ~₹{rental_details.get('estimated_fuel_cost'):,} ({rental_details.get('fuel_type')})<br/>"
                        f"• <b>Security Deposit:</b> {rental_details.get('security_deposit')}<br/>"
                        f"• <b>Suitability:</b> {rental_details.get('suitability')}",
                        self.body_style,
                    ),
                ]
            ]
            rental_table = Table(rental_callout_data, colWidths=[150, 354])
            rental_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
                    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#86EFAC")),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ])
            )
            story.append(KeepTogether(rental_table))

        story.append(Spacer(1, 10))

        # ----------------------------------------------------
        # SECTION 4: WEATHER & PACKING INTELLIGENCE
        # ----------------------------------------------------
        story.append(HRFlowable(width="100%", thickness=1, color=self.PRIMARY_COLOR, spaceAfter=8))
        story.append(Paragraph("4. Weather & Packing Intelligence", self.section_heading))

        weather = trip.get("weather_summary") or {}
        temp = weather.get("temperature_celsius") or weather.get("temp_c")
        cond = weather.get("condition") or "Pleasant"
        advisory = weather.get("advisory") or f"Expected pleasant conditions in {destination}. Layer appropriately."

        temp_str = f"{temp}°C" if temp is not None else "Pleasant / Moderate"
        weather_p = Paragraph(
            f"<b>Destination Climate:</b> {temp_str} • {cond}<br/><b>Advisory:</b> {advisory}",
            self.body_style,
        )

        packing = trip.get("packing_checklist") or []
        packing_items = packing[:12] if packing else [
            "Government photo ID & booking vouchers",
            "Breathable cottons and evening light layer",
            "Comfortable all-terrain walking shoes",
            "Universal charging cable & power bank",
            "Personal toiletries & essential medications",
            "Eco-friendly refillable water bottle",
        ]
        packing_p = Paragraph(
            "<b>Recommended Packing Items:</b><br/>"
            + "<br/>".join([f"• {item}" for item in packing_items]),
            self.body_style,
        )

        wp_table = Table(
            [[Paragraph("<b>Live Weather Snapshot</b>", self.body_bold), weather_p],
             [Paragraph("<b>Trip Packing Checklist</b>", self.body_bold), packing_p]],
            colWidths=[130, 374],
        )
        wp_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), self.BG_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, self.BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, self.BORDER_LIGHT),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        story.append(KeepTogether(wp_table))

        story.append(Spacer(1, 10))

        # ----------------------------------------------------
        # SECTION 5: ECO & SUSTAINABILITY REPORT
        # ----------------------------------------------------
        story.append(HRFlowable(width="100%", thickness=1, color=self.PRIMARY_COLOR, spaceAfter=8))
        story.append(Paragraph("5. Eco & Sustainability Report", self.section_heading))

        eco_score = trip.get("sustainability_score", 88)
        carbon = trip.get("carbon_footprint_estimate", 18)
        eco_recs = trip.get("eco_friendly_recommendations") or [
            "Opt for walking or shared mobility when traversing local bazaars and heritage routes.",
            "Choose locally owned homestays and community eateries to support regional livelihoods.",
            "Avoid single-use plastics by carrying reusable bottles and cloth tote bags.",
            "Respect sacred monuments and pristine beach/mountain ecosystems by leaving zero litter.",
        ]

        eco_rows = [
            [
                Paragraph("<b>Sustainability Score</b>", self.body_bold),
                Paragraph(f"<b>{eco_score}/100</b> — Eco Sentinel Verified", self.body_style),
            ],
            [
                Paragraph("<b>Estimated Carbon Footprint</b>", self.body_bold),
                Paragraph(f"<b>{carbon} kg CO₂</b> (Low impact travel trajectory)", self.body_style),
            ],
            [
                Paragraph("<b>Green Travel Best Practices</b>", self.body_bold),
                Paragraph("<br/>".join([f"• {rec}" for rec in eco_recs[:4]]), self.body_style),
            ],
        ]

        eco_table = Table(eco_rows, colWidths=[140, 364])
        eco_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#86EFAC")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBF7D0")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        story.append(KeepTogether(eco_table))

        # Build document with custom numbered canvas
        doc.build(story, canvasmaker=NumberedCanvas)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()


_pdf_generator_instance = TripPDFGenerator()


def get_pdf_generator() -> TripPDFGenerator:
    return _pdf_generator_instance


def compute_pdf_filename(user_name: str | None, destination: str | None) -> str:
    """
    Computes a personalized clean filename e.g. "deva_munnar.pdf"
    Takes first 4 letters of the user's name + "_" + destination.
    """
    import re

    raw_user = (user_name or "trip").strip()
    clean_user = re.sub(r"[^a-zA-Z0-9]", "", raw_user).lower()
    user_prefix = clean_user[:4] if len(clean_user) >= 4 else clean_user.ljust(4, "x")
    if not user_prefix:
        user_prefix = "trip"

    raw_dest = (destination or "itinerary").strip()
    clean_dest = re.sub(r"[^a-zA-Z0-9]", "", raw_dest).lower()
    if not clean_dest:
        clean_dest = "travel"

    return f"{user_prefix}_{clean_dest}.pdf"

