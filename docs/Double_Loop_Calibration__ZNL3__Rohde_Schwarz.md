# Double-Loop H-Field Probe Calibration: Example on Rohde & Schwarz ZNL3 (English)

The double-loop probe (one loop as transmitter connected to Port 1, the other as receiver to Port 2) measures changes in transmission due to the coil's presence. The subtraction isolates the coil's effect by removing direct probe coupling and background noise.

## Tools 
- Rohde & Schwarz ZNL3 network analyzer. If using another VNA brand (e.g., Keysight), the steps are similar but use equivalent menu names.
- A double-loop probe pair
- Coil, DC power supply, etc.

## Check before
- Ensure all RF connections are secure using a torque wrench (e.g., $`1~\mathrm{N\cdot m}`$ for steel SMA connectors) to avoid signal loss or damage. 
- Do not exceed port power ratings (typically +27 dBm max input; check data sheet). 
- Power the VNA with a three-pronged outlet.

## Instructions
1. Power On and Preset the VNA. Press \[Preset\] to reset to default settings.
1. Set Measurement Parameters.
    1. Set the frequency range via \[Freq\] hard key.  Select "Lin Freq" sweep type (default; use "Log Freq" if needed for broad ranges). Enter Center Freq (e.g., 127.7 MHz).
    1. Press Span and set the span (e.g., 30 MHz) 
    1. Press \[Sweep\] and set Number of Points (e.g., 901 for better resolution).
    1. Set source power via \[Bw Avg Power\] hard key. Enter 0 dBm.
    1. Set IF bandwidth via \[Bw Avg Power\] → Bandwidth tab. Recommend 10 kHz. 
    1. Configure trace for S21 via \[Meas\] hard key. Via \[Format\], set to "Log Mag" for magnitude in dB (default).
    1. Via \[Scale\], enable "Auto Scale Trace" to fit the display.
    1. Optional but highly recommended: Enable averaging via \[Trace\] → "Average" tab, set averaging to 30.
1. Prepare the test setup. 
    - Connect the double-loop to Port 1 and Port 2 (receiver) via cables. 
    - Tighten all connections with a torque wrench. Ensure the entire setup (VNA, cables, probe, coil mount) is mechanically stable. 
    - Position the double-loop probe far enough from the coil under test (when placed) to minimize influence on coil performance (e.g., you must not see calibrated |S21| curve deform—you’ll find it out as you go on). Typically, start with 4 cm separation and adjust based on preliminary tests.
    - Simultaneously, keep the probe far enough from the sample (phantom). Especially, do not put the sample (phantom) between the coil and double-loops.
    - Avoid nearby metallic objects or EMI sources that could interfere.
1. Measure Background S21 (Without Coil). 
    - Remove the coil under test from the setup. Keep the sample in place if convenient (for better representation of loading effects); otherwise, remove both. 
    - Reset averaging by pressing \[BW Avg Trace\], go to “Average”, press “Restart”.
    - View the S21 trace. If needed, auto-scale via \[Scale\] → "Auto Scale Trace".
    - Save this as a memory trace for subtraction: Press \[Trace\] → "Traces" tab → "Memory" → "Data to Memory" (creates Mem_Trc1 from current data).
    - **Do not move the double-loop probe after this step**. Do not touch the cables connected to them.
1. Measure S21 with Coil.
    1. Put the coil under test back in the setup. If the sample was removed before, put it in as well. 
    1. Reset averaging by pressing \[BW Avg Trace\], go to “Average”, press “Restart”. 
1. Perform Subtraction to Get Calibrated S21.
    1. Use built-in trace math for complex subtraction: \[Trace\] → "Math" tab → "Math Definition" → Set to "Data - Mem". The result gets rid of the coil's effect. 
    1. Add markers via \[Mkr\] for key readings (e.g., peak search).
    1. Optionally, press \[File\] to export traces to CSV if you want it to be further processed on a computer.

## Troubleshooting Tips
Things seldom go wrong. That said, below are what I have seen in the past.
- If traces look wacky: 
    - Unfasten all connections. Clean the dust inside cable connectors. Fasten all connection again. Tighten all connections by torque wrench.
    - Check cable's |S11|, |S21|, |S22|. Should be |S11|, |S22| < -20 dB, |S21| or |S12| is around 0 dB. If not so, the cable is damaged; just get another cable. 
- If traces are noisy: 
    - Increase averaging by pressing \[BW Avg Power\].
    - Increase VNA power by pressing \[BW Avg Power\].
- Compression/distortion: 
    - If an amplifier is connected to the coil and powered on: reduce VNA power by pressing \[BW Avg Power\].
    - Put the double-loop probe a little farther away from the coil. 
- Consult the ZNL user manual (available on Rohde & Schwarz website) for SCPI commands if automating via remote control (e.g., LAN/GPIB).