# Link ECU Log Analyzer

A reusable Codex/Agent Skill for analyzing Link ECU and PCLink `.llgx` logs across different engines, vehicles, fuels, sensors, and calibration strategies.

The skill quantifies log behavior first, uses vehicle-specific references when available, and deliberately limits its conclusions when configuration or safety information is unknown. It does not ship with targets or thresholds copied from a particular engine build.

## What it analyzes

- cranking, post-start, cold start, and warm-up;
- settled idle and throttle-return recovery;
- lambda/AFR behavior and target tracking;
- loaded pulls, MAP/boost, and boost-control behavior;
- rail and differential fuel pressure;
- oil pressure relative to RPM and oil temperature;
- injector usage, ignition, knock-channel validity, and ECU voltage;
- comparisons with a known-good log from the same build.

Analysis depends on the channels actually logged. A missing or unvalidated signal is reported as a limitation rather than replaced with an assumed value.

## Install

The ZIP contains one top-level `link-ecu-log-analyzer` folder. Import the ZIP using your host's skill interface, or extract that folder into a skills directory recognized by your Codex/Agent Skills environment. Keep `SKILL.md`, `scripts/`, `references/`, and `assets/` together.

For OpenAI-hosted skill upload and API integration, see the [official Agent Skills documentation](https://developers.openai.com/api/docs/guides/tools-skills).

The parser uses only the Python standard library and has no third-party package requirements.

## First-time guided setup

Users do not need to open or edit the profile template. Start with:

> Use the `link-ecu-log-analyzer` skill to guide me through first-time vehicle setup and create my profile.

The skill asks a few plain-language questions at a time. `Unknown` and `Skip` are valid answers. Users can choose:

- **Quick setup** for the essentials relevant to their immediate goal;
- **Full setup** for sensors, control strategies, documented limits, and known-good baselines;
- **Analyze first** to inspect a log immediately and complete setup later.

At the end, the skill creates a completed `link-ecu-vehicle-profile.md` file. The user can save and attach that file with future logs. Updates can also be conversational—for example, “Update my profile with this new fuel-pressure sensor calibration”—and the skill will regenerate the file.

## Quick start

1. Install or attach the skill.
2. Run guided setup, or upload a Link ECU `.llgx` log and choose **Analyze first**.
3. Tell the agent what was happening and what you want checked.
4. Attach the generated vehicle profile with later logs when it is not already available to the conversation or project.

Example prompt:

> Use the `link-ecu-log-analyzer` skill to inspect this `.llgx` file. Check the third-gear pull for lambda target error, differential fuel-pressure loss, injector margin, boost control, temperatures, oil pressure, and ECU voltage. My vehicle profile and log context are attached.

Without a vehicle profile, the skill still reports channel coverage, trends, event timing, correlations, target tracking, and relative changes. It will not invent engine-specific limits or unsupported tuning values.

## Vehicle onboarding

Guided setup fills [`assets/link-ecu-vehicle-profile-template.md`](assets/link-ecu-vehicle-profile-template.md) for the user. Manual editing remains available but is not required. Unknown answers remain `Unknown`.

High-value details include:

- engine/build, intended use, fuel, and Link ECU model;
- relevant ECU-setting changes since the last good log;
- sensor models, scaling, units, and absolute/gauge/differential pressure references;
- injector, pump, regulator, wastegate, and boost-control configuration;
- idle targets/control modes and warm-up configuration;
- confirmed builder/OEM pressure, temperature, RPM, and boost limits;
- validated knock configuration and base-timing verification status;
- known-good measurements from comparable logs on the same build.

Use [`assets/link-ecu-log-context-template.md`](assets/link-ecu-log-context-template.md) for details that change each session, such as fuel blend, ambient conditions, start temperature, test type, gear, recent setting changes, and driver observations.

The skill does not request or read `.pclx`, `.pcl5`, `.pcl`, or other Link tune files. Users only need to identify the Link ECU model and describe relevant setting changes when known.

You do not need to complete every field before using the skill. The analyzer asks only for missing information that could materially change the requested conclusion.

## Example requests

- “Check this cold start and tell me whether the RPM sag is airflow, ignition, or fueling related.”
- “Compare this warm-up log with my last known-good log by coolant-temperature region.”
- “Analyze these loaded pulls for lambda error, fuel-pressure loss, injector margin, boost, and voltage.”
- “Check oil pressure versus RPM and oil temperature. Use the builder limits in my profile.”
- “My setup details are incomplete. Analyze what the log proves and list what must be verified before changing the tune.”

## How unknown configurations are handled

The skill marks important facts as confirmed, observed, inferred, or unknown. With incomplete configuration it favors relative evidence—such as target error, pressure drop, RPM variability, voltage sag, and repeatable event timing—and explains which missing fact prevents a stronger conclusion.

It will not:

- reuse another vehicle's fuel, boost, oil-pressure, temperature, idle, or ignition values;
- convert AFR to lambda without knowing the fuel/display convention;
- confuse rail pressure with differential fuel pressure;
- treat coolant temperature as oil temperature;
- treat an absent or static knock channel as evidence of no knock;
- recommend tuning around a likely mechanical, electrical, sensor, or fuel-supply fault;
- declare an engine completely safe from one log.

## Output format

Reports normally include:

1. a short verdict;
2. profile coverage and important unknowns;
3. quantified findings;
4. concerns ranked by consequence and confidence;
5. actions separated into **CHANGE**, **VERIFY FIRST**, **KEEP / LOCK IN**, and **WATCH**;
6. missing channels and other limitations.

## Package structure

```text
link-ecu-log-analyzer/
├── LICENSE
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── link-ecu-log-context-template.md
│   └── link-ecu-vehicle-profile-template.md
├── references/
│   ├── analysis-playbook.md
│   ├── evidence-and-safety-gates.md
│   └── onboarding-and-profile-use.md
└── scripts/
    └── parse_llgx.py
```

## Troubleshooting

- **“No ds3 channels found”** — the file may be incomplete, not an `.llgx` log, or produced by an unsupported format revision.
- **Channels are missing** — enable the relevant parameters in PCLink logging and capture the event again.
- **Values or units are implausible** — verify sensor calibration, units, pressure reference, duplicated channel occurrences, and file-format compatibility before interpreting the data.
- **The report cannot judge a limit** — add the applicable builder/OEM limit, target-table value, sensor reference, or same-build baseline to the vehicle profile.

The parser reflects an observed PCLink `ds3` layout and may need updates for future format revisions.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 RestoJDM.

## Safety

This skill is an analysis aid, not a substitute for a qualified tuner, engine builder, mechanical pressure gauge, verified sensor calibration, or controlled dyno safety process. Do not repeat a pull or continue running an engine when the log or physical symptoms indicate a credible fuel-pressure, oil-pressure, temperature, detonation, electrical, or control hazard.
