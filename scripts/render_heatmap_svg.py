#!/usr/bin/env python3
"""Render contribution heatmap SVG"""
import json
import os

COLORS = {
    0: "#ebedf0",
    1: "#c6e48b",
    2: "#7bc96f",
    3: "#239a3b",
    4: "#108548",
    5: "#0a3d1a",
}

CELL_SIZE = 13
PADDING = 40
GAP = 2

def render_heatmap(data: dict, output_path: str = "../contrib-heatmap.svg") -> None:
    grid = data.get("grid", [])
    print(f"📊 Rendering {len(grid)} cells")
    
    while len(grid) < 371:
        grid.append({"level": 0, "count": 0})
    grid = grid[:371]
    
    level_counts = {i: 0 for i in range(6)}
    for cell in grid:
        level = min(cell.get("level", 0), 5)
        level_counts[level] += 1
    
    print(f"Level distribution: {level_counts}")
    
    weeks = 53
    days = 7
    width = PADDING * 2 + weeks * (CELL_SIZE + GAP)
    height = PADDING * 2 + days * (CELL_SIZE + GAP)
    
    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '<defs><style>',
        '@keyframes revealDiag { 0% { clip-path: polygon(0 0, 0 0, 0 100%); } 100% { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); } }',
        '.heatmap { animation: revealDiag 2s ease-out forwards; }',
        '.cell { stroke: #e0e0e0; stroke-width: 1; }',
        '</style></defs>',
        '<g class="heatmap">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
    ]
    
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, month in enumerate(month_labels):
        x = PADDING + (i * 4 + 1) * (CELL_SIZE + GAP)
        svg_lines.append(f'<text x="{x}" y="{PADDING - 10}" font-size="11" fill="#666">{month}</text>')
    
    day_labels = ["Mon", "Wed", "Fri", "Sun"]
    for i, day in enumerate(day_labels):
        idx = i * 2
        y = PADDING + (idx + 1) * (CELL_SIZE + GAP) + CELL_SIZE // 2
        svg_lines.append(f'<text x="{PADDING - 30}" y="{y}" font-size="11" fill="#666">{day}</text>')
    
    green_count = 0
    for idx, cell_data in enumerate(grid):
        week = idx // days
        day = idx % days
        x = PADDING + week * (CELL_SIZE + GAP)
        y = PADDING + day * (CELL_SIZE + GAP)
        level = min(cell_data.get("level", 0), 5)
        color = COLORS.get(level, COLORS[0])
        svg_lines.append(f'<rect class="cell" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{color}"/>')
        if level > 0:
            green_count += 1
    
    svg_lines.append('</g>')
    stats_y = height - 20
    svg_lines.append(f'<text x="{PADDING}" y="{stats_y}" font-size="12" fill="#666">{green_count} active days | Total: {data.get("total", 0)}</text>')
    svg_lines.append('</svg>')
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_lines))
    print(f"✅ Heatmap saved with {green_count} green cells")

if __name__ == "__main__":
    json_file = "../data/contributions.json"
    if not os.path.exists(json_file):
        print(f"❌ {json_file} not found")
        exit(1)
    with open(json_file, 'r') as f:
        data = json.load(f)
    render_heatmap(data)
