# 🎙️ VoiceML SDKs

Official client libraries for the [VoiceML REST API](https://voicetel.com/docs/api/v0.8/voiceml/) — VoiceTel's voice + SMS + AMD service with a **Twilio-compatible wire format**. Eight languages, all hand-written, all MIT-licensed, all public.

![API](https://img.shields.io/badge/API-v0.8.1-blue)
![Compatibility](https://img.shields.io/badge/Twilio--compatible-wire%20format-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![SDKs](https://img.shields.io/badge/SDKs-8-brightgreen)

## 📚 Table of Contents

- [Why VoiceML](#-why-voiceml)
- [Pick your language](#-pick-your-language)
- [Releases](#-releases)
- [What every SDK gives you](#-what-every-sdk-gives-you)
- [API Documentation](#-api-documentation)
- [Authentication, in 30 seconds](#-authentication-in-30-seconds)
- [Resource groups](#-resource-groups)
- [Twilio drop-in](#-twilio-drop-in)
- [Versioning](#-versioning)
- [Contributing](#-contributing)
- [License](#-license)

## 💡 Why VoiceML

VoiceML is VoiceTel's voice + SMS + AMD (answering-machine detection) service. The REST surface is **wire-compatible with Twilio's Programmable Voice and Messages APIs** (the `2010-04-01` namespace): the same path layout (including the canonical `.json` suffix), the same auth model, the same error codes, the same pagination envelope. Existing Twilio SDKs can point at `https://voiceml.voicetel.com` and work as drop-in replacements.

These SDKs are written separately — they ship VoiceML-specific extensions (real-time transcription engines, per-call SIPREC and `MZ`-prefixed audio forks, `Conference.member_count`, REST-side `<Pay>` session control), don't carry Twilio's full surface (no Studio / Flex / Verify), and give you native error types in each language. Pick your language, install, and you're done.

## 🎯 Pick your language

Each row links straight to the SDK repo. All eight cover the same **128 operations** across the resource groups listed in [voiceml-api-collections](https://github.com/voicetel/voiceml-api-collections).

| Language | Repo | Install | Idiomatic style |
|---|---|---|---|
| 🐍 **Python** | [voiceml-python-sdk](https://github.com/voicetel/voiceml-python-sdk) | `pip install voiceml` | `Client` + `AsyncClient`, Pydantic v2, httpx |
| 🟦 **TypeScript / Node** | [voiceml-node-sdk](https://github.com/voicetel/voiceml-node-sdk) | `npm install @voicetel.com/voiceml` | ESM + CJS, async-only, `fetch`-based, zero runtime deps |
| 🐹 **Go** | [voiceml-go-sdk](https://github.com/voicetel/voiceml-go-sdk) | `go get github.com/voicetel/voiceml-go-sdk` | `context.Context`, stdlib `net/http`, zero deps |
| ☕ **Java** | [voiceml-java-sdk](https://github.com/voicetel/voiceml-java-sdk) | `com.voicetel:voiceml:0.8.1` | Java 11, `java.net.http`, Jackson, builders |
| 🟪 **C# / .NET** | [voiceml-csharp-sdk](https://github.com/voicetel/voiceml-csharp-sdk) | `dotnet add package VoiceML` | net8.0, `async/await`, `System.Text.Json`, zero NuGet deps |
| 🐘 **PHP** | [voiceml-php-sdk](https://github.com/voicetel/voiceml-php-sdk) | `composer require voicetel/voiceml` | PHP 8.1+, Guzzle 7, typed enums, PSR-4 |
| 💎 **Ruby** | [voiceml-ruby-sdk](https://github.com/voicetel/voiceml-ruby-sdk) | `gem install voiceml` | Ruby 3.0+, stdlib `Net::HTTP`, kwargs, zero gem deps |
| 🦅 **Swift** | [voiceml-swift](https://github.com/voicetel/voiceml-swift) | SwiftPM: `https://github.com/voicetel/voiceml-swift` | Swift 5.9, `async throws`, `URLSession`, iOS/macOS/tvOS/watchOS/Linux |

## 🏷️ Releases

Latest **released** tag is **v0.8.1** across all 8 SDKs. v0.8.0 introduced the Twilio-compatible SIP Trunking surface (Domains, CredentialLists, IpAccessControlLists, Domain↔mapping bindings) and v0.8.1 adds Twilio's routes/v2 Inbound Processing Region API (`/v2/SipDomains/{name}`).

| Language | Latest release | All releases |
|---|---|---|
| 🐍 Python | [v0.8.1](https://github.com/voicetel/voiceml-python-sdk/releases/tag/v0.8.1) | [history](https://github.com/voicetel/voiceml-python-sdk/releases) |
| 🟦 TypeScript / Node | [v0.8.1](https://github.com/voicetel/voiceml-node-sdk/releases/tag/v0.8.1) | [history](https://github.com/voicetel/voiceml-node-sdk/releases) |
| 🐹 Go | [v0.8.1](https://github.com/voicetel/voiceml-go-sdk/releases/tag/v0.8.1) | [history](https://github.com/voicetel/voiceml-go-sdk/releases) |
| ☕ Java | [v0.8.1](https://github.com/voicetel/voiceml-java-sdk/releases/tag/v0.8.1) | [history](https://github.com/voicetel/voiceml-java-sdk/releases) |
| 🟪 C# / .NET | [v0.8.1](https://github.com/voicetel/voiceml-csharp-sdk/releases/tag/v0.8.1) | [history](https://github.com/voicetel/voiceml-csharp-sdk/releases) |
| 🐘 PHP | [v0.8.1](https://github.com/voicetel/voiceml-php-sdk/releases/tag/v0.8.1) | [history](https://github.com/voicetel/voiceml-php-sdk/releases) |
| 💎 Ruby | [v0.8.1](https://github.com/voicetel/voiceml-ruby-sdk/releases/tag/v0.8.1) | [history](https://github.com/voicetel/voiceml-ruby-sdk/releases) |
| 🦅 Swift | [v0.8.1](https://github.com/voicetel/voiceml-swift/releases/tag/v0.8.1) | [history](https://github.com/voicetel/voiceml-swift/releases) |

Highlights since the v0.4.0 initial release:
- **v0.5.0** — `.json` URL suffix on every path; `IncomingPhoneNumbers` resource + `Capabilities` sub-struct; `auth_token` / `authToken` constructor alias; `more_info` typed accessor on the error class.
- **v0.6.0** — Twilio-compatibility fixes: `IncomingPhoneNumber` full Twilio field set, `RecordingStatus` drops `failed`/adds `deleted`, `ConferenceStatus` adds `init`, `voice_method`/`voice_fallback_method` tightened to `[GET, POST]`.
- **v0.6.1** — spec tag-taxonomy sync (codegen metadata, no functional change).
- **v0.6.2** — `Recording.media_url` (D5) + `IncomingPhoneNumber.type` (D6) — closes the last two Twilio-compatible field gaps.
- **v0.6.3** — Participant coaching fields (`coaching`, `call_sid_to_coach`, `queue_time`); `Recording.error_code`; Twilio-exact LIST filter params (`StartTime`/`EndTime`/`DateCreated` triples); queue `MaxSize=0` unlimited default; expanded enum coverage; `StartConferenceRecordingAPI` recording source.
- **v0.6.4** — `PageToken` cursor pagination on all list endpoints.
- **v0.6.6** — `POST /Conferences/{sid}/Participants` (dial-in); account + call notification compat stubs; conference-scoped recording fetch/update/delete; typed IncomingPhoneNumber list/create (`Local`/`Mobile`/`TollFree`); accept-but-no-op list filters (`Log`, `MessageDate`, conference date filters, `IncludeSoftDeleted`).
- **v0.6.6.1** — TLS session-ticket caching (Go) and persistent connections (Ruby); typed status enums (Java/C#/PHP); pagination iterators on Conferences / Recordings / Queues across every SDK; vitest 4.x security bump for TypeScript.
- **v0.7.0** — **SMS support** via the new `/Messages` resource (Twilio-compatible: send, fetch, list with To / From / DateSent filters, body redaction, delete) and the **`<Pay>` REST companion** at `POST /Calls/{sid}/Payments[/{sid}]` (start a Pay session on a live call, advance via `Capture=...`, terminate via `Status=complete|cancel`). Per-tenant Stripe BYO. Operation count: 74 → 81 across 8 resource families.
- **v0.7.1** — Null bugfix. Fleet-wide README parity refresh — every SDK README now follows the same emoji-decorated structure (Features → Installation → Quickstart → Authentication → Resource Reference → Errors → Async / Pagination → Migration → Rate Limits → Dev → Docs → Contributors → Sponsors → License) with verified version, test count, and resource list per language. No functional changes.
- **v0.7.1.1** — Lockstep fix on Python / PHP / Go / Ruby / Swift. The v0.7.1 release left runtime `VERSION` constants at `0.7.0` in five SDKs; this round brings the constant, package metadata, and smoke-test pin into lockstep at `0.7.1.1` on every SDK whose registry accepts a 4-segment version. TypeScript / Java / C# stayed at v0.7.1 (npm semver-2 + missing publish credentials).
- **v0.8.0** — **SIP Trunking** added: `/SIP/Domains` (CRUD), `/SIP/CredentialLists` + `/Credentials` (CRUD), `/SIP/IpAccessControlLists` + `/IpAddresses` (CRUD), and Domain↔ACL/CredentialList mappings under three namespaces (historical, `/Auth/Calls/`, `/Auth/Registrations/`). 45 new operations across 6 sub-resources; spec operation count 81 → 126. Python / TypeScript / Go / Java / PHP shipped at v0.8.0; C# / Ruby / Swift skipped straight to v0.8.1.
- **v0.8.1** — **Routes V2 Inbound Processing Region API** added: `GET` / `POST /v2/SipDomains/{name}` for setting a SIP domain's voice region (Twilio's routes/v2 namespace, keyed by domain name with the account resolved from HTTP Basic auth). 2 new operations; spec operation count 126 → 128. Shipped uniformly across all 8 SDKs.

## 🛠️ Tooling

| Tool | Repo | Purpose |
|---|---|---|
| **CLI** | [voiceml-cli](https://github.com/voicetel/voiceml-cli) | Interactive REPL + `-x` one-shot commands against the VoiceML API |
| **Collections** | [voiceml-api-collections](https://github.com/voicetel/voiceml-api-collections) | Postman v2.1 + Bruno collections for all 128 operations |

## ✨ What every SDK gives you

- **Strongly typed end-to-end** — every request body and response payload is a typed struct / class / record in the host language.
- **Twilio-compatible wire format** — the same `2010-04-01/Accounts/{AccountSid}/...` paths (with `.json` suffix), the same HTTP Basic auth, the same `{code, message, more_info, status}` error envelope. If you're migrating from `twilio-python` / `twilio-node` / etc., the constructor signature is the same (`auth_token` / `authToken` alias supported alongside `api_key` / `apiKey`).
- **Auto-retry on 429 / 5xx** with `Retry-After` honored, exponential backoff capped at 8 s. Default `maxRetries = 2`.
- **Structured errors** — every SDK exposes an `ApiError` (or equivalent) plus status-keyed subclasses: `AuthenticationError` (401), `NotFoundError` (404), `ConflictError` (409), `GoneError` (410), `RateLimitError` (429), `NotImplementedAPIError` (501), `ServerError` (5xx). The `.more_info` / `.MoreInfo` accessor surfaces Twilio's docs URL on every error. Catch broadly or pattern-match.
- **Form-urlencoded by default**, JSON-body acceptance documented — matches Twilio's wire convention exactly.
- **Booleans as `"true"` / `"false"` strings** — what Twilio sends; what every SDK here sends.
- **Cursor-style pagination** — `next_page_uri` / `previous_page_uri` honored; Python and TypeScript include an `iterate()` helper for `/Calls`.
- **Recording audio fetch** — `recordings.get_audio(sid)` transparently follows the 302 → S3 presigned-URL redirect; you get the WAV bytes regardless of where they were served from.
- **Zero codegen footprint** — every line is hand-written. No Swagger Codegen artifacts, no auto-generated method names like `accountsAccountSidCallsGet`.

## 📖 API Documentation

- **Reference docs:** [voicetel.com/docs/api/v0.8/voiceml/](https://voicetel.com/docs/api/v0.8/voiceml/)
- **Validator:** [voicetel.com/voiceml/validator/](https://voicetel.com/voiceml/validator/)
- **SDK catalogue:** [voicetel.com/docs/voiceml-sdks/](https://voicetel.com/docs/voiceml-sdks/)

## 🔑 Authentication, in 30 seconds

VoiceML uses **HTTP Basic auth** — the same shape Twilio uses:

- **Username** = your `AccountSid` (Twilio format: literal `AC` + 32 hex chars)
- **Password** = your per-tenant API key (or `auth_token` if you're using the Twilio-compat alias)

The same value the Twilio SDK validates in its constructor is what you pass to the VoiceML SDK.

```python
# Python
from voiceml import Client
from voiceml.models import CreateCallRequest

with Client(account_sid="AC…", api_key="…") as c:
    call = c.calls.create(CreateCallRequest(
        To="+18005551234", From="+18005550000", Url="https://example.com/twiml",
    ))
```

```ts
// TypeScript / Node
import { Client } from 'voiceml';

const c = new Client({ accountSid: 'AC…', apiKey: '…' });
const call = await c.calls.create({
  To: '+18005551234', From: '+18005550000', Url: 'https://example.com/twiml',
});
```

```go
// Go
import voiceml "github.com/voicetel/voiceml-go-sdk"

c, _ := voiceml.NewClient(voiceml.ClientOptions{AccountSid: "AC…", APIKey: "…"})
call, _ := c.Calls.Create(ctx, &voiceml.CreateCallParams{
    To: "+18005551234", From: "+18005550000", URL: voiceml.String("https://example.com/twiml"),
})
```

```java
// Java
import com.voicetel.voiceml.VoicemlClient;
import com.voicetel.voiceml.models.CreateCallRequest;

VoicemlClient c = VoicemlClient.builder().accountSid("AC…").apiKey("…").build();
var call = c.calls().create(CreateCallRequest.builder()
    .to("+18005551234").from("+18005550000").url("https://example.com/twiml").build());
```

```csharp
// C# / .NET
using VoiceML;
using VoiceML.Models;

var client = new VoiceMLClient(new ClientOptions { AccountSid = "AC…", ApiKey = "…" });
var call = await client.Calls.CreateAsync(new CreateCallRequest {
    To = "+18005551234", From = "+18005550000", Url = "https://example.com/twiml",
});
```

```php
// PHP
use VoiceML\Client;
use VoiceML\Model\CreateCallRequest;

$c = new Client(accountSid: 'AC…', apiKey: '…');
$call = $c->calls->create(new CreateCallRequest(
    to: '+18005551234', from: '+18005550000', url: 'https://example.com/twiml',
));
```

```ruby
# Ruby
require 'voiceml'

c = VoiceML::Client.new(account_sid: 'AC…', api_key: '…')
call = c.calls.create(to: '+18005551234', from: '+18005550000', url: 'https://example.com/twiml')
```

```swift
// Swift
import VoiceML

let c = try VoiceMLClient(options: .init(accountSid: "AC…", apiKey: "…"))
let call = try await c.calls.create(.init(to: "+18005551234", from: "+18005550000", url: "https://example.com/twiml"))
```

## 🧩 Resource groups

All eight SDKs expose the same eight top-level resources, each hanging off the client as a property:

| Resource | Covers |
|---|---|
| `client.calls` | Originate, fetch, terminate, hot-swap TwiML, list filtered by Status / StartTime — plus the per-call sub-resources: **Recordings**, **Streams** (audio_fork / `MZ` sids), **Siprec** (`SR` sids), **Transcriptions** (`RT` sids, real-time via Deepgram / Google / AWS / Azure), **Notifications**, **Events**, **UserDefinedMessages**, and **Payments** (REST `<Pay>` start / Capture advance / Status complete or cancel) |
| `client.conferences` | List, fetch, end. Plus **Participants** (mute / hold / kick) and **conference-scoped Recordings** |
| `client.messages` | Outbound SMS — create, fetch, list (To / From / DateSent filters), update (Body redaction; Status=canceled), delete. Pagination iterator. |
| `client.queues` | Create (idempotent on `FriendlyName`), list, update, delete. Plus **Members** — list, peek-front, dequeue-front, dequeue-specific |
| `client.applications` | CRUD on stored TwiML + callback bundles dispatched via `<Dial><Application>` |
| `client.recordings` | Account-wide list, metadata fetch, audio fetch (follows S3 redirect), delete |
| `client.incoming_phone_numbers` | List, create, fetch, update, delete tenant-assigned DIDs (PN-prefixed sids; `Capabilities` sub-struct; full Twilio-compat field surface) |
| `client.diagnostics` | `/health` deep probe (memdb / FreeSWITCH / disk / load), `/openapi.json` |

## 🔁 Twilio drop-in

The simplest migration path from `twilio-*` to VoiceML:

```python
# Before
from twilio.rest import Client as TwilioClient
client = TwilioClient("AC…", "<auth_token>")

# After
from voiceml import Client
client = Client(account_sid="AC…", auth_token="<auth_token>")  # api_key= also works
```

The constructor signature is the same `(account_sid, secret)` shape. `auth_token` / `authToken` is accepted as an alias for `api_key` / `apiKey`. Method names follow the resource map above (`client.calls.create(...)`) rather than Twilio's nested `client.api.v2010.accounts(sid).calls.create(...)` chain — flatter and language-idiomatic.

Where VoiceML extends Twilio:
- `Conference.member_count` on the live conference response.
- `Stream` sids are `MZ`-prefixed; `Siprec` is `SR`; `Transcription` is `RT`.
- `CallTranscription` exposes `transcription_engine` (`deepgram` / `google` / `aws` / `azure`) and `language_code` directly on the resource.
- The error class carries a typed `.more_info` / `.MoreInfo` accessor matching Twilio's docs-URL field.

Where VoiceML deliberately omits Twilio:
- No Studio, Flex, Verify, Pricing, Trunking, IP-Messaging surfaces.
- `POST /Calls/{Sid}/UserDefinedMessages` returns 501 (mounted as a compat stub).
- `POST /Conferences/{Sid}` v1 supports only `Status=completed`; Twilio's `AnnounceUrl` / `AnnounceMethod` aren't yet implemented.

Every SDK's README lists the per-language nuances.

## 🔢 Versioning

- Latest **released** SDK version: **v0.8.1** (matches the OpenAPI spec tag on GitHub).
- SDK package version tracks the API spec version in lockstep.
- The OpenAPI source of truth is published at [voicetel.com/docs/api/v0.8/voiceml/](https://voicetel.com/docs/api/v0.8/voiceml/). When the spec bumps, update all repos listed in this catalogue; each repo's GitHub Releases record the change.

## 🤝 Contributing

Each repo has its own contribution rules in its `README`. In general:

- Open an issue on the affected SDK's repo describing the change.
- Send a PR against `main`. CI runs tests + lint + coverage on every PR.
- Bugs that span multiple SDKs (spec drift, model mistakes) should be reported here in `voicetel/voiceml-sdks` and we'll fan them out.

## 📄 License

Every SDK in this catalogue is licensed under the **MIT License**. See each repo's `LICENSE` file (and this repo's [LICENSE](LICENSE)).

---

| Sponsor | Contribution |
|---------|--------------|
| [VoiceTel Communications](https://voicetel.com) | Primary development and production hosting |
