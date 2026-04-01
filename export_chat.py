"""
export_chat.py — Chat Export Module
=====================================
Export conversations as:
- Plain text (.txt) — simple, always works
- PDF (.pdf)        — uses fpdf2 for a formatted document
"""

import io
from datetime import datetime


def export_as_text(messages, user_profile=None):
    """Export conversation as a plain text string.

    Args:
        messages: list of {role, content} dicts
        user_profile: optional user profile dict

    Returns:
        str — the full text content
    """
    lines = []
    lines.append("=" * 60)
    lines.append("  CHATBOT WITH MEMORY — Conversation Export")
    lines.append(f"  Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)

    if user_profile:
        lines.append("")
        lines.append("USER PROFILE:")
        if user_profile.get("name"):
            lines.append(f"  Name: {user_profile['name']}")
        if user_profile.get("interests"):
            lines.append(f"  Interests: {', '.join(user_profile['interests'])}")
        if user_profile.get("goals"):
            lines.append(f"  Goals: {', '.join(user_profile['goals'])}")

    lines.append("")
    lines.append("CONVERSATION:")
    lines.append("-" * 60)

    for msg in messages:
        role = "You" if msg["role"] == "user" else "AI"
        lines.append(f"\n[{role}]")
        lines.append(msg["content"])

    lines.append("")
    lines.append("-" * 60)
    lines.append("End of conversation")

    return "\n".join(lines)


def export_as_pdf(messages, user_profile=None):
    """Export conversation as a PDF using fpdf2.

    Args:
        messages: list of {role, content} dicts
        user_profile: optional user profile dict

    Returns:
        bytes — the PDF file content
    """
    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # --- Header ---
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(108, 99, 255)  # Purple
        pdf.cell(0, 12, "Chatbot with Memory", ln=True, align="C")

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(130, 130, 130)
        pdf.cell(0, 6, f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                 ln=True, align="C")
        pdf.ln(8)

        # --- User Profile ---
        if user_profile:
            has_any = (
                user_profile.get("name")
                or user_profile.get("interests")
                or user_profile.get("goals")
            )
            if has_any:
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_text_color(50, 50, 50)
                pdf.cell(0, 8, "User Profile", ln=True)
                pdf.set_draw_color(108, 99, 255)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(3)

                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(60, 60, 60)

                if user_profile.get("name"):
                    pdf.cell(0, 6, f"Name: {user_profile['name']}", ln=True)
                if user_profile.get("interests"):
                    pdf.cell(0, 6,
                             f"Interests: {', '.join(user_profile['interests'])}",
                             ln=True)
                if user_profile.get("goals"):
                    pdf.cell(0, 6,
                             f"Goals: {', '.join(user_profile['goals'])}", ln=True)
                pdf.ln(6)

        # --- Conversation ---
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, "Conversation", ln=True)
        pdf.set_draw_color(108, 99, 255)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        for msg in messages:
            is_user = msg["role"] == "user"

            # Role label
            pdf.set_font("Helvetica", "B", 10)
            if is_user:
                pdf.set_text_color(0, 120, 180)
                pdf.cell(0, 6, "You:", ln=True)
            else:
                pdf.set_text_color(108, 99, 255)
                pdf.cell(0, 6, "Anti-Gravity AI:", ln=True)

            # Message text — clean up markdown symbols for PDF
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(40, 40, 40)
            text = msg["content"]
            # Strip basic markdown
            for sym in ["**", "*", "##", "#", "```"]:
                text = text.replace(sym, "")
            pdf.multi_cell(0, 5, text.strip())
            pdf.ln(4)

        return bytes(pdf.output())

    except ImportError:
        # Fall back to text if fpdf2 not installed
        return export_as_text(messages, user_profile).encode("utf-8")
