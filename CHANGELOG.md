# Changelog

All notable changes to this catalogue are documented here.

## [0.9.3] - 2026-10-18

### Fixed

- Use the scoped `@voicetel.com/voiceml` npm import and pass Go call parameters by value, with a complete context/error-handling example.
- Document C# source and explicit local-feed installation while `VoiceML` is unavailable on nuget.org.
- Replace obsolete operation totals and resource lists with release-aware coverage, including Pricing, SIP trunking, Conversations, Messaging Services, Voice v1, Routes v2 and Assistants.
- Identify unsupported list/fetch GETs under `/2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/{Streams,Siprec,Transcriptions}[/{Sid}].json` (HTTP 405 / API code 20004); their SDK removal is pending release. POST start/stop operations remain supported.
- Distinguish SDK v0.9.2 releases from the catalogue v0.9.1 release, registry availability, lagging collections/CLI releases and pending source fixes.

### Added

- Go and TypeScript quickstart compilation checks and read-only registry checks in CI, including a scheduled drift check.

### Security

- Direct npm usage to the official scoped package and C# installation to an explicitly selected local feed.
- Clarify that VoiceML requires VoiceML-issued credentials; Twilio-issued credentials do not work.

### Docs

- Refresh repository/reference links, migration wording, transport descriptions and fictional phone numbers.
- Correct licence information: the catalogue, Ruby and Swift use MIT; the other six SDK repositories carry MIT with Commons Clause terms. No licence texts changed.
- Mark new operations and transport/model/webhook fixes as unreleased rather than attributing them to existing registry packages.
