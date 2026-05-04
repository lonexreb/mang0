"""Single source of truth for mang0 mechanical dimensions.

All units are millimetres. Origin convention:
- Lower chassis sits on Z=0
- Motherboard origin at the geometric centre of the lower chassis floor
- Lid hinges at the rear edge

Update these and re-run generate_starter_scene.py to refresh the
Blender scene. Anything that mutates these (Claude via the Blender
MCP connector, hand edits, etc.) must update this file too — the
scene script re-reads it on every regeneration.
"""

# --- External envelope (closed lid) -------------------------------------------
ENVELOPE_W = 300.0   # left-right (mm)
ENVELOPE_D = 215.0   # front-back
ENVELOPE_H = 16.0    # closed-lid total

WALL_T = 1.5         # CNC chassis wall

# --- Display lid --------------------------------------------------------------
LID_H = 5.5
PANEL_W = 295.0      # Samsung ATNA33TP11 active area approximation
PANEL_D = 165.0
PANEL_T = 1.2
BEZEL_T = 4.0

# --- Lower chassis ------------------------------------------------------------
LOWER_H = ENVELOPE_H - LID_H

# --- Motherboard --------------------------------------------------------------
MB_W = 280.0
MB_D = 90.0
MB_T = 1.6           # 12-layer HDI
MB_OFFSET_Y = -45.0  # toward the rear under the keyboard
MB_OFFSET_Z = WALL_T

# --- Strix Halo BGA + LPDDR5X PoP ---------------------------------------------
SOC_SIZE = 25.0
SOC_T = 2.0
SOC_OFFSET_X = -40.0  # left of MB centre
SOC_OFFSET_Y = 0.0

# --- Hailo-10H (M.2 Key M, 2280) ----------------------------------------------
HAILO_W = 22.0
HAILO_D = 80.0
HAILO_T = 4.0
HAILO_OFFSET_X = 70.0
HAILO_OFFSET_Y = 20.0

# --- NVMe primary (M.2 2280) --------------------------------------------------
NVME_W = 22.0
NVME_D = 80.0
NVME_T = 3.5
NVME_OFFSET_X = 70.0
NVME_OFFSET_Y = -20.0

# --- WiFi 7 module (M.2 E-key 2230) -------------------------------------------
WIFI_W = 22.0
WIFI_D = 30.0
WIFI_T = 3.0
WIFI_OFFSET_X = 110.0
WIFI_OFFSET_Y = 0.0

# --- Battery pack (4S1P pouch cells) ------------------------------------------
# Pouch cells are required for a 16 mm-thick laptop. 21700 cylindrical cells
# (21 mm diameter) listed in BOM.md as the *fallback* would force the envelope
# to grow to ~26 mm — laptop-hostile.
#
# Default cell here matches the anyon_e v1 reference (~15.7 Wh per cell).
# Amprius SiCore pouches in similar form factor are the v2 target when
# available — see batteries/README.md.
BATT_CELL_W = 100.0  # length of a single pouch
BATT_CELL_D = 67.0   # width
BATT_CELL_T = 5.7    # thickness
BATT_CELLS = 4       # 4S1P
# Lay cells side-by-side along Y (2×2 stack along the front edge):
# total pack envelope:
BATT_PACK_W = 2 * BATT_CELL_W   # 200
BATT_PACK_D = 2 * BATT_CELL_D   # 134
BATT_PACK_T = BATT_CELL_T       # 5.7 (single layer)
BATT_OFFSET_Y = 30.0  # toward the front, under the palm rest

# --- Vapor chamber + blowers --------------------------------------------------
VC_W = 80.0
VC_D = 60.0
VC_T = 1.5
BLOWER_W = 35.0
BLOWER_D = 35.0
BLOWER_T = 6.0
BLOWER_OFFSET = 60.0  # left and right of vapor chamber centre

# --- Trackpad -----------------------------------------------------------------
TRACKPAD_W = 130.0
TRACKPAD_D = 80.0
TRACKPAD_T = 1.5
TRACKPAD_OFFSET_Y = 60.0

# --- USB-C ports (×2, on each side) -------------------------------------------
USBC_W = 9.0
USBC_D = 8.5
USBC_T = 3.5

# --- Sanity check (run with `python3 chassis/blender/dimensions.py`) ----------
if __name__ == "__main__":
    import textwrap
    print(textwrap.dedent(f"""
        mang0 dimensional sanity check
        ------------------------------
        envelope         {ENVELOPE_W:>6} x {ENVELOPE_D} x {ENVELOPE_H} mm
        lid              {ENVELOPE_W - 2*WALL_T:>6} x {ENVELOPE_D - 2*WALL_T} x {LID_H} mm
        lower            {ENVELOPE_W - 2*WALL_T:>6} x {ENVELOPE_D - 2*WALL_T} x {LOWER_H} mm
        motherboard      {MB_W:>6} x {MB_D} x {MB_T} mm
        battery pack     {BATT_PACK_W:>6} x {BATT_PACK_D} x {BATT_PACK_T} mm  ({BATT_CELLS} pouch cells, 2x2)
        vapor chamber    {VC_W:>6} x {VC_D} x {VC_T} mm
        blowers (each)   {BLOWER_W:>6} x {BLOWER_D} x {BLOWER_T} mm
    """).strip())

    # Fit checks
    assert MB_W < ENVELOPE_W - 2 * WALL_T, "Motherboard wider than chassis interior"
    assert MB_D < ENVELOPE_D - 2 * WALL_T, "Motherboard deeper than chassis interior"
    assert BATT_PACK_T < LOWER_H - WALL_T, "Battery pack too thick for lower chassis"
    assert MB_T + max(SOC_T, HAILO_T, NVME_T) + VC_T < LOWER_H - WALL_T, \
        "Stack-up (MB + components + vapor chamber) does not fit in lower chassis"
    print("\nALL FITS OK")
