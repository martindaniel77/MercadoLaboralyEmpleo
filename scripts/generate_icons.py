import os
import math
import struct
import zlib
import sys

def create_png_rgba(width, height, get_pixel):
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # Filter 0
        for x in range(width):
            r, g, b, a = get_pixel(x, y)
            raw_data.extend([int(max(0, min(255, round(r)))),
                             int(max(0, min(255, round(g)))),
                             int(max(0, min(255, round(b)))),
                             int(max(0, min(255, round(a))))])
    
    compressed = zlib.compress(bytes(raw_data), level=6)
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    png.extend(struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc))
    
    idat_crc = zlib.crc32(b'IDAT' + compressed)
    png.extend(struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc))
    
    iend_crc = zlib.crc32(b'IEND')
    png.extend(struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc))
    
    return bytes(png)

def create_ico(png_bytes_list):
    count = len(png_bytes_list)
    header = struct.pack('<HHH', 0, 1, count)
    offset = 6 + (16 * count)
    dir_entries = []
    image_data = []
    
    for w, h, data in png_bytes_list:
        w_byte = 0 if w >= 256 else w
        h_byte = 0 if h >= 256 else h
        size = len(data)
        entry = struct.pack('<BBBBHHII', w_byte, h_byte, 0, 0, 1, 32, size, offset)
        dir_entries.append(entry)
        image_data.append(data)
        offset += size
        
    return header + b''.join(dir_entries) + b''.join(image_data)

def point_in_poly(px, py, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if py > min(p1y, p2y):
            if py <= max(p1y, p2y):
                if px <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or px <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# M and L precise polygon coordinates (64x64 design space)
M_POLY = [
    (11.0, 18.0), (17.5, 18.0), (22.0, 29.0), (26.5, 18.0), (33.0, 18.0), 
    (33.0, 46.0), (27.5, 46.0), (27.5, 27.0), (23.5, 36.5), (20.5, 36.5), 
    (16.5, 27.0), (16.5, 46.0), (11.0, 46.0)
]

L_POLY = [
    (36.5, 18.0), (42.5, 18.0), (42.5, 40.5), (53.0, 40.5), 
    (53.0, 46.0), (36.5, 46.0)
]

def sample_point(u, v):
    px = u * 64.0
    py = v * 64.0
    
    # 1. Rounded rectangle background: center (32, 32), size 56x56, r=14
    dx = max(0.0, abs(px - 32.0) - 14.0)
    dy = max(0.0, abs(py - 32.0) - 14.0)
    dist_outside = math.sqrt(dx*dx + dy*dy) - 14.0
    
    if dist_outside > 0:
        return (0, 0, 0, 0)
        
    # Gold Gradient: Top-left #FCE280 -> Mid #EDBD4C -> Bot #B67F16
    t = (u + v) * 0.5
    c_top = (252, 226, 128)
    c_mid = (237, 189, 76)
    c_bot = (182, 127, 22)
    
    if t < 0.45:
        sub_t = t / 0.45
        r = c_top[0] * (1 - sub_t) + c_mid[0] * sub_t
        g = c_top[1] * (1 - sub_t) + c_mid[1] * sub_t
        b = c_top[2] * (1 - sub_t) + c_mid[2] * sub_t
    else:
        sub_t = (t - 0.45) / 0.55
        r = c_mid[0] * (1 - sub_t) + c_bot[0] * sub_t
        g = c_mid[1] * (1 - sub_t) + c_bot[1] * sub_t
        b = c_mid[2] * (1 - sub_t) + c_bot[2] * sub_t
        
    # Inner border bevel highlight
    if dist_outside > -2.0:
        bevel = (1.2 - u - v) * 35.0
        r = min(255, max(0, r + bevel))
        g = min(255, max(0, g + bevel))
        b = min(255, max(0, b + bevel))

    # 2. Data analytics vertical accent bars in background
    bar_dark = (29, 23, 12)
    bar_alpha = 0.16
    if (41.0 <= px <= 44.5 and 35.0 <= py <= 46.0) or \
       (46.5 <= px <= 50.0 and 27.0 <= py <= 46.0) or \
       (52.0 <= px <= 55.5 and 19.0 <= py <= 46.0):
        r = r * (1 - bar_alpha) + bar_dark[0] * bar_alpha
        g = g * (1 - bar_alpha) + bar_dark[1] * bar_alpha
        b = b * (1 - bar_alpha) + bar_dark[2] * bar_alpha

    # 3. Data node indicator
    node_dist = math.sqrt((px - 50.5)**2 + (py - 14.5)**2)
    if node_dist <= 3.8:
        r, g, b = 29, 23, 12
        if node_dist <= 1.6:
            r, g, b = 252, 226, 128

    # 4. Text "M" and "L"
    if point_in_poly(px, py, M_POLY) or point_in_poly(px, py, L_POLY):
        r, g, b = 29, 23, 12

    return (r, g, b, 255)

def render_pixel(x, y, size):
    if size <= 48:
        # 2x2 grid for anti-aliasing on small sizes (4 samples)
        samples = [0.25, 0.75]
        total_r, total_g, total_b, total_a = 0.0, 0.0, 0.0, 0.0
        for sy in samples:
            for sx in samples:
                u = (x + sx) / size
                v = (y + sy) / size
                sr, sg, sb, sa = sample_point(u, v)
                total_r += sr * (sa / 255.0)
                total_g += sg * (sa / 255.0)
                total_b += sb * (sa / 255.0)
                total_a += sa
        num_samples = 4.0
        avg_a = total_a / num_samples
        if avg_a <= 0.5:
            return (0, 0, 0, 0)
        avg_r = (total_r / num_samples) / (avg_a / 255.0)
        avg_g = (total_g / num_samples) / (avg_a / 255.0)
        avg_b = (total_b / num_samples) / (avg_a / 255.0)
        return (avg_r, avg_g, avg_b, avg_a)
    else:
        # 1 sample for larger resolutions
        u = (x + 0.5) / size
        v = (y + 0.5) / size
        return sample_point(u, v)

SVG_CONTENT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <!-- Gradient for Squircle Badge -->
    <linearGradient id="mlGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FCE280" />
      <stop offset="45%" stop-color="#EDBD4C" />
      <stop offset="100%" stop-color="#B67F16" />
    </linearGradient>
    
    <!-- Border Gradient -->
    <linearGradient id="mlBorderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF8E0" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#7C5209" stop-opacity="0.75" />
    </linearGradient>
    
    <!-- Subtle Drop Shadow -->
    <filter id="mlShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#1D170C" flood-opacity="0.35" />
    </filter>
  </defs>

  <!-- Squircle Base -->
  <rect x="4" y="4" width="56" height="56" rx="14" ry="14" fill="url(#mlGoldGrad)" stroke="url(#mlBorderGrad)" stroke-width="1.5" filter="url(#mlShadow)" />

  <!-- Data mining analytics bars (subtle background motif) -->
  <rect x="41" y="35" width="3.5" height="11" rx="1.5" fill="#1D170C" opacity="0.16" />
  <rect x="46.5" y="27" width="3.5" height="19" rx="1.5" fill="#1D170C" opacity="0.16" />
  <rect x="52" y="19" width="3.5" height="27" rx="1.5" fill="#1D170C" opacity="0.16" />

  <!-- Data node indicator -->
  <circle cx="50.5" cy="14.5" r="3.8" fill="#1D170C" />
  <circle cx="50.5" cy="14.5" r="1.6" fill="#FCE280" />
  <line x1="43" y1="18.5" x2="50.5" y2="14.5" stroke="#1D170C" stroke-width="1.2" stroke-dasharray="1.5 1.5" opacity="0.5" />

  <!-- Monospace 'M' Vector Path -->
  <path d="M 11 18 L 17.5 18 L 22 29 L 26.5 18 L 33 18 L 33 46 L 27.5 46 L 27.5 27 L 23.5 36.5 L 20.5 36.5 L 16.5 27 L 16.5 46 L 11 46 Z" fill="#1D170C" />

  <!-- Monospace 'L' Vector Path -->
  <path d="M 36.5 18 L 42.5 18 L 42.5 40.5 L 53 40.5 L 53 46 L 36.5 46 Z" fill="#1D170C" />
</svg>
'''

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_dir = os.path.join(base_dir, "static", "img")
    os.makedirs(img_dir, exist_ok=True)
    
    # 1. Write SVG
    svg_path = os.path.join(img_dir, "favicon.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(SVG_CONTENT)
    print(f"[OK] {svg_path}", flush=True)
    
    # 2. Generate PNGs of various sizes
    sizes = [16, 32, 48, 180, 192, 512]
    png_buffers = {}
    
    for s in sizes:
        png_data = create_png_rgba(s, s, lambda x, y, size=s: render_pixel(x, y, size))
        png_buffers[s] = png_data
        
        filename = f"favicon-{s}x{s}.png" if s in [16, 32] else (
            "apple-touch-icon.png" if s == 180 else (
                f"android-chrome-{s}x{s}.png" if s in [192, 512] else f"favicon-{s}.png"
            )
        )
        file_path = os.path.join(img_dir, filename)
        with open(file_path, "wb") as f:
            f.write(png_data)
        print(f"[OK] {file_path}", flush=True)

    # 3. Create multi-resolution .ico (16x16, 32x32, 48x48)
    ico_data = create_ico([
        (16, 16, png_buffers[16]),
        (32, 32, png_buffers[32]),
        (48, 48, png_buffers[48])
    ])
    
    ico_img_path = os.path.join(img_dir, "favicon.ico")
    with open(ico_img_path, "wb") as f:
        f.write(ico_data)
    print(f"[OK] {ico_img_path}", flush=True)
    
    ico_static_path = os.path.join(base_dir, "static", "favicon.ico")
    with open(ico_static_path, "wb") as f:
        f.write(ico_data)
    print(f"[OK] {ico_static_path}", flush=True)

    manifest_content = '''{
  "name": "Mercado Laboral y Empleo | Minería de Datos",
  "short_name": "MercadoLaboral",
  "icons": [
    {
      "src": "/static/img/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/img/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#1D170C",
  "background_color": "#FAF6EA",
  "display": "standalone"
}'''
    manifest_path = os.path.join(base_dir, "static", "site.webmanifest")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print(f"[OK] {manifest_path}", flush=True)
    print("All favicon assets successfully generated!", flush=True)

if __name__ == '__main__':
    main()
