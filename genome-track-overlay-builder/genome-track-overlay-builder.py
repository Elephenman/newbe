#!/usr/bin/env python3
"""基因组多轨道叠加配置生成"""

# 基因组多轨道叠加配置
import json

print("=" * 60)
print("  🎨 基因组多轨道叠加配置器")
print("=" * 60)

tracks_config = get_input("轨道配置文件路径", "tracks.json")
genome_ver = get_input("基因组版本", "hg38")
region = get_input("显示区域(chr:start-end)", "chr1:1000000-2000000")
output_file = get_input("叠加配置输出路径", "track_overlay.html")

try:
    with open(tracks_config, "r", encoding="utf-8") as f:
        tracks = json.load(f)
except FileNotFoundError:
    tracks = {
        "tracks": [
            {"name": "Genes", "type": "gene", "file": "genes.bed", "color": "#4C72B0"},
            {"name": "ATAC-seq", "type": "peak", "file": "atac_peaks.bed", "color": "#55A868"},
            {"name": "ChIP-seq", "type": "signal", "file": "chip_signal.bedgraph", "color": "#C44E52"}
        ]
    }

print("✅ 轨道数: " + str(len(tracks.get("tracks", []))))

parts = region.split(":")
chrom = parts[0]
pos_parts = parts[1].split("-")
start = int(pos_parts[0])
end = int(pos_parts[1])

html_parts = []
html_parts.append("<!DOCTYPE html>")
html_parts.append("<html>")
html_parts.append("<head>")
html_parts.append("<title>Genome Track Overlay - " + region + "</title>")
html_parts.append("<style>")
html_parts.append("body { font-family: Arial, sans-serif; margin: 20px; }")
html_parts.append(".track { margin: 5px 0; padding: 10px; border-left: 3px solid; }")
html_parts.append(".track-name { font-weight: bold; font-size: 14px; }")
html_parts.append(".track-info { font-size: 12px; color: #666; }")
html_parts.append(".header { background: #f5f5f5; padding: 15px; border-radius: 5px; }")
html_parts.append("</style>")
html_parts.append("</head>")
html_parts.append("<body>")
html_parts.append('<div class="header">')
html_parts.append("<h2>Genome Track Overlay</h2>")
html_parts.append("<p>Genome: " + genome_ver + " | Region: " + region + " | Size: " + str(end-start) + " bp</p>")
html_parts.append("</div>")

for track in tracks.get("tracks", []):
    color = track.get("color", "#333")
    name = track.get("name", "Unknown")
    ttype = track.get("type", "unknown")
    file = track.get("file", "N/A")
    html_parts.append('<div class="track" style="border-color: ' + color + ';">')
    html_parts.append('<div class="track-name">' + name + '</div>')
    html_parts.append('<div class="track-info">Type: ' + ttype + ' | File: ' + file + ' | Color: ' + color + '</div>')
    html_parts.append("</div>")

html_parts.append("</body></html>")
html_content = "\n".join(html_parts)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("\n✅ 叠加配置已生成")
print("  区域: " + region)
print("  轨道数: " + str(len(tracks.get("tracks", []))))
print("📄 输出: " + output_file)
