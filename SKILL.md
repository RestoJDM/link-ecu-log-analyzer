---
name: link-ecu-log-analyzer
description: Analyze Link ECU / PCLink .llgx logs for idle, starting, warm-up, fueling, boost, pressure, ignition, electrical, and general engine behavior. Use a vehicle-specific profile when available and switch to evidence-limited analysis when configuration or safety limits are unknown.
---

# Link ECU Log Analyzer

## Purpose

Quantify what a Link ECU log demonstrates, separate observations from configuration-dependent judgments, and recommend the smallest defensible next step. Prioritize the user's scenario while always performing a proportionate safety scan of the captured operating range.

Never apply settings, thresholds, or known-good values from a different engine or vehicle.

## Evidence order

Use evidence in this order:

1. the current log and the user's current description;
2. a current, confirmed vehicle profile;
3. known-good logs from the same hardware, fuel, calibration, and sensor setup;
4. documented engine-builder, component-manufacturer, or OEM limits supplied for this vehicle;
5. generic mechanical patterns, clearly labeled as heuristics rather than pass/fail limits.

New user information overrides stale profile content. Record the date and source of consequential profile updates.

## Start every analysis

1. Identify the requested scenario, relevant changes since the last good log, and the conditions captured.
2. Look for a supplied vehicle profile. Common names include `link-ecu-vehicle-profile.md`, `vehicle-profile.md`, and files created from the bundled template.
3. Parse the `.llgx` file with `scripts/parse_llgx.py` and inventory all channels, units, occurrences, time ranges, and sample counts before choosing signals.
4. Resolve channel names semantically; Link firmware, ECU configuration, and user labels vary.
5. Determine whether the task is profile-supported, same-build comparison, or unknown-configuration analysis.

If the user says this is their first time, asks to set up a profile, or invokes the skill without a log and profile, start guided onboarding. The user must not need to open or edit the Markdown template. Ask a small group of plain-language questions at a time, accept `Unknown` or `Skip`, adapt later questions to the build and intended analysis, and create the completed profile file for the user. Ask which Link ECU model they have, but do not request or claim to read a `.pclx`, `.pcl5`, `.pcl`, or other tune file. Use a native structured-question interface when the host provides one; otherwise conduct the same flow in chat. Read and follow [references/onboarding-and-profile-use.md](references/onboarding-and-profile-use.md).

If a user supplies a log without a profile and wants immediate analysis, continue with observations that the data supports; do not block useful results behind onboarding. Ask only for missing facts that materially affect the requested conclusion, then offer guided onboarding for future logs.

If parsing fails or metadata is implausible, state that the file may use an unsupported PCLink format revision. Do not analyze decoded values that have not passed basic time, unit, and plausibility checks.

## Configuration confidence

Treat each important fact as one of:

- **confirmed** — supplied by the user or authoritative build documentation;
- **observed** — directly present in the current log or ECU export;
- **inferred** — a reasoned interpretation that still needs confirmation;
- **unknown** — unavailable or ambiguous.

Unknown is an acceptable value. Do not silently fill profile gaps with typical values.

### Unknown-configuration mode

When configuration is incomplete:

- report channel availability, units, operating phases, trends, correlations, repeatability, and target-tracking where both actual and target are logged;
- use relative findings such as pressure change, percent drop, RPM variability, target error, or voltage sag;
- identify impossible or ambiguous measurements as sensor/configuration questions;
- replace exact calibration changes with verification steps or a bounded test plan;
- avoid declaring engine-specific temperatures, pressures, boost, AFR/lambda, ignition timing, or idle speeds safe/unsafe without a confirmed reference;
- say exactly which missing fact prevents the stronger conclusion.

## Units and signal meaning

Confirm meaning before calculating:

- MAP may be absolute pressure, gauge pressure, or manifold gauge pressure; use logged barometric pressure when converting.
- AFR depends on fuel stoichiometry. Prefer lambda. Convert AFR to lambda only when the displayed AFR convention or stoichiometric value is known.
- Fuel rail pressure is not differential fuel pressure. For a manifold-referenced regulator, calculate rail pressure minus manifold pressure only after confirming both pressure references and units.
- Oil, fuel, and manifold pressure channels may use kPa, bar, psi, or a custom calibration.
- A static knock channel may be disabled, unconfigured, filtered incorrectly, or simply not sampled. It is not evidence of no knock.
- A lean wideband reading during fuel cut or misfire is not proof of lean combustion.

Preserve original units in reported evidence. If converting, show the conversion and avoid false precision.

## Time alignment

Channels may have different sample rates. Compare signals by timestamp using nearest valid sample or last observation carried forward. Use a maximum gap appropriate to the observed sample cadence and event duration; never assume array indices align and never bridge a gap large enough to hide the event being examined. Keep the original high-rate signal for brief events and disclose sparse sampling.

## Analysis routing

Read [references/analysis-playbook.md](references/analysis-playbook.md) for phase detection, metrics, and scenario-specific analysis.

Before making a safety assessment or recommending a calibration change, read [references/evidence-and-safety-gates.md](references/evidence-and-safety-gates.md).

## Recommendation standard

Prefer the smallest change supported by repeatable evidence. Normally change one variable at a time. Multiple changes are reasonable only when they affect clearly separate operating phases.

For each proposed calibration change state:

- the observed behavior and supporting measurements;
- the relevant profile/configuration facts and their confidence;
- the exact table, axis region, or setting when known;
- a conservative value or range only when the evidence gate is satisfied;
- the expected effect and a rollback or stop condition;
- what to leave unchanged;
- what the next controlled log must confirm.

Do not tune around a suspected mechanical, electrical, fuel-supply, sensor, or synchronization fault. Do not recommend advancing ignition timing from a road log without an appropriate knock-validation and load-testing process.

## Default report

### Verdict

Give the main conclusion in 1–3 sentences using calibrated language. Never claim an engine is completely safe from one ECU log.

### Profile coverage

Briefly list the configuration facts used, important unknowns, and how those unknowns limit the conclusion.

### Quantified findings

Use a compact table of the measurements that matter to the scenario. Distinguish logged facts from derived values.

### Concerns

Rank demonstrated concerns by consequence and confidence. Do not manufacture concerns to fill the section.

### Recommendation

Separate actions into:

- **CHANGE** — sufficiently supported calibration changes;
- **VERIFY FIRST** — configuration, sensor, mechanical, or test information needed before changing the tune;
- **KEEP / LOCK IN** — behavior shown to be working for this vehicle;
- **WATCH** — items worth trending in the next comparable log.

### Limitations

State missing channels, uncaptured phases, uncertain units/references, sparse sampling, and any safety domain the log cannot assess.

Use language such as: “No obvious fueling, pressure, temperature, or oil-pressure problem is visible in the operating range captured, subject to the limits above.”
