#!/usr/bin/env python3
"""
generate_pcb.py

1) Runs SKiDL script rf_gain_block.py to produce rf_gain_block.net
2) Loads template.kicad_pcb
3) Imports netlist into board
4) Places footprints at predefined coords
5) Routes simple 50Ω microstrip tracks
6) Pours ground zone
7) Saves final rf_gain_block.kicad_pcb
"""

import os
import subprocess
import pcbnew

# 1. Generate netlist by running SKiDL script
subprocess.run(["python3", "rf_gain_block.py"], check=True)

# 2. Load template PCB
template = "template.kicad_pcb"
board = pcbnew.LoadBoard(template)

# 3. Import the netlist into the board
netfile = "rf_gain_block.net"
netlist = pcbnew.NETLIST_READER.BoardImporter(board)
netlist.SetNetlistFilename(netfile)
netlist.Configure(board, pcbnew.NETLIST_READER.IMPORT_USES_EARTH_GROUND)
netlist.Import()

# 4. Footprint placement (coordinates in mm)
placements = {
    "Q1":    (80, 50),
    "C1":    (60, 50),
    "L_in":  (70, 50),
    "C_sh_in": (70, 60),
    "Lb1":   (80, 60),
    "Rd":    (90, 60),
    "C_bp1": (90, 70),
    "L_out": (100, 50),
    "C2":    (110, 50),
    "C_sh_out": (110, 60),
    "BPF_IN":  (50, 50),
    "BPF_OUT": (130, 50),
}

for f in board.GetFootprints():
    ref = f.GetReference()
    if ref in placements:
        x_mm, y_mm = placements[ref]
        f.SetPosition(pcbnew.wxPointMM(x_mm, y_mm))
        f.SetOrientation(0)   # 0°, rotate if needed

# 5. Simple routing between pads (straight lines)
#    This example assumes one pad per net; for real boards you'll need a router.
track_width = pcbnew.FromMM(1.0)  # 1 mm track for ~50 Ω on FR-4 1.6 mm
def route(net_name, start_pad, end_pad):
    net = board.FindNet(net_name)
    start = start_pad.GetPosition()
    end   = end_pad.GetPosition()
    segment = pcbnew.PCB_TRACK(board)
    segment.SetStart(start)
    segment.SetEnd(end)
    segment.SetWidth(track_width)
    segment.SetNetCode(net.GetNet())
    board.Add(segment)

# Example: route RF_IN → C1 pad “1”
pad_rf_in = board.FindFootprintByReference("BPF_IN").FindPadByNumber("OUT")
pad_c1    = board.FindFootprintByReference("C1").FindPadByNumber("1")
route("RF_IN", pad_rf_in, pad_c1)

# ... repeat route() calls for each connection ...

# 6. Pour ground zone on bottom copper
zone = pcbnew.ZONE_CONTAINER(board)
zone.SetLayer(pcbnew.B_Cu)
zone.SetIsFilled(True)
zone.SetNetCode(board.FindNet("GND").GetNet())
outline = pcbnew.ZONE_FILL_CONTROLLER(board).GetOutlineForBoard()
zone.Outline().AddOutline(outline)
board.Add(zone)

# 7. Finalize and save
pcbnew.Refresh()
output = "rf_gain_block.kicad_pcb"
board.Save(output)
print(f"PCB written to {output}")
