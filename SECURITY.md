# Security Policy

## Reporting a Vulnerability

This repository is the catalogue for the VoiceML SDK family — its
content is documentation (`README.md`, `LICENSE`) only; there is no
executable code shipped from this repo.

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

For issues in this catalogue's own content (broken links, stale
version references) please open a regular public issue — those are
documentation defects, not security ones.
