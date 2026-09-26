import os
import subprocess
import markdown

def generate():
    with open("PROJECT_REPORT.md", "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc"]
    )

    styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Content Creation and Analysis System - Project Report</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap');

@page {{
    size: A4;
    margin: 20mm 18mm 20mm 18mm;
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #1e293b;
    line-height: 1.65;
    font-size: 11pt;
    max-width: 860px;
    margin: 0 auto;
    padding: 30px 20px;
}}

h1, h2, h3, h4 {{
    font-family: 'Space Grotesk', sans-serif;
    color: #0f172a;
    font-weight: 700;
    margin-top: 1.6em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}}

h1 {{
    font-size: 24pt;
    border-bottom: 3px solid #6366f1;
    padding-bottom: 8px;
    margin-top: 0;
    color: #1e1b4b;
}}

h2 {{
    font-size: 15pt;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
    color: #312e81;
}}

h3 {{
    font-size: 12pt;
    color: #4338ca;
}}

p, li {{
    color: #334155;
    font-size: 10.5pt;
}}

ul, ol {{
    padding-left: 24px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}}

th, td {{
    padding: 9px 12px;
    text-align: left;
    border: 1px solid #cbd5e1;
}}

th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
}}

tr:nth-child(even) {{
    background-color: #f8fafc;
}}

code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}}

pre {{
    background-color: #0f172a;
    color: #f8fafc;
    padding: 14px 18px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.45;
    page-break-inside: avoid;
}}

pre code {{
    background: transparent;
    color: inherit;
    border: none;
    padding: 0;
}}

blockquote {{
    border-left: 4px solid #6366f1;
    padding-left: 14px;
    margin: 16px 0;
    color: #475569;
    background: #f8fafc;
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
}}

a {{
    color: #4f46e5;
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

hr {{
    border: 0;
    border-top: 1px solid #e2e8f0;
    margin: 28px 0;
}}

.badge {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 8.5pt;
    font-weight: 600;
}}

@media print {{
    body {{
        padding: 0;
        font-size: 10pt;
    }}
    pre {{
        white-space: pre-wrap;
        word-break: break-all;
    }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    # Write HTML files
    html_path_proj = "PROJECT_REPORT.html"
    html_path_down = "/Users/vismayjain/Downloads/PROJECT_REPORT.html"
    
    with open(html_path_proj, "w", encoding="utf-8") as f:
        f.write(styled_html)
    with open(html_path_down, "w", encoding="utf-8") as f:
        f.write(styled_html)
        
    print(f"Generated {html_path_proj} and {html_path_down}")

    # Generate PDF via Headless Chrome
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    pdf_path_proj = os.path.abspath("PROJECT_REPORT.pdf")
    pdf_path_down = "/Users/vismayjain/Downloads/AI_Content_Creation_Project_Report.pdf"

    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path_proj}",
        os.path.abspath(html_path_proj)
    ]
    subprocess.run(cmd, check=True)

    # Copy to Downloads
    import shutil
    shutil.copyfile(pdf_path_proj, pdf_path_down)
    print(f"Successfully generated PDF at {pdf_path_proj} and {pdf_path_down}")

if __name__ == "__main__":
    generate()
