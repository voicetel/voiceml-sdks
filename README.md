# 🎙️ VoiceML SDKs

Official client libraries for the [VoiceML REST API](https://voiceml.voicetel.com) — VoiceTel's outbound voice + AMD service with a **Twilio-shaped wire format**. Eight languages, all hand-written, all targeting API **v0.4.0**, all MIT-licensed, all public.

![API](https://img.shields.io/badge/API-v0.4.0-blue)
![Compatibility](https://img.shields.io/badge/Twilio--compatible-wire%20format-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![SDKs](https://img.shields.io/badge/SDKs-8-brightgreen)

## 📚 Table of Contents

- [Why VoiceML](#-why-voiceml)
- [Pick your language](#-pick-your-language)
- [What every SDK gives you](#-what-every-sdk-gives-you)
- [API documentation](#-api-documentation)
- [Authentication, in 30 seconds](#-authentication-in-30-seconds)
- [Resource groups](#-resource-groups)
- [Twilio drop-in](#-twilio-drop-in)
- [Versioning & spec parity](#-versioning--spec-parity)
- [Contributing](#-contributing)
- [License](#-license)

## 💡 Why VoiceML

VoiceML is VoiceTel's outbound voice + AMD (answering-machine detection) service. The REST surface is **wire-compatible with Twilio's Programmable Voice API** (the `2010-04-01` namespace): the same path layout, the same auth model, the same error codes, the same pagination envelope. Existing Twilio SDKs can point at `https://voiceml.voicetel.com` and work as drop-in replacements.

These SDKs are written separately — they ship VoiceML-specific extensions (real-time transcription engines, per-call SIPREC and `MZ`-prefixed audio forks, `Conference.member_count`), don't carry Twilio's full surface (no Studio / Flex / Verify), and give you native error types in each language. Pick your language, install, and you're done.

## 🎯 Pick your language

Each row links straight to the SDK repo. All eight cover the same **53 operations across 6 resource groups** (Calls, Conferences, Queues, Applications, Recordings, Diagnostics — plus the call-scoped sub-resources for Streams, SIPREC, Transcriptions, Notifications, Events, and User-Defined Messages).

| Language | Repo | Install | Idiomatic style |
|---|---|---|---|
| 🐍 **Python** | [voiceml-python-sdk](https://github.com/voicetel/voiceml-python-sdk) | `pip install voiceml` | `Client` + `AsyncClient`, Pydantic v2, httpx |
| 🟦 **TypeScript / Node** | [voiceml-node-sdk](https://github.com/voicetel/voiceml-node-sdk) | `npm install voiceml` | ESM + CJS, async-only, `fetch`-based, zero runtime deps |
| 🐹 **Go** | [voiceml-go-sdk](https://github.com/voicetel/voiceml-go-sdk) | `go get github.com/voicetel/voiceml-go-sdk` | `context.Context`, stdlib `net/http`, zero deps |
| ☕ **Java** | [voiceml-java-sdk](https://github.com/voicetel/voiceml-java-sdk) | `com.voicetel:voiceml:0.4.0` | Java 11, `java.net.http`, Jackson, builders |
| 🟪 **C# / .NET** | [voiceml-csharp-sdk](https://github.com/voicetel/voiceml-csharp-sdk) | `dotnet add package VoiceML` | net8.0, `async/await`, `System.Text.Json`, zero NuGet deps |
| 🐘 **PHP** | [voiceml-php-sdk](https://github.com/voicetel/voiceml-php-sdk) | `composer require voicetel/voiceml` | PHP 8.1+, Guzzle 7, typed enums, PSR-4 |
| 💎 **Ruby** | [voiceml-ruby-sdk](https://github.com/voicetel/voiceml-ruby-sdk) | `gem install voiceml` | Ruby 3.0+, stdlib `Net::HTTP`, kwargs, zero gem deps |
| 🦅 **Swift** | [voiceml-swift](https://github.com/voicetel/voiceml-swift) | SwiftPM: `https://github.com/voicetel/voiceml-swift` | Swift 5.9, `async throws`, `URLSession`, iOS/macOS/tvOS/watchOS/Linux |

## ✨ What every SDK gives you

- **Strongly typed end-to-end** — every request body and response payload is a typed struct / class / record in the host language.
- **Twilio-shape wire format** — the same `2010-04-01/Accounts/{AccountSid}/...` paths, the same HTTP Basic auth, the same `{code, message, more_info, status}` error envelope. If you're migrating from `twilio-python` / `twilio-node` / etc., the constructor signature is the same.
- **Auto-retry on 429 / 5xx** with `Retry-After` honored, exponential backoff capped at 8 s. Default `maxRetries = 2`.
- **Structured errors** — every SDK exposes an `ApiError` (or equivalent) plus status-keyed subclasses: `AuthenticationError` (401), `NotFoundError` (404), `ConflictError` (409), `GoneError` (410), `RateLimitError` (429), `NotImplementedAPIError` (501), `ServerError` (5xx). Catch broadly or pattern-match.
- **Form-urlencoded by default**, JSON-body acceptance documented — matches Twilio's wire convention exactly.
- **Booleans as `"true"` / `"false"` strings** — what Twilio sends; what every SDK here sends.
- **Cursor-style pagination** — `next_page_uri` / `previous_page_uri` honored; Python and TypeScript include an `iterate()` helper for `/Calls`.
- **Recording audio fetch** — `recordings.get_audio(sid)` transparently follows the 302 → S3 presigned-URL redirect; you get the WAV bytes regardless of where they were served from.
- **Zero codegen footprint** — every line is hand-written. No Swagger Codegen artifacts, no auto-generated method names like `accountsAccountSidCallsGet`.

## 📖 API documentation

- **Reference docs:** [voiceml.voicetel.com](https://voiceml.voicetel.com)
- **Raw OpenAPI 3.1 spec:** [voiceml.voicetel.com/openapi.json](https://voiceml.voicetel.com/openapi.json)
- **Health probe:** [voiceml.voicetel.com/health](https://voiceml.voicetel.com/health)

## 🔑 Authentication, in 30 seconds

VoiceML uses **HTTP Basic auth** — the same shape Twilio uses:

- **Username** = your `AccountSid` (Twilio format: literal `AC` + 32 hex chars)
- **Password** = your per-tenant API key

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

All eight SDKs expose the same six top-level resources, each hanging off the client as a property:

| Resource | Covers |
|---|---|
| `client.calls` | Originate, fetch, terminate, hot-swap TwiML, list filtered by Status / StartTime — plus the per-call sub-resources: **Recordings**, **Streams** (audio_fork / `MZ` sids), **Siprec** (`SR` sids), **Transcriptions** (`RT` sids, real-time via Deepgram / Google / AWS / Azure), **Notifications**, **Events**, **UserDefinedMessages** |
| `client.conferences` | List, fetch, end. Plus **Participants** (mute / hold / kick) and **conference-scoped Recordings** |
| `client.queues` | Create (idempotent on `FriendlyName`), list, update, delete. Plus **Members** — list, peek-front, dequeue-front, dequeue-specific |
| `client.applications` | CRUD on stored TwiML + callback bundles dispatched via `<Dial><Application>` |
| `client.recordings` | Account-wide list, metadata fetch, audio fetch (follows S3 redirect), delete |
| `client.diagnostics` | `/health` deep probe (memdb / FreeSWITCH / disk / load), `/openapi.json` |

## 🔁 Twilio drop-in

The simplest migration path from `twilio-*` to VoiceML:

```python
# Before
from twilio.rest import Client as TwilioClient
client = TwilioClient("AC…", "<auth_token>")

# After
from voiceml import Client
client = Client(account_sid="AC…", api_key="<api_key>")
```

The constructor signature is the same `(account_sid, secret)` shape. Method names follow the resource map above (`client.calls.create(...)`) rather than Twilio's nested `client.api.v2010.accounts(sid).calls.create(...)` chain — flatter and language-idiomatic.

Where VoiceML extends Twilio:
- `Conference.member_count` on the live conference response.
- `Stream` sids are `MZ`-prefixed; `Siprec` is `SR`; `Transcription` is `RT`.
- `CallTranscription` exposes `transcription_engine` (`deepgram` / `google` / `aws` / `azure`) and `language_code` directly on the resource.

Where VoiceML deliberately omits Twilio:
- No Studio, Flex, Verify, Messaging, Pricing, Trunking, IP-Messaging surfaces — VoiceML is **voice + AMD only**.
- `POST /Calls/{Sid}/UserDefinedMessages` returns 501 (mounted as a compat stub).
- `POST /Conferences/{Sid}` v1 supports only `Status=completed`; Twilio's `AnnounceUrl` / `AnnounceMethod` aren't yet implemented.

Every SDK's README lists the per-language nuances.

## 🔢 Versioning & spec parity

- All SDKs target **VoiceML API v0.4.0** (the `2010-04-01` Twilio-shape namespace).
- SDK package version tracks the API version: Python `0.4.0`, npm `0.4.0`, Java `0.4.0`, NuGet `0.4.0`, Composer `0.4.0`, Gem `0.4.0`, Swift `0.4.0`, Go module tagged `v0.4.0`.
- The OpenAPI source of truth is at [voiceml.voicetel.com/openapi.json](https://voiceml.voicetel.com/openapi.json). When the spec bumps, the SDKs get updated commits; each repo's `CHANGELOG` (or commit history) records the change.

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
