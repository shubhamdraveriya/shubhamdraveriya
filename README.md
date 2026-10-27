<a href="https://shubhamdraveriya.github.io/website/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
    <img alt="Shubham Draveriya — RTL design and embedded systems engineer. I build hardware that has to work the first time." src="assets/header-light.svg" width="100%">
  </picture>
</a>

<p align="center">
  <a href="https://shubhamdraveriya.github.io/website/"><img alt="Website" src="https://img.shields.io/badge/website-the%20die%20stack-e9b949?style=for-the-badge&labelColor=15172b"></a>
  <a href="https://www.linkedin.com/in/shubham-draveriya"><img alt="LinkedIn" src="https://img.shields.io/badge/linkedin-shubham--draveriya-6fe3e1?style=for-the-badge&labelColor=15172b"></a>
  <a href="https://drive.google.com/file/d/1e9Pp6eI2Jy77L3aIGjsXdL-Me41j0Ima/view?usp=drive_link"><img alt="Resume" src="https://img.shields.io/badge/resume-pdf-9b8cff?style=for-the-badge&labelColor=15172b"></a>
  <img alt="Open to RTL, verification and FPGA roles" src="https://img.shields.io/badge/status-open%20to%20RTL%20%2F%20FPGA%20roles-ff7ab6?style=for-the-badge&labelColor=15172b">
</p>

## `$ whoami`

I write RTL, debug it waveform by waveform, and bring it up on real boards. Lately that means
a satellite's onboard data chain on a Zynq UltraScale+: hyperspectral samples go in, get
compressed to the CCSDS 123 standard, framed and Reed-Solomon coded, shot down a fiber link,
and come out the other side **bit-exact**.

The part I enjoy most is bring-up: running code on a core I built, staring at the trace until
the bug gives itself away, then fixing it for real.

```systemverilog
module shubham_draveriya (
  input  logic clk,                 // 250 MHz, every rising edge counts
  input  spec_t spec,
  output silicon_t silicon          // CDC clean, bit-exact
);
  always_ff @(posedge clk)
    silicon <= bring_up(verify(rtl(spec)));
endmodule
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/whoami-dark.svg">
  <img alt="whoami.vcd: a waveform with RTL, RISC-V, FPGA, CCSDS 123, AXI4 and MCP on the data bus, going from spec through simulation and bring-up to ship" src="assets/whoami-light.svg" width="100%">
</picture>

## Featured silicon

<p align="center">
  <a href="https://github.com/shubhamdraveriya/Hyperspectral-Payload-Processor"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-hpdp-dark.svg">
    <img alt="Hyperspectral Payload Processor: a satellite's onboard data chain on a ZCU106, 250 MHz timing met, 3.4×10¹² bits error-free over fiber, 944 images bit-exact" src="assets/card-hpdp-light.svg" width="49%">
  </picture></a>
  <a href="https://github.com/shubhamdraveriya/Image-Processing-Accelerator-for-Edge-Detection"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-payload-dark.svg">
    <img alt="Onboard Payload Datapath: vendor-neutral SystemVerilog for calibration, CCSDS 123 compression and onboard analytics, about 7.2k LUTs, 67 simulation cases, 27 of 27 injected bugs caught" src="assets/card-payload-light.svg" width="49%">
  </picture></a>
  <a href="https://github.com/shubhamdraveriya/efinity-mcp"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-efinity-dark.svg">
    <img alt="efinity-mcp: an MCP server that lets an AI assistant drive the Efinix Efinity FPGA toolchain, 27 tools, RTL to bitstream in 47 seconds, tested on a Ti375" src="assets/card-efinity-light.svg" width="49%">
  </picture></a>
  <a href="https://github.com/shubhamdraveriya/RISC-V"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-riscv-dark.svg">
    <img alt="RV32I RISC-V core written from scratch in Verilog-2001, 27 instructions, 5 pipeline stages" src="assets/card-riscv-light.svg" width="49%">
  </picture></a>
</p>

<details>
<summary><b>What's behind the HPDP numbers</b></summary>
<br>

| Milestone | What was proven, on the board |
|---|---|
| CCSDS 123 compressor | bit-exact on all 864 configurations of the test matrix; 250 MHz at 13.6k LUTs |
| Reference models | byte-identical with an independent CCSDS 123.0-B-2 implementation (NTNU) on 944 images |
| Optical downlink | PRBS-31, 3.4 × 10¹² bits error-free over OM3 fiber at 1.25 Gbaud |
| Error correction | scenes recovered bit-exact at a channel BER of 0, 10⁻⁴ and 10⁻³ |
| Sustained rate | 76.8 Msamples/s for 10 minutes without a dropped line |
| Radiation mitigation | SEM scrubbing corrects upsets in ≤ 153 ms; ECC, TMR, watchdogs; no silent corruption in protected state |

Full report in [the repository](https://github.com/shubhamdraveriya/Hyperspectral-Payload-Processor).

</details>

## On the bench

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/bench-dark.svg">
  <img alt="Boards on the bench: ZCU106 (Zynq UltraScale+), Kintex-7 with GTX transceivers, Efinix Ti375 N1156, and Basys 3 (Artix-7)" src="assets/bench-light.svg" width="100%">
</picture>

## The lab stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img alt="HDL and verification: SystemVerilog, Verilog-2001, self-checking testbenches, Icarus, Verilator, GTKWave, fault injection. Toolchains: Vivado and Vitis, Efinix Efinity, Yosys, SystemRDL and PeakRDL, Tcl. Interfaces and standards: AXI4, CCSDS 123.0-B-2, AOS frames and Space Packets, Reed-Solomon, GTX, Aurora, SFP, ECC, TMR, SEM. Software: Python and pytest, bare-metal C on Cortex-A53, RISC-V assembly, MCP servers, Git and CI." src="assets/stack-light.svg" width="100%">
</picture>

## Right now

- 🛰️ **HPDP**: milestones M0–M7 are done and board-tested, including the `NX_MAX` 1024 build and runs on real hyperspectral data.
- 🤖 **efinity-mcp**: v0.1.0 is out. It is tested on Windows; if you run Efinity on Linux, I'd like to hear how it goes.
- 🔍 **Looking for**: internships, full-time roles and collaborations in RTL design, verification and FPGA bring-up.

## Let's talk

Hiring for RTL, verification or bring-up work, or building something with FPGAs in it?
Find me on [LinkedIn](https://www.linkedin.com/in/shubham-draveriya), grab my
[resume](https://drive.google.com/file/d/1e9Pp6eI2Jy77L3aIGjsXdL-Me41j0Ima/view?usp=drive_link),
or take [the chip apart on my website](https://shubhamdraveriya.github.io/website/).

<p align="center"><sub><code>$finish;</code> · artwork is hand-written SVG from <a href="assets/generate.py"><code>assets/generate.py</code></a> and follows your light or dark theme</sub></p>
