#!/usr/bin/env python3
def create_info_card(output_path: str = "../info-card.svg") -> None:
    INFO_ROWS = {
        "OS": "Linux (Ubuntu)",
        "Editor": "VS Code",
        "Language": "Python, JavaScript",
        "Specialization": "IoT, Cybersecurity, Blockchain",
        "Focus": "SOC Analyst & Full-Stack Dev",
        "Company": "ABS Technologies",
    }
    
    card_width = 480
    card_height = 220
    padding = 20
    row_height = 30
    
    svg_lines = [
        f'<svg width="{card_width}" height="{card_height}" xmlns="http://www.w3.org/2000/svg">',
        '<defs><style>',
        '.title { font-family: monospace; font-size: 14px; font-weight: bold; fill: #26a641; }',
        '.label { font-family: monospace; font-size: 12px; fill: #0e4429; font-weight: bold; }',
        '.value { font-family: monospace; font-size: 12px; fill: #0e4429; }',
        '.card-bg { fill: #f0f6fc; stroke: #30363d; stroke-width: 1; }',
        '@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }',
        '.info-item { animation: fadeIn 0.6s ease-in forwards; }',
        '</style></defs>',
        f'<rect class="card-bg" width="{card_width}" height="{card_height}" rx="5"/>',
    ]
    
    svg_lines.append(f'<text class="title" x="{padding}" y="{padding + 15}">shreyas@profile</text>')
    
    y_offset = padding + 45
    for idx, (key, value) in enumerate(INFO_ROWS.items()):
        delay = (idx + 1) * 0.1
        svg_lines.append(f'<g class="info-item" style="animation-delay: {delay}s;">')
        svg_lines.append(f'<text class="label" x="{padding}" y="{y_offset}">{key}:</text>')
        svg_lines.append(f'<text class="value" x="{padding + 120}" y="{y_offset}">{value}</text>')
        svg_lines.append('</g>')
        y_offset += row_height
    
    svg_lines.append('</svg>')
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_lines))
    print(f"✅ Info card saved")

if __name__ == "__main__":
    create_info_card()
