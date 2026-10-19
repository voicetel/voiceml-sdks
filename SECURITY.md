# Security Policy

## Reporting a Vulnerability

This repository is the catalogue for the VoiceML SDK family — its
ships documentation, not an SDK package. Repository verification scripts
compile examples and check public registry metadata; they do not call the API.

For vulnerabilities in **any of the SDK repos** (Go, Python,
TypeScript / Node, Java, C#, Ruby, PHP, Swift) or the **CLI** or
**Collections** repos, please report them privately on the affected
repository:

| Surface | Report |
| ------- | ------ |
| 🐹 Go SDK | <https://github.com/voicetel/voiceml-go-sdk/security/advisories/new> |
| 🐍 Python SDK | <https://github.com/voicetel/voiceml-python-sdk/security/advisories/new> |
| 🟦 TypeScript / Node SDK | <https://github.com/voicetel/voiceml-node-sdk/security/advisories/new> |
| ☕ Java SDK | <https://github.com/voicetel/voiceml-java-sdk/security/advisories/new> |
| 🟪 C# / .NET SDK | <https://github.com/voicetel/voiceml-csharp-sdk/security/advisories/new> |
| 🐘 PHP SDK | <https://github.com/voicetel/voiceml-php-sdk/security/advisories/new> |
| 💎 Ruby SDK | <https://github.com/voicetel/voiceml-ruby-sdk/security/advisories/new> |
| 🦅 Swift SDK | <https://github.com/voicetel/voiceml-swift/security/advisories/new> |
| 🔧 CLI | <https://github.com/voicetel/voiceml-cli/security/advisories/new> |
| 📦 Collections | <https://github.com/voicetel/voiceml-api-collections/security/advisories/new> |

For a cross-cutting issue that affects every SDK (spec drift,
shared model defect), file the private advisory against whichever
SDK first reproduces the issue and we will fan it out to the others.

For ordinary content issues (broken links, stale version references), open
a regular public issue. For a security-sensitive catalogue issue, such as
an install command pointing to an unexpected package or credentials exposed
in an example, use this repository's private reporting form:
<https://github.com/voicetel/voiceml-sdks/security/advisories/new>.

## Package identity

- The official npm package is `@voicetel.com/voiceml`.
- The official NuGet package is `VoiceML`, owned by the `voicetel`
  organization on nuget.org and published from voicetel/voiceml-csharp-sdk.
  Treat similarly named packages from other owners as unofficial.
- VoiceML authentication requires a VoiceML AccountSid and API key.
  Twilio-issued credentials do not authenticate with VoiceML.

For SDK security support, consult the affected repository's policy; the
current supported SDK release line is `0.9.x`. The CLI uses its own version
line. Catalogue corrections are maintained on `main`.
