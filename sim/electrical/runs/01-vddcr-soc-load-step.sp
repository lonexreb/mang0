* sim/electrical/runs/01-vddcr-soc-load-step.sp
*
* Validate VDDCR_SOC multiphase regulation under 0->80 A load step.
* Pass criteria (per AMD Strix Halo PDG): undershoot < 50 mV, recovery < 50 us.
*
* This is a STUB — drop in TI's TPS53676 SPICE model and replace
* the placeholder behavioral source with the vendor model.
*
* Vendor model: download from https://www.ti.com/product/TPS53676/toolssoftware
* Place in sim/electrical/models/ as tps53676.lib

.include ../models/tps53676.lib  ; vendor model — not yet committed

* --- Stimulus -----------------------------------------------------------------
Vin   VIN  0   12
Iload VOUT 0   PWL(0 0    100u 0    101u 80    500u 80    501u 0    1m 0)

* --- DUT (placeholder behavioral) ---------------------------------------------
* Replace with: XU1 VIN VOUT GND <ctrl pins> TPS53676
* For now, ideal voltage source so the deck runs:
Vsoc VOUT 0 0.95

* --- Bulk + ceramic decoupling per PDG recommendation ------------------------
Cb1 VOUT 0 470u  ; bulk
Cb2 VOUT 0 470u  ; bulk
Cb3 VOUT 0 470u  ; bulk
Cc1 VOUT 0 22u   ; ceramic
Cc2 VOUT 0 22u
Cc3 VOUT 0 22u
Cc4 VOUT 0 22u

* --- Analysis ----------------------------------------------------------------
.tran 100n 1.5m
.measure tran v_undershoot MIN V(VOUT) FROM=100u TO=300u
.measure tran v_recovery   WHEN V(VOUT)=0.95 RISE=1 TD=101u
.print tran V(VOUT) I(Iload)

.end
