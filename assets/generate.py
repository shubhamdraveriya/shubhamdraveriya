#!/usr/bin/env python3
"""Generates the SVG artwork for the GitHub profile README.

Every image is written twice, as <name>-dark.svg and <name>-light.svg, and the
README picks one with <picture> and prefers-color-scheme. The palette follows
the "Die Stack" website (shubhamdraveriya.github.io/website).

    python3 assets/generate.py
"""

from pathlib import Path
from textwrap import wrap

OUT = Path(__file__).resolve().parent

THEMES = {
    "dark": dict(
        bg="#15172b", panel="#1b1c36", die="#1d1235", line="#33355a", grid="#2a2c4d",
        text="#eceaf5", muted="#b4b2cc", faint="#7b7999",
        gold="#e9b949", cyan="#6fe3e1", violet="#9b8cff", pink="#ff7ab6",
    ),
    "light": dict(
        bg="#fbfaf6", panel="#ffffff", die="#f1edff", line="#dcd9e6", grid="#e9e6f0",
        text="#1b1c36", muted="#4a4963", faint="#85839c",
        gold="#a36f00", cyan="#0b7a78", violet="#5a48d6", pink="#c0266c",
    ),
}

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"

STYLE = """
  <style>
    .sans {{ font-family: {sans}; }}
    .mono {{ font-family: {mono}; }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>""".format(sans=SANS, mono=MONO)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, title, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f"  <title>{esc(title)}</title>{STYLE}\n{body}\n</svg>\n"
    )


def frame(w, h, t):
    return (
        f'  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" '
        f'fill="{t["bg"]}" stroke="{t["line"]}"/>'
    )


# --------------------------------------------------------------------------
# Header: name, role, a typed bring-up command and a chip that powers up.
# --------------------------------------------------------------------------

def header(t):
    W, H = 1200, 380
    o = [frame(W, H, t)]
    o.append(
        f'''  <defs>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{t["grid"]}"/>
    </pattern>
    <clipPath id="frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17"/></clipPath>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="{t["bg"]}" stop-opacity="1"/>
      <stop offset="0.45" stop-color="{t["bg"]}" stop-opacity="0.92"/>
      <stop offset="1" stop-color="{t["bg"]}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#dots)"/>'''
    )

    # Chip on the right, with traces running out to the edges of the frame.
    cx, cy = 985, 190
    pk, die = 220, 132
    px, py = cx - pk / 2, cy - pk / 2
    traces = []
    for i, dy in enumerate((-66, -22, 22, 66)):
        y = cy + dy
        traces.append(f"M{px} {y} H{px - 60 - 20 * (i % 2)} V{y + (-24 if dy < 0 else 24)} H690")
        traces.append(f"M{px + pk} {y} H{px + pk + 40 + 18 * (i % 2)} V{y + (-30 if dy < 0 else 30)} H{W}")
    for dx in (-66, -22, 22, 66):
        x = cx + dx
        traces.append(f"M{x} {py} V{py - 26} H{x + (dx // 2)} V0")
        traces.append(f"M{x} {py + pk} V{py + pk + 26} H{x - (dx // 2)} V{H}")
    for d in traces:
        o.append(f'    <path d="{d}" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>')
    colors = [t["cyan"], t["violet"], t["gold"], t["pink"]]
    for i, d in enumerate(traces):
        c = colors[i % 4]
        dur = 3.2 + (i % 5) * 0.55
        o.append(
            f'    <path d="{d}" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" '
            f'stroke-dasharray="14 900" stroke-dashoffset="914">'
            f'<animate attributeName="stroke-dashoffset" values="914;0" dur="{dur:.2f}s" '
            f'begin="{(i * 0.37) % 3:.2f}s" repeatCount="indefinite"/></path>'
        )
    # Fade the left traces out under the text.
    o.append(f'    <rect x="0" y="0" width="760" height="{H}" fill="url(#fade)"/>')

    # Package with pins.
    o.append(
        f'    <rect x="{px}" y="{py}" width="{pk}" height="{pk}" rx="12" fill="{t["panel"]}" '
        f'stroke="{t["line"]}" stroke-width="2"/>'
    )
    for k in range(8):
        off = px + 25 + k * 24
        o.append(f'    <rect x="{off}" y="{py - 7}" width="10" height="7" rx="1.5" fill="{t["faint"]}"/>')
        o.append(f'    <rect x="{off}" y="{py + pk}" width="10" height="7" rx="1.5" fill="{t["faint"]}"/>')
        o.append(f'    <rect x="{px - 7}" y="{off}" width="7" height="10" rx="1.5" fill="{t["faint"]}"/>')
        o.append(f'    <rect x="{px + pk}" y="{off}" width="7" height="10" rx="1.5" fill="{t["faint"]}"/>')
    o.append(f'    <circle cx="{px + 18}" cy="{py + 18}" r="4" fill="{t["faint"]}"/>')

    # Die: a 4x4 grid of blocks that light up in a wave.
    dx0, dy0 = cx - die / 2, cy - die / 2
    o.append(
        f'    <rect x="{dx0}" y="{dy0}" width="{die}" height="{die}" rx="6" fill="{t["die"]}" '
        f'stroke="{t["gold"]}" stroke-width="2"/>'
    )
    cell, gap = 24, 6
    start = dx0 + (die - (4 * cell + 3 * gap)) / 2
    for r in range(4):
        for c in range(4):
            x, y = start + c * (cell + gap), start - dx0 + dy0 + r * (cell + gap)
            col = colors[(r + c) % 4]
            o.append(
                f'    <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{col}" opacity="0.18">'
                f'<animate attributeName="opacity" values="0.18;0.18;0.95;0.35;0.18" '
                f'keyTimes="0;{0.05 + (r + c) * 0.06:.2f};{0.1 + (r + c) * 0.06:.2f};{0.3 + (r + c) * 0.06:.2f};1" '
                f'dur="4s" repeatCount="indefinite"/></rect>'
            )
    o.append(
        f'    <text x="{cx}" y="{py + pk - 14}" text-anchor="middle" class="mono" font-size="11" '
        f'letter-spacing="2" fill="{t["faint"]}">SD-01 · RV32I</text>'
    )
    o.append("  </g>")

    # Text block.
    x = 64
    o.append(
        f'  <text x="{x}" y="98" class="mono" font-size="15" letter-spacing="3" fill="{t["gold"]}">'
        f"RTL · FPGA · RISC-V · SPACE PAYLOADS</text>"
    )
    o.append(
        f'  <text x="{x - 3}" y="172" class="sans" font-size="66" font-weight="800" '
        f'letter-spacing="-1.5" fill="{t["text"]}">Shubham Draveriya</text>'
    )
    o.append(
        f'  <text x="{x}" y="216" class="sans" font-size="23" fill="{t["muted"]}">'
        f"RTL design and embedded systems engineer.</text>"
    )
    o.append(
        f'  <text x="{x}" y="246" class="sans" font-size="23" fill="{t["muted"]}">'
        f"I build hardware that has to work the first time.</text>"
    )

    # Typed command with a cursor that follows it.
    cmd = "$ make bringup && ./verify --bit-exact"
    cw = 10.85  # advance of an 18px monospace glyph
    n = len(cmd)
    steps = [f"{i * cw:.1f}" for i in range(n + 1)]
    hold = 18
    values = ";".join(steps + [steps[-1]] * hold + ["0"])
    total = n + hold + 2
    kt = ";".join(f"{i / total:.4f}" for i in range(total))
    o.append(
        f'''  <defs><clipPath id="typed"><rect x="{x}" y="276" width="0" height="34">
    <animate attributeName="width" values="{values}" keyTimes="{kt}" dur="8s" calcMode="discrete" repeatCount="indefinite"/>
  </rect></clipPath></defs>
  <rect x="{x - 14}" y="270" width="{n * cw + 48}" height="46" rx="10" fill="{t["panel"]}" stroke="{t["line"]}"/>
  <text x="{x}" y="300" class="mono" font-size="18" fill="{t["text"]}" clip-path="url(#typed)">{esc(cmd)}</text>
  <rect x="{x}" y="284" width="10" height="21" fill="{t["cyan"]}">
    <animateTransform attributeName="transform" type="translate" values="{";".join(s + " 0" for s in steps)};{";".join([steps[-1] + " 0"] * hold)};0 0" keyTimes="{kt}" dur="8s" calcMode="discrete" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
  </rect>'''
    )
    t_on = n / total
    o.append(
        f'''  <text x="{x}" y="348" class="mono" font-size="15" fill="{t["cyan"]}" opacity="0">✔ timing met   ✔ 0 errors   ✔ bit-exact
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t_on:.3f};{t_on + 0.03:.3f};0.98;1" dur="8s" repeatCount="indefinite"/>
  </text>'''
    )
    return svg(W, H, "Shubham Draveriya — RTL design and embedded systems engineer", "\n".join(o))


# --------------------------------------------------------------------------
# whoami.vcd: a waveform viewer with the interests on the data bus.
# --------------------------------------------------------------------------

def waveform(t):
    W, H = 1200, 360
    X0, CW, N = 230, 57, 16
    XE = X0 + N * CW
    top, rh = 78, 44
    o = [frame(W, H, t)]
    o.append(f'  <path d="M1 52 H{W - 1}" stroke="{t["line"]}"/>')
    for i, c in enumerate((t["pink"], t["gold"], t["cyan"])):
        o.append(f'  <circle cx="{30 + i * 20}" cy="27" r="6" fill="{c}" opacity="0.85"/>')
    o.append(f'  <text x="104" y="32" class="mono" font-size="15" fill="{t["text"]}">whoami.vcd</text>')
    o.append(
        f'  <text x="{W - 30}" y="32" text-anchor="end" class="mono" font-size="13" fill="{t["faint"]}">'
        f"timescale 1ns/1ps · {N} cycles · 0 errors</text>"
    )
    o.append(f'  <path d="M{X0 - 18} 52 V{H - 1}" stroke="{t["line"]}"/>')
    for k in range(N + 1):
        x = X0 + k * CW
        o.append(f'  <path d="M{x} {top - 8} V{H - 24}" stroke="{t["grid"]}" stroke-dasharray="3 5"/>')

    rows = ["clk", "rst_n", "valid", "ready", "data[31:0]", "stage"]

    def ylo(r):
        return top + r * rh + 30

    def yhi(r):
        return top + r * rh + 8

    for r, name in enumerate(rows):
        o.append(
            f'  <text x="32" y="{ylo(r) - 6}" class="mono" font-size="15" fill="{t["muted"]}">{name}</text>'
        )

    def bits(r, b, color):
        d = f"M{X0} {ylo(r) if not b[0] else yhi(r)}"
        for k, v in enumerate(b):
            x = X0 + k * CW
            y = yhi(r) if v else ylo(r)
            d += f" V{y} H{x + CW}"
        return f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'

    clk = f"M{X0} {ylo(0)}"
    for k in range(N):
        x = X0 + k * CW
        clk += f" V{yhi(0)} H{x + CW / 2} V{ylo(0)} H{x + CW}"
    o.append(f'  <path d="{clk}" fill="none" stroke="{t["cyan"]}" stroke-width="2" stroke-linejoin="round"/>')
    o.append(bits(1, [0, 0] + [1] * 14, t["cyan"]))
    o.append(bits(2, [0, 0] + [1] * 14, t["cyan"]))
    o.append(bits(3, [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], t["cyan"]))

    def bus(r, segs, colors):
        for (s, n, label), c in zip(segs, colors):
            x1, x2 = X0 + s * CW, X0 + (s + n) * CW
            y1, y2, ym = yhi(r), ylo(r), (yhi(r) + ylo(r)) / 2
            d = f"M{x1} {ym} L{x1 + 6} {y1} H{x2 - 6} L{x2} {ym} L{x2 - 6} {y2} H{x1 + 6} Z"
            if label is None:
                o.append(f'  <path d="{d}" fill="{t["faint"]}" fill-opacity="0.12" stroke="{t["faint"]}" stroke-width="1.5"/>')
                o.append(
                    f'  <text x="{(x1 + x2) / 2}" y="{ym + 5}" text-anchor="middle" class="mono" '
                    f'font-size="13" fill="{t["faint"]}">xxxx</text>'
                )
                continue
            o.append(f'  <path d="{d}" fill="{c}" fill-opacity="0.16" stroke="{c}" stroke-width="1.8"/>')
            o.append(
                f'  <text x="{(x1 + x2) / 2}" y="{ym + 5}" text-anchor="middle" class="mono" '
                f'font-size="14" font-weight="700" fill="{c}">{esc(label)}</text>'
            )

    pal = [t["gold"], t["cyan"], t["violet"], t["pink"], t["gold"], t["cyan"], t["violet"]]
    bus(4, [(0, 2, None), (2, 2, "RTL"), (4, 3, "RISC-V"), (7, 2, "FPGA"),
            (9, 3, "CCSDS 123"), (12, 2, "AXI4"), (14, 2, "MCP")], pal)
    bus(5, [(0, 2, None), (2, 3, "SPEC"), (5, 4, "SIM + VERIFY"), (9, 4, "BRING-UP"), (13, 3, "SHIP")],
        [None, t["violet"], t["cyan"], t["gold"], t["pink"]])

    o.append(
        f'  <text x="{X0 + 7.5 * CW}" y="{top + 3 * rh + 4}" text-anchor="middle" class="mono" font-size="11" '
        f'fill="{t["pink"]}">backpressure handled</text>'
    )

    # Sweeping cursor.
    o.append(
        f'''  <g>
    <path d="M{X0} {top - 14} V{H - 18}" stroke="{t["gold"]}" stroke-width="2"/>
    <path d="M{X0 - 7} {top - 20} H{X0 + 7} L{X0} {top - 11} Z" fill="{t["gold"]}"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;{XE - X0} 0" dur="7s" repeatCount="indefinite"/>
  </g>'''
    )
    return svg(W, H, "whoami.vcd: a waveform with RTL, RISC-V, FPGA, CCSDS 123, AXI4 and MCP on the data bus", "\n".join(o))


# --------------------------------------------------------------------------
# Project cards.
# --------------------------------------------------------------------------

PROJECTS = [
    dict(
        slug="hpdp", accent="gold", kicker="01 · SPACE PAYLOAD · ZCU106",
        title="Hyperspectral Payload Processor",
        desc="The onboard data chain of an Earth-observation satellite on a Zynq "
             "UltraScale+: sensor, CCSDS 123 compression, Reed-Solomon and AOS framing, "
             "a 1.25 Gbaud fiber link and a ground station that recovers it bit-exact.",
        stats=[("250 MHz", "timing met, full chip"), ("3.4×10¹²", "bits error-free"), ("944", "images bit-exact")],
        tags=["SystemVerilog", "Vivado", "CCSDS", "SEM + TMR"],
    ),
    dict(
        slug="payload", accent="cyan", kicker="02 · VENDOR-NEUTRAL RTL · CI",
        title="Onboard Payload Datapath",
        desc="Calibration, CCSDS 123.0-B-2 lossless compression and onboard analytics "
             "(NDVI, cloud mask, Sobel edges) that decide which frames are worth "
             "downlinking. SECDED memories and triplicated control.",
        stats=[("~7.2k", "LUTs, whole payload"), ("67", "simulation cases"), ("27/27", "injected bugs caught")],
        tags=["SystemVerilog", "AXI4-Stream", "Verilator", "Yosys"],
    ),
    dict(
        slug="efinity", accent="violet", kicker="03 · AI × EDA · OPEN SOURCE",
        title="efinity-mcp",
        desc="An MCP server that lets an AI assistant drive the Efinix Efinity "
             "toolchain: create projects, set up PLLs and I/O, compile, query "
             "static timing and program the board.",
        stats=[("27", "MCP tools"), ("47 s", "RTL to bitstream"), ("Ti375", "tested on silicon")],
        tags=["Python", "MCP", "Efinity", "Tcl STA"],
    ),
    dict(
        slug="riscv", accent="pink", kicker="04 · CPU MICROARCHITECTURE",
        title="RV32I RISC-V Core",
        desc="A RISC-V processor written from scratch in Verilog-2001: fetch, decode, "
             "ALU, register file, branches and jumps, verified by running assembly "
             "on the core and checking every writeback in the waveforms.",
        stats=[("RV32I", "base integer ISA"), ("27", "instructions"), ("5", "pipeline stages")],
        tags=["Verilog", "Icarus", "GTKWave", "RISC-V asm"],
    ),
]


def card(t, p):
    W, H = 600, 340
    a = t[p["accent"]]
    o = [frame(W, H, t)]
    o.append(f'  <rect x="32" y="30" width="44" height="5" rx="2.5" fill="{a}"/>')
    o.append(
        f'  <text x="32" y="64" class="mono" font-size="13" letter-spacing="2" fill="{a}">{esc(p["kicker"])}</text>'
    )
    o.append(
        f'  <text x="{W - 32}" y="64" text-anchor="end" class="mono" font-size="20" fill="{t["faint"]}">↗</text>'
    )
    o.append(
        f'  <text x="30" y="104" class="sans" font-size="31" font-weight="800" letter-spacing="-0.5" '
        f'fill="{t["text"]}">{esc(p["title"])}</text>'
    )
    for i, line in enumerate(wrap(p["desc"], 58)):
        o.append(
            f'  <text x="32" y="{140 + i * 25}" class="sans" font-size="17.5" fill="{t["muted"]}">{esc(line)}</text>'
        )
    o.append(f'  <path d="M32 232 H{W - 32}" stroke="{t["line"]}"/>')
    for i, (num, label) in enumerate(p["stats"]):
        x = 32 + i * 184
        o.append(
            f'  <text x="{x}" y="266" class="mono" font-size="25" font-weight="700" fill="{t["text"]}">{esc(num)}</text>'
        )
        o.append(
            f'  <text x="{x}" y="288" class="mono" font-size="12.5" fill="{t["faint"]}">{esc(label)}</text>'
        )
    x = 32
    for tag in p["tags"]:
        w = len(tag) * 7.8 + 22
        o.append(
            f'  <rect x="{x}" y="304" width="{w}" height="24" rx="12" fill="{a}" fill-opacity="0.12" '
            f'stroke="{a}" stroke-opacity="0.5"/>'
        )
        o.append(
            f'  <text x="{x + w / 2}" y="320.5" text-anchor="middle" class="mono" font-size="13" fill="{a}">{esc(tag)}</text>'
        )
        x += w + 8
    return svg(W, H, f'{p["title"]}: {p["desc"]}', "\n".join(o))


# --------------------------------------------------------------------------
# On the bench: the boards.
# --------------------------------------------------------------------------

BOARDS = [
    ("ZCU106", "Zynq UltraScale+ XCZU7EV", ["250 MHz payload chain,", "1.25 Gbaud SFP fiber link"], "gold"),
    ("Kintex-7", "GTX transceivers", ["Aurora links over SFP,", "high-speed serial bring-up"], "cyan"),
    ("Ti375 N1156", "Efinix Titanium", ["Built and programmed by", "an AI through efinity-mcp"], "violet"),
    ("Basys 3", "Artix-7", ["Where the Sobel edge", "accelerator started"], "pink"),
]


def bench(t):
    W, H = 1200, 250
    o = [frame(W, H, t)]
    bw, gap, x0 = 266, 20, 32
    for i, (name, part, lines, acc) in enumerate(BOARDS):
        a = t[acc]
        x, y = x0 + i * (bw + gap), 34
        o.append(f'  <rect x="{x}" y="{y}" width="{bw}" height="182" rx="12" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="1.5"/>')
        for k in range(10):
            o.append(f'  <rect x="{x + 18 + k * 24}" y="{y - 6}" width="9" height="6" rx="1" fill="{t["faint"]}" opacity="0.7"/>')
            o.append(f'  <rect x="{x + 18 + k * 24}" y="{y + 182}" width="9" height="6" rx="1" fill="{t["faint"]}" opacity="0.7"/>')
        o.append(
            f'  <circle cx="{x + bw - 24}" cy="{y + 26}" r="6" fill="{a}">'
            f'<animate attributeName="opacity" values="1;0.2;1" dur="{1.1 + i * 0.35:.2f}s" repeatCount="indefinite"/></circle>'
        )
        o.append(f'  <circle cx="{x + bw - 24}" cy="{y + 26}" r="11" fill="{a}" opacity="0.15"/>')
        o.append(f'  <text x="{x + 20}" y="{y + 36}" class="mono" font-size="21" font-weight="700" fill="{t["text"]}">{esc(name)}</text>')
        o.append(f'  <text x="{x + 20}" y="{y + 60}" class="mono" font-size="12.5" fill="{a}">{esc(part)}</text>')
        o.append(f'  <path d="M{x + 20} {y + 80} H{x + bw - 20}" stroke="{t["line"]}" stroke-dasharray="4 4"/>')
        for j, line in enumerate(lines):
            o.append(f'  <text x="{x + 20}" y="{y + 110 + j * 24}" class="sans" font-size="16" fill="{t["muted"]}">{esc(line)}</text>')
    return svg(W, H, "Boards on the bench: ZCU106, Kintex-7, Efinix Ti375, Basys 3", "\n".join(o))


# --------------------------------------------------------------------------
# The lab stack.
# --------------------------------------------------------------------------

STACK = [
    ("HDL + VERIFICATION", "gold", ["SystemVerilog", "Verilog-2001", "Self-checking testbenches",
                                    "Icarus · Verilator", "GTKWave", "Fault injection"]),
    ("TOOLCHAINS", "cyan", ["Vivado + Vitis", "Efinix Efinity", "Yosys",
                            "SystemRDL · PeakRDL", "Tcl, STA + CDC reports"]),
    ("INTERFACES + STANDARDS", "violet", ["AXI4-Lite · AXI4-Stream", "CCSDS 123.0-B-2",
                                         "AOS frames · Space Packets", "Reed-Solomon",
                                         "GTX · Aurora · SFP", "ECC · TMR · SEM"]),
    ("SOFTWARE", "pink", ["Python + pytest", "Bare-metal C on Cortex-A53", "RISC-V assembly",
                          "MCP servers", "Git + CI"]),
]


def stack(t):
    W, H = 1200, 300
    o = [frame(W, H, t)]
    cw = (W - 64) / 4
    for i, (head, acc, items) in enumerate(STACK):
        a = t[acc]
        x = 32 + i * cw + 8
        if i:
            o.append(f'  <path d="M{32 + i * cw} 34 V{H - 34}" stroke="{t["line"]}"/>')
        o.append(f'  <text x="{x + 8}" y="56" class="mono" font-size="13" letter-spacing="2" fill="{a}">{head}</text>')
        o.append(f'  <rect x="{x + 8}" y="68" width="28" height="3" rx="1.5" fill="{a}"/>')
        for j, it in enumerate(items):
            y = 104 + j * 31
            o.append(f'  <rect x="{x + 8}" y="{y - 9}" width="7" height="7" rx="1" fill="{a}" opacity="0.8"/>')
            o.append(f'  <text x="{x + 26}" y="{y}" class="sans" font-size="16.5" fill="{t["text"]}">{esc(it)}</text>')
    return svg(W, H, "Lab stack: HDL and verification, toolchains, interfaces and standards, software", "\n".join(o))


def main():
    for mode, t in THEMES.items():
        files = {
            "header": header(t),
            "whoami": waveform(t),
            "bench": bench(t),
            "stack": stack(t),
        }
        for p in PROJECTS:
            files[f'card-{p["slug"]}'] = card(t, p)
        for name, data in files.items():
            (OUT / f"{name}-{mode}.svg").write_text(data, encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)


if __name__ == "__main__":
    main()
