# Evidence and Safety Gates

Read this reference before assigning a safety conclusion or proposing a calibration change.

## General gate

An exact change requires all of the following:

- a clearly identified operating phase and repeatable behavior;
- the required channels with credible units, calibration, timestamps, and sample rate;
- relevant configuration facts for this vehicle;
- evidence that the symptom is calibration-related rather than mechanical, electrical, sensor, or logging-related;
- a conservative stop condition and a follow-up log plan.

If any item is missing, give a verification step or bounded test plan instead of a tune value.

## Domain gates

### Lambda/fueling

For target-error conclusions, require valid wideband data and a valid target channel/table for the same operating cells. Account for sensor warm-up, fuel cut, transients, and possible misfire. AFR-to-lambda conversion additionally requires the AFR convention or fuel stoichiometry.

Target-relative lambda error may be reported as:

`lambda error = actual lambda - target lambda`

Positive is leaner than target; negative is richer. Report magnitude and duration, not a single extreme.

Do not recommend fuel-table changes while differential fuel pressure, injector capacity, sensor validity, or fuel composition is materially uncertain.

### Fuel pressure

Confirm sensor scaling, units, regulator/reference type, and pressure reference. Prefer logged differential fuel pressure when correctly configured. Otherwise derive it only from compatible absolute or gauge signals.

Establish a same-log low-load reference or a confirmed profile baseline. Report loaded average, minimum, sustained loss, percent change, RPM/MAP relationship, and sensor sampling limits. A progressive pressure loss as fuel demand rises is a supply-system investigation, not a fuel-table correction.

### Boost/load

Confirm whether the pressure channel is absolute or gauge and whether barometric pressure is logged. Compare to the vehicle's configured target/limit when supplied. Without those facts, report observed manifold pressure and control behavior but do not label the boost level acceptable for the build.

Never classify a free-rev as a loaded pull. Require corroborating TPS, MAP/MGP, RPM trend, and preferably gear or vehicle speed.

### Oil pressure

Confirm sensor scaling and units. Evaluate pressure against RPM and oil temperature. Coolant temperature is not oil temperature. Use builder/OEM limits when supplied; otherwise restrict conclusions to trends such as RPM tracking, sudden collapse, heat-related drift, or sensor implausibility.

A sudden sustained loss relative to the immediately preceding pressure at similar RPM/load warrants stopping the test and verifying mechanically, even when an absolute engine-specific limit is unavailable.

### Temperature

Use confirmed limits for coolant, oil, intake air, exhaust, or component protection. Without a confirmed limit, report the measured range and trend and request the relevant builder/OEM limit. Do not substitute a generic internet threshold.

### Ignition and knock

Ignition angle alone cannot prove combustion safety. A knock channel is usable only if it is configured, dynamic, and understood for this engine. If it is missing, static, disabled, or unvalidated, state: “Knock safety cannot be assessed from this log.”

Do not infer absence of knock from lambda, EGT, ignition angle, or engine sound descriptions. Do not recommend advancing timing without an appropriate controlled load test and validated knock/detonation monitoring.

### Injector capacity and electrical behavior

Interpret injector duty using the configured injection mode, channel definition, and operating strategy. Investigate values near the system's practical control limit, but do not assume a universal safe duty-cycle ceiling.

Report battery/ECU voltage sag and correlation with pressure, dwell, injector, or idle behavior. Compare against the vehicle profile or component requirements when available.

## Severity and confidence

Keep consequence and confidence separate. A potentially severe pattern with uncertain configuration should be labeled high consequence / limited confidence, followed by a cautious stop or verification instruction.

Escalate immediately when the log credibly shows any of the following in the captured range:

- sustained leaner-than-target operation under meaningful load;
- progressive or abrupt differential fuel-pressure loss under rising demand;
- abrupt sustained oil-pressure collapse relative to RPM;
- operation beyond a confirmed temperature, boost, RPM, or pressure limit;
- loss of injector control margin or severe ECU-voltage instability;
- repeated stalls or uncontrolled actuation that creates an immediate operating hazard.

Use “no obvious issue visible in this log” rather than “safe.” A log cannot verify unlogged knock, mechanical clearances, sensor truth, combustion quality, or behavior outside the captured range.
