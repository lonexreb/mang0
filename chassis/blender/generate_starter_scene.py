"""Generate the mang0 industrial-design starter scene in Blender.

Run inside Blender 4.2+ via:

    Scripting > Open > generate_starter_scene.py > Run Script

…or headless:

    blender --background --python chassis/blender/generate_starter_scene.py \
            --output-file chassis/blender/mang0.blend

Once the scene exists, Claude (via the Blender MCP connector wired in
.mcp.json) can read/mutate it conversationally:

    "Move the vapor chamber 5 mm forward and re-export STEP."
    "Add a 1 mm chamfer to the lower chassis bottom edges."
    "Show me the cross-section through the SoC and battery."

The script is idempotent — it clears any objects in the mang0
collections and rebuilds them from dimensions.py so re-runs always
match the dimension file.
"""
from __future__ import annotations

import math
import os
import sys

# Make dimensions.py importable when running headless
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dimensions as D  # noqa: E402

try:
    import bpy  # type: ignore
except ImportError:
    print("This script must run inside Blender. See module docstring.")
    sys.exit(1)


# --- Helpers -----------------------------------------------------------------

def clear_collection(name: str) -> bpy.types.Collection:
    coll = bpy.data.collections.get(name)
    if coll:
        for obj in list(coll.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(coll)
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def make_material(name: str, rgba: tuple[float, float, float, float],
                  metallic: float = 0.0, roughness: float = 0.5,
                  alpha: float = 1.0) -> bpy.types.Material:
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if alpha < 1.0:
            mat.blend_method = "BLEND"
            bsdf.inputs["Alpha"].default_value = alpha
    return mat


def make_box(name: str, w: float, d: float, h: float,
             location: tuple[float, float, float],
             collection: bpy.types.Collection,
             material: bpy.types.Material) -> bpy.types.Object:
    """Add a box of size w x d x h centred at `location`. Sizes are mm
    but Blender uses metres internally — we scale by 0.001."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=tuple(c * 0.001 for c in location))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (w * 0.001, d * 0.001, h * 0.001)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.clear()
    obj.data.materials.append(material)
    # Move from default scene collection into ours
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def make_cylinder(name: str, radius: float, height: float,
                  location: tuple[float, float, float], rotation_x: float,
                  collection: bpy.types.Collection,
                  material: bpy.types.Material) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius * 0.001, depth=height * 0.001,
        location=tuple(c * 0.001 for c in location),
        rotation=(rotation_x, 0, 0),
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.clear()
    obj.data.materials.append(material)
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


# --- Build scene -------------------------------------------------------------

def build_scene() -> None:
    # Wipe default cube/light/camera if present
    for name in ("Cube", "Light", "Camera"):
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    # Materials
    mat_aluminum = make_material("Anodized Aluminum", (0.10, 0.10, 0.11, 1.0),
                                 metallic=0.85, roughness=0.35)
    mat_pcb = make_material("FR-4 PCB", (0.10, 0.35, 0.18, 1.0),
                            metallic=0.0, roughness=0.6)
    mat_copper = make_material("Copper", (0.85, 0.45, 0.20, 1.0),
                               metallic=0.95, roughness=0.30)
    mat_silicon = make_material("BGA Silicon", (0.05, 0.05, 0.05, 1.0),
                                metallic=0.30, roughness=0.45)
    mat_battery = make_material("Cell Wrap", (0.15, 0.15, 0.15, 1.0),
                                metallic=0.0, roughness=0.7)
    mat_npu = make_material("NPU PCB", (0.10, 0.10, 0.45, 1.0),
                            metallic=0.0, roughness=0.6)
    mat_amoled = make_material("AMOLED", (0.02, 0.02, 0.02, 1.0),
                               metallic=0.0, roughness=0.05)
    mat_glass = make_material("Trackpad Glass", (0.85, 0.85, 0.90, 0.4),
                              metallic=0.0, roughness=0.05, alpha=0.4)

    # Collections
    coll_chassis = clear_collection("Chassis")
    coll_mb = clear_collection("Motherboard")
    coll_battery = clear_collection("Battery")
    coll_cooling = clear_collection("Cooling")
    coll_display = clear_collection("Display")
    coll_input = clear_collection("Input")

    # --- Lower chassis (closed shell, rough) -----------------------------------
    lower_floor_z = D.WALL_T / 2
    make_box("Chassis_LowerFloor",
             w=D.ENVELOPE_W, d=D.ENVELOPE_D, h=D.WALL_T,
             location=(0, 0, lower_floor_z),
             collection=coll_chassis, material=mat_aluminum)

    # Side walls (4)
    side_wall_z = D.LOWER_H / 2
    make_box("Chassis_LowerLeft",
             w=D.WALL_T, d=D.ENVELOPE_D, h=D.LOWER_H,
             location=(-D.ENVELOPE_W / 2 + D.WALL_T / 2, 0, side_wall_z),
             collection=coll_chassis, material=mat_aluminum)
    make_box("Chassis_LowerRight",
             w=D.WALL_T, d=D.ENVELOPE_D, h=D.LOWER_H,
             location=(D.ENVELOPE_W / 2 - D.WALL_T / 2, 0, side_wall_z),
             collection=coll_chassis, material=mat_aluminum)
    make_box("Chassis_LowerFront",
             w=D.ENVELOPE_W, d=D.WALL_T, h=D.LOWER_H,
             location=(0, D.ENVELOPE_D / 2 - D.WALL_T / 2, side_wall_z),
             collection=coll_chassis, material=mat_aluminum)
    make_box("Chassis_LowerRear",
             w=D.ENVELOPE_W, d=D.WALL_T, h=D.LOWER_H,
             location=(0, -D.ENVELOPE_D / 2 + D.WALL_T / 2, side_wall_z),
             collection=coll_chassis, material=mat_aluminum)

    # --- Lid (hinged at rear, closed for layout) ------------------------------
    lid_z = D.LOWER_H + D.LID_H / 2
    make_box("Chassis_LidShell",
             w=D.ENVELOPE_W, d=D.ENVELOPE_D, h=D.LID_H,
             location=(0, 0, lid_z),
             collection=coll_display, material=mat_aluminum)
    make_box("Display_PanelAMOLED",
             w=D.PANEL_W, d=D.PANEL_D, h=D.PANEL_T,
             location=(0, 0, D.LOWER_H + D.LID_H - D.PANEL_T / 2 - 0.5),
             collection=coll_display, material=mat_amoled)

    # --- Motherboard ---------------------------------------------------------
    mb_z = D.MB_OFFSET_Z + D.MB_T / 2
    make_box("Motherboard_PCB",
             w=D.MB_W, d=D.MB_D, h=D.MB_T,
             location=(0, D.MB_OFFSET_Y, mb_z),
             collection=coll_mb, material=mat_pcb)

    # Strix Halo BGA + LPDDR5X PoP (modeled as one stacked block)
    soc_z = mb_z + D.MB_T / 2 + D.SOC_T / 2
    make_box("MB_StrixHalo_SoC",
             w=D.SOC_SIZE, d=D.SOC_SIZE, h=D.SOC_T,
             location=(D.SOC_OFFSET_X, D.MB_OFFSET_Y + D.SOC_OFFSET_Y, soc_z),
             collection=coll_mb, material=mat_silicon)

    # Hailo-10H NPU (M.2 2280 in M-key slot)
    hailo_z = mb_z + D.MB_T / 2 + D.HAILO_T / 2
    make_box("MB_Hailo10H_NPU",
             w=D.HAILO_W, d=D.HAILO_D, h=D.HAILO_T,
             location=(D.HAILO_OFFSET_X, D.MB_OFFSET_Y + D.HAILO_OFFSET_Y, hailo_z),
             collection=coll_mb, material=mat_npu)

    # NVMe primary
    nvme_z = mb_z + D.MB_T / 2 + D.NVME_T / 2
    make_box("MB_NVMe_Primary",
             w=D.NVME_W, d=D.NVME_D, h=D.NVME_T,
             location=(D.NVME_OFFSET_X, D.MB_OFFSET_Y + D.NVME_OFFSET_Y, nvme_z),
             collection=coll_mb, material=mat_npu)

    # WiFi 7 (E-key)
    wifi_z = mb_z + D.MB_T / 2 + D.WIFI_T / 2
    make_box("MB_MT7925_WiFi7",
             w=D.WIFI_W, d=D.WIFI_D, h=D.WIFI_T,
             location=(D.WIFI_OFFSET_X, D.MB_OFFSET_Y + D.WIFI_OFFSET_Y, wifi_z),
             collection=coll_mb, material=mat_npu)

    # --- Vapor chamber + blowers ---------------------------------------------
    vc_z = soc_z + D.SOC_T / 2 + D.VC_T / 2
    make_box("Cooling_VaporChamber",
             w=D.VC_W, d=D.VC_D, h=D.VC_T,
             location=(D.SOC_OFFSET_X, D.MB_OFFSET_Y, vc_z),
             collection=coll_cooling, material=mat_copper)

    blower_z = mb_z + D.MB_T / 2 + D.BLOWER_T / 2
    make_box("Cooling_Blower_L",
             w=D.BLOWER_W, d=D.BLOWER_D, h=D.BLOWER_T,
             location=(D.SOC_OFFSET_X - D.BLOWER_OFFSET, D.MB_OFFSET_Y, blower_z),
             collection=coll_cooling, material=mat_aluminum)
    make_box("Cooling_Blower_R",
             w=D.BLOWER_W, d=D.BLOWER_D, h=D.BLOWER_T,
             location=(D.SOC_OFFSET_X + D.BLOWER_OFFSET, D.MB_OFFSET_Y, blower_z),
             collection=coll_cooling, material=mat_aluminum)

    # --- Battery pack (4 pouch cells, 2x2 grid laid flat along XY) -----------
    batt_z = D.WALL_T + D.BATT_CELL_T / 2
    # 2 columns x 2 rows of pouches, centred at (0, BATT_OFFSET_Y)
    layout = [
        (-D.BATT_CELL_W / 2,  D.BATT_CELL_D / 2),
        ( D.BATT_CELL_W / 2,  D.BATT_CELL_D / 2),
        (-D.BATT_CELL_W / 2, -D.BATT_CELL_D / 2),
        ( D.BATT_CELL_W / 2, -D.BATT_CELL_D / 2),
    ]
    for i, (dx, dy) in enumerate(layout):
        make_box(
            name=f"Battery_Pouch_{i + 1}",
            w=D.BATT_CELL_W, d=D.BATT_CELL_D, h=D.BATT_CELL_T,
            location=(dx, D.BATT_OFFSET_Y + dy, batt_z),
            collection=coll_battery, material=mat_battery,
        )

    # --- Trackpad ------------------------------------------------------------
    trackpad_z = D.LOWER_H - D.TRACKPAD_T / 2
    make_box("Input_TrackpadGlass",
             w=D.TRACKPAD_W, d=D.TRACKPAD_D, h=D.TRACKPAD_T,
             location=(0, D.TRACKPAD_OFFSET_Y, trackpad_z),
             collection=coll_input, material=mat_glass)

    # --- USB-C ports (port openings) ----------------------------------------
    port_z = D.LOWER_H * 0.6
    make_box("IO_USBC_Left",
             w=D.USBC_T, d=D.USBC_W, h=D.USBC_D,
             location=(-D.ENVELOPE_W / 2 + D.USBC_T / 2, 0, port_z),
             collection=coll_input, material=mat_silicon)
    make_box("IO_USBC_Right",
             w=D.USBC_T, d=D.USBC_W, h=D.USBC_D,
             location=(D.ENVELOPE_W / 2 - D.USBC_T / 2, 0, port_z),
             collection=coll_input, material=mat_silicon)


def setup_camera_and_lighting() -> None:
    # Camera: hero 3/4 angle
    bpy.ops.object.camera_add(location=(0.45, -0.45, 0.30),
                              rotation=(math.radians(60), 0, math.radians(45)))
    cam = bpy.context.active_object
    cam.name = "HeroCamera"
    cam.data.lens = 50
    bpy.context.scene.camera = cam

    # Three-point lighting
    bpy.ops.object.light_add(type="AREA", location=(0.5, -0.5, 0.6))
    bpy.context.active_object.data.energy = 80
    bpy.context.active_object.name = "KeyLight"

    bpy.ops.object.light_add(type="AREA", location=(-0.4, -0.3, 0.5))
    bpy.context.active_object.data.energy = 30
    bpy.context.active_object.name = "FillLight"

    bpy.ops.object.light_add(type="AREA", location=(0.0, 0.6, 0.6))
    bpy.context.active_object.data.energy = 40
    bpy.context.active_object.name = "RimLight"

    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.02, 0.02, 0.025, 1)
        bg.inputs["Strength"].default_value = 0.4

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080


def main() -> None:
    build_scene()
    setup_camera_and_lighting()

    # If invoked with --output-file <path>, save the .blend
    if "--output-file" in sys.argv:
        idx = sys.argv.index("--output-file")
        out_path = sys.argv[idx + 1]
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out_path))
        print(f"Saved: {out_path}")
    else:
        print("Scene built. Save the file in Blender (Ctrl+S) "
              "or pass --output-file <path> when running headless.")


if __name__ == "__main__":
    main()
