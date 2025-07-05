# Wideband RF HF Gain Amplifier (0.1–50 MHz)
#### Author: Bocaletto Luca

## Introduction  
This document describes the design, simulation, PCB layout, and testing procedures for a two-stage wideband RF gain block amplifier covering 0.1 to 50 MHz. The amplifier delivers 24 dB gain, a noise figure below 3 dB, and unconditional stability while operating from a single 5 V supply. All component values, footprints, and layout guidelines are provided to support a seamless transition to prototyping and production.

## Project Objectives  
The goal is to amplify HF signals up to 50 MHz with flat gain, low noise, and minimal distortion. The amplifier must interface to 50 Ω systems, consume less than 25 mA total current, and require no external matching resistors thanks to internally matched MMIC devices. Two identical Mini-Circuits PSA4-5043+ amplifiers are cascaded to achieve the target gain and linearity.

## System Specifications  
The amplifier meets the following targets:  
– Frequency range: 0.1–50 MHz  
– Small-signal gain: 24 dB ±1 dB  
– Noise figure: ≤ 3 dB total  
– Input/output impedance: 50 Ω  
– Input P1 dB: ≥ +10 dBm  
– Output P1 dB: ≥ +15 dBm  
– IIP3: > +10 dBm  
– Supply voltage: 5 V DC  
– Supply current: < 25 mA  
– Stability: Unconditionally stable (Rollett’s K > 1)  
– PCB substrate: FR-4, εr ≈ 4.4, thickness 1.6 mm  

## Active Device Selection  
The Mini-Circuits PSA4-5043+ MMIC in SOT-23-6 is chosen for both stages. It offers 12 dB gain, 2 dB noise figure, and DC–500 MHz bandwidth at a 5 V, 10 mA bias. Cascading two devices provides approximately 24 dB of flat gain across the HF band while maintaining low noise and excellent linearity. An S-parameter model is available for accurate simulation in ADS or LTspice.

## Circuit Architecture and Biasing  
Each MMIC stage is biased in class A. The 5 V supply is fed through a 220 nH RF choke to isolate RF from the DC rail. A 100 nF bypass capacitor placed next to each MMIC pin ensures a low-impedance path to ground at HF. No external bias resistors or matching networks are required, as the PSA4-5043+ integrates its own bias network and maintains a 50 Ω match internally.

Between the two stages and at the amplifier input and output, 220 nF coupling capacitors provide AC coupling down to 0.1 MHz. These large-value caps allow the amplifier to pass DC-coupled signals virtually to DC, ensuring a flat response from 0.1 MHz.

## RF Coupling and Filtering  
To suppress out-of-band signals and protect against strong broadcast interference, dual T-section band-pass filters on the PCB can be implemented at the amplifier input and output. Each filter comprises two series inductors and a shunt capacitor, tuned for a 0.1–50 MHz passband. The filters minimize unwanted low-frequency DC shifts and high-frequency noise without disrupting the HF gain.

## Simulation and Verification  
The complete schematic—including two PSA4-5043+ devices, coupling capacitors, RF chokes, bypass capacitors, and optional T-filters—is imported into ADS and LTspice. An AC sweep from 10 kHz to 100 MHz verifies gain flatness, input/output return loss, noise figure (using the noise model), and unconditional stability (Rollett’s K factor). A two-tone simulation at 10 MHz and 30 MHz evaluates IIP3 linearity.

## PCB Layout Guidelines  
The layout is optimized for HF performance on FR-4. RF traces are drawn as 50 Ω microstrip (≈ 3 mm width) but impedance control is relaxed below 50 MHz. Critical components—MMICs, RF chokes, bypass capacitors, and coupling caps—are placed within 1 mm of each other. A solid ground plane on the bottom layer with via stitching every 5 mm ensures low ground impedance. All RF/DC components are clustered to minimize parasitic inductance and capacitance.

## Bill of Materials  
A minimal parts list includes:  
- 2 × Mini-Circuits PSA4-5043+ (SOT-23-6)  
- 4 × 220 nF coupling capacitors, 0805, 6.3 V  
- 2 × 220 nH RF chokes, 0603  
- 2 × 100 nF bypass capacitors, 0805, 10 V  
- Optional filter parts: inductors and capacitors for two T-sections per filter stage  

## Testing Procedures  
After prototyping, performance is verified as follows:  
1. Measure S-parameters with a network analyzer to confirm gain, return loss, and input P1 dB.  
2. Measure noise figure on a noise-figure analyzer across 0.1–50 MHz.  
3. Perform two-tone IIP3 testing on a spectrum analyzer at representative HF frequencies.  
4. Verify stability by sweeping from DC to 500 MHz and ensuring no oscillations.  
5. Conduct temperature testing from –20 °C to +70 °C to characterize drift.

## ASCII Schematic Diagram  
```plaintext
           RF_IN ── C_in1 ──[PSA4-5043+]── C_coup ──[PSA4-5043+]── C_out2 ── RF_OUT
                     │         │            │         │
                    GND       CHK1         CHK2      GND
                               │            │
                              VCC          VCC
                     C_bp1     │            │     C_bp2
                     │         │            │     │
                    GND       GND          GND   GND

Legend:
C_in1/C_out2 – 220 nF coupling capacitors
C_coup       – 220 nF interstage coupling capacitor
CHK1/CHK2    – 220 nH RF choke on supply line
C_bp1/C_bp2  – 100 nF DC bypass capacitors
[PSA4-5043+] – MMIC amplifier, 12 dB gain, DC–500 MHz
```

## File .py generate PCB scheme

Below is an example Python script that uses SKiDL to generate the netlist and then KiCad’s pcbnew Python API to import that netlist, place footprints, draw 50 Ω microstrip tracks, pour a ground zone and export a finished .kicad_pcb. You’ll need KiCad 6+ installed, and to run this on the same machine where pcbnew is available in Python.

Save this as generate_pcb.py alongside:

A KiCad PCB template named template.kicad_pcb (empty board with correct layers).

The SKiDL script rf_gain_block.py from before, to produce rf_gain_block.net.

## file python How it works:

           • Step 1 calls your SKiDL script to emit rf_gain_block.net. 
           • Step 2 loads a nearly-empty KiCad board with your layer stack. 
           • Step 3 imports the netlist, adding footprints to the board. 
           • Step 4 positions each footprint at exact (x,y) mm coordinates. 
           • Step 5 shows how to draw a straight track for each net; in practice you’ll add one route() call per net or hook up an autorouter. 
           • Step 6 pours a ground zone on the bottom copper connected to GND. 
           • Step 7 writes out the final .kicad_pcb, ready for DRC and Gerber export.

---

[![Read Online](https://img.shields.io/badge/Read%20Online-blue)](https://bocaletto-luca.github.io/RF-Amplifier-HF/index.html)  

[![Read Online](https://img.shields.io/badge/Read%20Online-blue)](https://bocaletto-luca.github.io/RF-Amplifier-WiFi/index.html)

---
