"""Generate placeholder icons (192, 512) for Daggerheart Roller.

Pure stdlib PNG writer. Design: warm-dark background with a centered circle
split vertically — gold (Hope) on the left, silver (Fear) on the right.
4x supersampling gives clean edges.
"""
import os, struct, zlib

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BG     = (26, 20, 16)
GOLD   = (212, 161, 74)
SILVER = (168, 176, 184)


def png_bytes(width, height, rgb):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    stride = width * 3
    raw = b''.join(b'\x00' + rgb[y*stride:(y+1)*stride] for y in range(height))
    idat = zlib.compress(raw, 9)
    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')


def make(size):
    cx = cy = size / 2.0
    # Maskable safe zone: keep content within ~40% radius (covers 80% center)
    r_outer = size * 0.40
    r_outer2 = r_outer * r_outer
    # Subtle inner shading via a slightly smaller "rim"
    r_inner = size * 0.36
    r_inner2 = r_inner * r_inner

    # Sub-sample offsets (4x supersampling)
    offsets = [(0.125, 0.125), (0.375, 0.125), (0.625, 0.125), (0.875, 0.125),
               (0.125, 0.375), (0.375, 0.375), (0.625, 0.375), (0.875, 0.375),
               (0.125, 0.625), (0.375, 0.625), (0.625, 0.625), (0.875, 0.625),
               (0.125, 0.875), (0.375, 0.875), (0.625, 0.875), (0.875, 0.875)]
    n_samples = len(offsets)

    def blend(a, b, t):
        return (int(a[0]*(1-t) + b[0]*t),
                int(a[1]*(1-t) + b[1]*t),
                int(a[2]*(1-t) + b[2]*t))

    pixels = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            # Decide fill side: pixel center vs vertical split
            fill = GOLD if (x + 0.5) < cx else SILVER

            in_count = 0
            rim_count = 0
            for sx, sy in offsets:
                dx = (x + sx) - cx
                dy = (y + sy) - cy
                d2 = dx*dx + dy*dy
                if d2 <= r_outer2:
                    in_count += 1
                    if d2 > r_inner2:
                        rim_count += 1

            if in_count == 0:
                c = BG
            elif in_count == n_samples:
                c = fill
            else:
                c = blend(BG, fill, in_count / n_samples)

            # Slight darken at the rim for depth
            if in_count > 0 and rim_count > 0:
                rim_t = rim_count / n_samples * 0.35
                c = blend(c, BG, rim_t)

            off = (y * size + x) * 3
            pixels[off]   = c[0]
            pixels[off+1] = c[1]
            pixels[off+2] = c[2]

    return png_bytes(size, size, bytes(pixels))


for s in (192, 512):
    path = os.path.join(OUT_DIR, f'icon-{s}.png')
    with open(path, 'wb') as f:
        f.write(make(s))
    print(path)
