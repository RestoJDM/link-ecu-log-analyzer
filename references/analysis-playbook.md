# Analysis Playbook

Use only the sections relevant to the user's scenario plus a basic audit of fueling, pressures, temperatures, injector margin, and ECU voltage over the operating range actually captured.

## Channel inventory and quality

Inventory engine speed, ECT, IAT, MAP/MGP/barometric pressure, TPS, lambda/AFR actual and target, ignition, idle controls, enrichments, fuel pressure, oil pressure/temperature, injector duty/pulse width, boost control, knock, battery/ECU voltage, gear, speed, and status channels when present.

For each selected signal check:

- units and pressure reference;
- sample count, time range, median sample interval, and gaps;
- duplicate channel occurrences;
- static, clipped, impossible, or discontinuous values;
- whether an enable/status/readiness channel changes its interpretation.

## Cranking and start

Detect cranking from low nonzero RPM, starter/start status, voltage drop, crank enrichment, and fuel-pressure buildup. Do not use a universal cranking-RPM threshold when the profile provides one. If logging begins after firing, say cranking was not captured.

For post-start behavior, inspect the transition from cranking to sustained running rather than relying on a fixed time window. Measure flare, sag, stall/restart, target error, airflow control, ignition response, enrichment, fuel pressure, and lambda only after sensor readiness.

## Warm-up

Analyze primarily by ECT and phase, not elapsed time. Use bins narrow enough to expose a transition but large enough to contain representative samples; 1–5 °C bins are often useful and are not a requirement.

Report sample count, lambda distribution, RPM/target error, idle/base position, enrichment, MAP, ignition, and voltage in the relevant bins. Pay attention to repeated changes across adjacent temperature regions and separate accessory/load events from calibration effects.

## Settled idle

Select windows with closed throttle, stable operating conditions, no deliberate blip, and status/lockouts consistent with idle control. Define “warm” from the profile; if unavailable, use an ECT plateau only as an explicitly labeled heuristic.

Calculate mean/median RPM, standard deviation, robust range such as 5th–95th percentile, target error, lambda distribution, MAP, idle position versus base, ignition response, differential fuel pressure, and ECU voltage. Determine whether closed-loop control is active, saturated, locked out, or simply near base.

Do not change fueling to correct an airflow/control problem unless mixture evidence is causal. If correction is at a control limit, verify mechanical airflow and lockouts before moving more table cells.

## Throttle return

Detect deliberate throttle/RPM excursions followed by closed throttle and idle re-entry. For each clean event report peak RPM, minimum recovery RPM, overshoot/undershoot relative to target, time to enter and remain in an appropriate target band, idle position, ignition, lambda, MAP, and status/lockout transitions.

Choose target bands relative to idle target and sample rate. Values such as ±50 or ±100 rpm may be convenient reporting bands, not universal quality limits. Separate fuel cut and transient wideband behavior from stable idle mixture.

## Loaded pulls and boost control

Require a meaningful load event supported by TPS, MAP/MGP, RPM acceleration, and preferably gear/speed. For each pull report the captured RPM/load range, peak pressure with reference, boost target/error when valid, lambda target/error, injector duty/pulse width, fuel-pressure behavior, voltage, IAT/ECT, oil pressure/temperature, ignition, and usable knock data.

Evaluate the whole event and duration. Do not judge a pull by a lone sample. Identify shifts, lift, overrun, control transitions, and sensor dropouts separately.

## Lambda events

Group adjacent samples into events using timestamp-aware logic. For each event report duration, actual versus target, RPM/load/ECT, MAP/TPS trend, and coincident RPM roughness or pressure change. Very lean readings during deceleration fuel cut are expected. A simultaneous lambda spike and RPM disturbance can reflect misfire oxygen rather than insufficient commanded fuel.

## Fuel pressure

For a confirmed manifold-referenced system, prioritize differential pressure. Compare low-load reference with loaded average/minimum and quantify sustained loss in pressure units and percent. Correlate with RPM, load, injector demand, pump command, and ECU/pump voltage where available.

Possible causes of demand-related loss include pump voltage/wiring/ground, pickup or in-tank plumbing, restriction, pump condition/capacity, regulator/reference plumbing, and sensor calibration. Rank them only when evidence distinguishes them; otherwise provide a verification order.

## Oil pressure

Plot or bin pressure versus RPM and oil temperature. Look for normal RPM tracking, sudden collapse at similar RPM, heat-related drift, near-stall artifacts, relief behavior, and sensor dropout. Never infer oil temperature from coolant temperature.

## Comparison logs

Confirm comparability before computing a delta: same vehicle/build, fuel, sensor scaling, ECU-settings state, operating phase, and similar environmental/load conditions. If not comparable, explain the confounder.

Align phases or RPM/load cells rather than raw elapsed time. Report material deltas with sample coverage and avoid treating normal run-to-run noise as a calibration result.
