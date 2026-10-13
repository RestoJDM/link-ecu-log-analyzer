# Onboarding and Profile Use

Read this reference when a vehicle profile is absent, incomplete, stale, or contradicted by the current user or log.

## Principle

The profile is a vehicle-specific evidence record, not a universal tune specification. It should distinguish confirmed facts, logged observations, inferred values, and unknowns. Never require every field before doing useful log analysis.

The bundled [profile template](../assets/link-ecu-vehicle-profile-template.md) is designed for persistent vehicle/build details. The [log-context template](../assets/link-ecu-log-context-template.md) captures facts that can change every session.

## Guided first-time onboarding

The user should not have to edit the template. When they ask for first-time setup, conduct a short conversation and generate `link-ecu-vehicle-profile.md` from their answers.

Open with a brief explanation such as:

> I’ll build the vehicle profile for you. I’ll ask a few questions at a time, and “unknown” is always acceptable. We can do a quick essentials setup or a more complete setup. You can update the generated profile later by talking to me.

When the host offers a native structured-question interface, use it for short choices and answers. Otherwise ask in ordinary chat. Never imply that a pop-up is guaranteed.

Offer these routes:

- **Quick setup** — collect the essentials needed to interpret common logs, then generate the profile.
- **Full setup** — continue into sensors, limits, idle, boost, oil, ignition, and known-good baselines.
- **Analyze first** — inspect an attached log now in unknown-configuration mode and offer setup afterward.

Ask no more than five concise questions in one turn. Combine closely related items, explain unfamiliar terms in one sentence, and do not re-ask facts already supplied. Accept approximate answers when precision is not safety-critical and mark their confidence accordingly.

### Round 1 — vehicle essentials

Ask for:

1. vehicle and engine, including displacement and important internal/cam changes;
2. naturally aspirated, turbocharged, or supercharged, plus relevant hardware if known;
3. Link ECU model (for example, the model/generation shown on the ECU or in PCLink);
4. fuel type or blend;
5. the main goal: idle/startup, fueling, boost pulls, oil pressure, general health, or another concern.

For quick setup, follow with only the task-relevant minimum from the sections below, then generate the profile.

### Round 2 — control strategy and sensors

Ask only what is relevant to the build and goal:

- fuel equation/load source and whether MAP/MGP is absolute or gauge;
- lambda versus AFR display convention;
- injector, pump, regulator, and base differential fuel pressure;
- pressure-sensor models, units, scaling, and reference;
- idle hardware/control mode;
- oil-pressure and oil-temperature sensing;
- knock setup and whether it has been validated for this engine.

If the user does not recognize a term, explain where it is commonly found in PCLink or suggest leaving it unknown. Do not turn onboarding into a tuning lesson.

Do not ask the user to upload a `.pclx`, `.pcl5`, `.pcl`, or other tune file. These proprietary tune files are not supported by this skill. Collect the Link ECU model and any relevant setting changes the user describes in plain language.

### Round 3 — targets and limits

Ask for only documented or deliberately configured references:

- idle target and relevant warm-up tables;
- lambda targets for the operating range they plan to analyze;
- boost target/cut and rev limit;
- builder/OEM oil-pressure and temperature limits;
- any tuner-specified constraints or settings that should not be changed.

Do not ask users to invent limits. Record the source/date when known; otherwise mark the field unknown.

### Round 4 — baselines and recent changes

Ask whether they have:

- a known-good log from the same build;
- a recent hardware, fuel, firmware, sensor, wiring, or ECU-setting change;
- a known issue that should be watched in every analysis;
- preferred report units.

Skip this round when the user chose quick setup and it is not needed for the immediate goal.

## Finish the setup

Before generating the file:

1. summarize the collected facts and call out any inference;
2. ask the user to correct only material misunderstandings;
3. place unanswered fields in the template as `Unknown` rather than deleting them;
4. add confidence/source notes for consequential targets and limits;
5. create `link-ecu-vehicle-profile.md` as a downloadable file or workspace artifact when supported;
6. if file creation is unavailable, provide the completed Markdown in a single reusable block and tell the user they can upload it with future logs;
7. briefly list the highest-impact unknowns, without making completion of them mandatory.

Tell the user they can update the profile conversationally, for example: “Update my profile: I changed to a different fuel-pressure sensor and here is its calibration.” Regenerate the file after confirmed changes so the user never has to hand-edit Markdown.

## Progressive onboarding

1. Start with the user's immediate question and inspect the available channels.
2. Ask only for facts that could change the answer or the safety of the next action.
3. Offer guided setup when the user wants repeatable future analysis.
4. Populate the profile from facts the user has already provided; do not make them re-enter known information or edit the template manually.
5. Mark unverified fields `Unknown`. Add a source and date to safety limits and known-good baselines.
6. Ask the user to confirm inferred facts before treating them as limits or tune specifications.

## High-value minimum by task

### Any task

- engine and major build changes;
- Link ECU model;
- fuel type;
- what changed since the last known-good result;
- channel units and whether pressure channels are absolute, gauge, or differential.

### Fueling or boost

- fuel stoichiometry/display convention if AFR rather than lambda is logged;
- injector model/flow reference and base differential fuel pressure;
- regulator type and manifold reference;
- MAP/MGP meaning, boost target/limit, wastegate strategy, and fuel-pressure sensor scaling;
- lambda target channel or the relevant target-table values;
- dyno/road context, gear, and fuel used.

### Oil pressure or temperature

- sensor model, scaling, and units;
- oil temperature channel or measured oil temperature;
- oil grade and relevant hardware changes;
- builder/OEM minimum pressure and maximum temperature references, if available.

### Idle, starting, or warm-up

- idle-control hardware and mode;
- idle target and base-position tables versus coolant temperature;
- closed-loop and ignition-idle modes/lockouts;
- initial coolant temperature, ambient conditions, and accessory loads;
- fuel and recent cold-start-related changes.

### Ignition or knock

- fuel, compression ratio, boost/load range, and base timing verification status;
- ignition hardware and dwell source;
- knock sensor/configuration status and whether the knock system is known to be calibrated for this engine;
- engine-builder or tuner limits. Do not invent generic knock thresholds.

## Updating profiles

When hardware, fuel, firmware, sensor calibration, or ECU settings change:

- preserve the old value in a short change-history entry when it affects comparisons;
- mark old known-good logs as non-comparable if the change materially alters the signal;
- do not overwrite a confirmed builder limit with an inferred value;
- note whether relevant ECU settings changed before future comparison logs.

If two sources disagree, show the conflict and use neither as an authoritative limit until resolved.
