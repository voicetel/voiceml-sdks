# 🎙️ VoiceML SDKs

Official client libraries for the [VoiceML REST API](https://voicetel.com/docs/api/v0.9/voiceml/) — VoiceTel's Twilio-compatible voice, messaging and answering-machine-detection service. Eight hand-written SDKs in public repositories; see [License](#-license) for their individual terms.

![API](https://img.shields.io/badge/API-v0.9.2-blue)
![Compatibility](https://img.shields.io/badge/Twilio--compatible-wire%20format-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![SDKs](https://img.shields.io/badge/SDKs-8-brightgreen)

## 📚 Table of Contents

- [Why VoiceML](#-why-voiceml)
- [Pick your language](#-pick-your-language)
- [Releases](#-releases)
- [Tooling](#-tooling)
- [What every SDK gives you](#-what-every-sdk-gives-you)
- [API Documentation](#-api-documentation)
- [Authentication, in 30 seconds](#-authentication-in-30-seconds)
- [Resource groups](#-resource-groups)
- [Twilio-compatible migration](#-twilio-compatible-migration)
- [Versioning](#-versioning)
- [Contributing](#-contributing)
- [License](#-license)

## 💡 Why VoiceML

VoiceML provides a **Twilio-compatible API** for voice and messaging, including account-scoped resources in the `2010-04-01` namespace. Migration uses VoiceML-issued credentials and the VoiceML endpoint; resource coverage and method names are documented in each SDK. Twilio-issued credentials do not authenticate with VoiceML.

These SDKs include VoiceML extensions such as live transcription, per-call SIPREC, `MZ`-prefixed audio forks, `Conference.member_count`, and REST-side `<Pay>` session control, with native models and error types in each language.

## 🎯 Pick your language

Each row links to the official SDK source. Install commands select published packages except for C#, whose source/local-feed installation is described below. Coverage evolves with the OpenAPI document; use each repository's release notes and spec-contract results for the exact source snapshot it supports.

| Language | Repo | Install | Idiomatic style |
|---|---|---|---|
| 🐍 **Python** | [voiceml-python-sdk](https://github.com/voicetel/voiceml-python-sdk) | `pip install voiceml` | `Client` + `AsyncClient`, Pydantic v2, httpx |
| 🟦 **TypeScript / Node** | [voiceml-node-sdk](https://github.com/voicetel/voiceml-node-sdk) | `npm install @voicetel.com/voiceml` | ESM, async-only, `fetch`-based, zero runtime deps; CommonJS packaging fix pending release |
| 🐹 **Go** | [voiceml-go-sdk](https://github.com/voicetel/voiceml-go-sdk) | `go get github.com/voicetel/voiceml-go-sdk` | `context.Context`, stdlib `net/http`, zero deps |
| ☕ **Java** | [voiceml-java-sdk](https://github.com/voicetel/voiceml-java-sdk) | `com.voicetel:voiceml:0.9.2` | Java 11, `java.net.http`, Jackson, builders |
| 🟪 **C# / .NET** | [voiceml-csharp-sdk](https://github.com/voicetel/voiceml-csharp-sdk) | NuGet publication pending — [build from source / local feed](#c-installation-from-source) | .NET 8+, `async/await`, `System.Text.Json`, no runtime package dependencies |
| 🐘 **PHP** | [voiceml-php-sdk](https://github.com/voicetel/voiceml-php-sdk) | `composer require voicetel/voiceml` | PHP 8.1+, Guzzle 7, typed enums, PSR-4 |
| 💎 **Ruby** | [voiceml-ruby-sdk](https://github.com/voicetel/voiceml-ruby-sdk) | `gem install voiceml` | Ruby 3.1+, stdlib `Net::HTTP`, kwargs, zero gem deps |
| 🦅 **Swift** | [voiceml-swift](https://github.com/voicetel/voiceml-swift) | SwiftPM: `https://github.com/voicetel/voiceml-swift` | Swift 5.9, `async throws`, `URLSession`, iOS/macOS/tvOS/watchOS/Linux |

### C# installation from source

As checked on **2026-10-17**, `VoiceML` is **not published on nuget.org**. A GitHub Release is not proof of a NuGet publication. Build a package from the [official source](https://github.com/voicetel/voiceml-csharp-sdk) and select its local feed explicitly. With the .NET 10 SDK, run from a directory where you want the checkout, feed and application:

```sh
git clone https://github.com/voicetel/voiceml-csharp-sdk.git
dotnet pack voiceml-csharp-sdk/src/VoiceML/VoiceML.csproj -c Release -o "$PWD/voiceml-local-feed"
dotnet new console -n MyVoiceApp -f net8.0
dotnet add MyVoiceApp/MyVoiceApp.csproj package VoiceML --version 0.9.2 --source "$PWD/voiceml-local-feed"
dotnet build MyVoiceApp/MyVoiceApp.csproj -c Release
```

Alternatively, use a source project reference after cloning:

```sh
dotnet new console -n MyVoiceApp -f net8.0
dotnet add MyVoiceApp/MyVoiceApp.csproj reference voiceml-csharp-sdk/src/VoiceML/VoiceML.csproj
dotnet build MyVoiceApp/MyVoiceApp.csproj -c Release
```

## 🏷️ Releases

Release status checked **2026-10-17**: all eight SDK repositories have a **v0.9.2 GitHub Release**. Registry availability is separate: C# still requires the source/local-feed path above. This catalogue's own latest GitHub Release is [v0.9.1](https://github.com/voicetel/voiceml-sdks/releases/tag/v0.9.1); the SDK release table does not imply a v0.9.2 catalogue release.

| Language | Latest release | All releases |
|---|---|---|
| 🐍 Python | [v0.9.2](https://github.com/voicetel/voiceml-python-sdk/releases/tag/v0.9.2) | [history](https://github.com/voicetel/voiceml-python-sdk/releases) |
| 🟦 TypeScript / Node | [v0.9.2](https://github.com/voicetel/voiceml-node-sdk/releases/tag/v0.9.2) | [history](https://github.com/voicetel/voiceml-node-sdk/releases) |
| 🐹 Go | [v0.9.2](https://github.com/voicetel/voiceml-go-sdk/releases/tag/v0.9.2) | [history](https://github.com/voicetel/voiceml-go-sdk/releases) |
| ☕ Java | [v0.9.2](https://github.com/voicetel/voiceml-java-sdk/releases/tag/v0.9.2) | [history](https://github.com/voicetel/voiceml-java-sdk/releases) |
| 🟪 C# / .NET | [v0.9.2](https://github.com/voicetel/voiceml-csharp-sdk/releases/tag/v0.9.2) | [history](https://github.com/voicetel/voiceml-csharp-sdk/releases) |
| 🐘 PHP | [v0.9.2](https://github.com/voicetel/voiceml-php-sdk/releases/tag/v0.9.2) | [history](https://github.com/voicetel/voiceml-php-sdk/releases) |
| 💎 Ruby | [v0.9.2](https://github.com/voicetel/voiceml-ruby-sdk/releases/tag/v0.9.2) | [history](https://github.com/voicetel/voiceml-ruby-sdk/releases) |
| 🦅 Swift | [v0.9.2](https://github.com/voicetel/voiceml-swift/releases/tag/v0.9.2) | [history](https://github.com/voicetel/voiceml-swift/releases) |

Release highlights:
- **v0.7.x and earlier** — calls, conferences, queues, applications, recordings, incoming phone numbers, SMS and REST payment-session control; README consistency updates and model fixes.
- **v0.8.x** — SIP domain, credential-list and IP access-control management, plus Routes v2 SIP-domain region settings.
- **v0.9.1** — Conversations v1 (including service-scoped resources), Voice v1, Routes v2 phone-number region settings, and Assistants v1.
- **v0.9.2** — Messaging Service management, Pricing v1/v2 lookups (including Trunking rates), and separate Conversations/Messaging product hosts with configurable overrides.

### Pending SDK fixes

The current source work includes missing account/balance, caller-ID, message-media, recorded-transcription, export, usage, SIP-registration, Messaging Service phone-number and YAML-diagnostic operations; pagination, retry, download and model fixes; webhook-signature helpers; and the TypeScript CommonJS packaging repair. These are **unreleased fixes**, not features of the existing registry packages merely because their working-tree version still reads `0.9.2`. See each SDK's Unreleased changelog when those changes land. The resource table below distinguishes these additions from released coverage; it does not claim complete operation coverage for v0.9.2.

## 🛠️ Tooling

| Tool | Repo | Purpose |
|---|---|---|
| **CLI** | [voiceml-cli](https://github.com/voicetel/voiceml-cli) | Interactive REPL + `-x` one-shot commands for a subset of the API. Independent release line; latest GitHub Release is [v0.2.0](https://github.com/voicetel/voiceml-cli/releases/tag/v0.2.0), built against an older SDK. |
| **Collections** | [voiceml-api-collections](https://github.com/voicetel/voiceml-api-collections) | Postman v2.1 + Bruno requests. The [v0.9.1 release archive](https://github.com/voicetel/voiceml-api-collections/releases/tag/v0.9.1) predates the generated collections on `main`; current-spec regeneration and host/body fixes await release. Consult the repository for snapshot coverage. |

## ✨ What every SDK gives you

- **Native request/response models** and resource-oriented methods, with per-language naming.
- **VoiceML HTTP Basic authentication**, with `auth_token` / `authToken` aliases for migration-compatible constructor usage.
- **Structured API errors** exposing HTTP status, API code and `more_info` where supplied. Go uses error helpers; class-based SDKs use their documented exception hierarchies.
- **Endpoint-specific encoding**: form-urlencoded account-resource writes and JSON for endpoints that declare JSON, including Assistants.
- **Configurable HTTP clients, timeouts and retries**, plus list and recording-audio helpers. Exact behavior depends on the installed release.

The pending transport fixes follow server-provided continuation links rather than page counters; retry GET/HEAD/DELETE/PUT on retryable status/transport failures; and retry POST/PATCH only on 429 or connection-establishment failures where nothing was sent. They add HTTP-date `Retry-After` parsing with a 60-second cap and full-jitter backoff (0.5-second base, 8-second ceiling; default two retries). Download fixes strip credentials on cross-origin redirects and refuse HTTPS-to-HTTP redirects. These fixes require the next SDK release or a build from the repaired source.

## 📖 API Documentation

- **Reference docs:** [voicetel.com/docs/api/v0.9/voiceml/](https://voicetel.com/docs/api/v0.9/voiceml/)
- **Validator:** [voicetel.com/voiceml/validator/](https://voicetel.com/voiceml/validator/)
- **SDK catalogue:** [voicetel.com/docs/voiceml-sdks/](https://voicetel.com/docs/voiceml-sdks/)
- **SDK source:** the official GitHub repositories in [Pick your language](#-pick-your-language); this catalogue is maintained at [voicetel/voiceml-sdks](https://github.com/voicetel/voiceml-sdks).

## 🔑 Authentication, in 30 seconds

VoiceML uses **HTTP Basic auth**:

- **Username** = your VoiceML `AccountSid` (literal `AC` + 32 hex characters).
- **Password** = your VoiceML API key (`auth_token` / `authToken` is only an SDK argument alias).

Twilio-issued credentials do **not** work. Replace the sample AccountSid and key below with your VoiceML credentials, and replace the fictional phone numbers and example TwiML URL before running. These examples create an outbound call; verification compiles or mocks them without calling production.

```python
# Python
from voiceml import Client
from voiceml.models import CreateCallRequest

with Client(account_sid="AC00000000000000000000000000000001", api_key="your-voiceml-api-key") as c:
    call = c.calls.create(CreateCallRequest(
        to="+14155550100", from_="+14155550101", url="https://example.com/twiml",
    ))
```

```ts
// TypeScript / Node
import { Client } from '@voicetel.com/voiceml';

const c = new Client({ accountSid: 'AC00000000000000000000000000000001', apiKey: 'your-voiceml-api-key' });
const call = await c.calls.create({
  To: '+14155550100', From: '+14155550101', Url: 'https://example.com/twiml',
});
```

```go
package main

import (
    "context"
    "fmt"
    "log"

    voiceml "github.com/voicetel/voiceml-go-sdk"
)

func main() {
    c, err := voiceml.NewClient(voiceml.ClientOptions{
        AccountSid: "AC00000000000000000000000000000001", APIKey: "your-voiceml-api-key",
    })
    if err != nil {
        log.Fatal(err)
    }
    call, err := c.Calls.Create(context.Background(), voiceml.CreateCallParams{
        To: "+14155550100", From: "+14155550101", URL: voiceml.String("https://example.com/twiml"),
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(call.Sid)
}
```

```java
// Java
import com.voicetel.voiceml.VoicemlClient;
import com.voicetel.voiceml.models.CreateCallRequest;

VoicemlClient c = VoicemlClient.builder()
    .accountSid("AC00000000000000000000000000000001").apiKey("your-voiceml-api-key").build();
var call = c.calls().create(CreateCallRequest.builder()
    .to("+14155550100").from("+14155550101").url("https://example.com/twiml").build());
```

```csharp
// C# / .NET
using VoiceML;
using VoiceML.Models;

using var client = new VoiceMLClient(new ClientOptions {
    AccountSid = "AC00000000000000000000000000000001", ApiKey = "your-voiceml-api-key",
});
var call = await client.Calls.CreateAsync(new CreateCallRequest {
    To = "+14155550100", From = "+14155550101", Url = "https://example.com/twiml",
});
```

```php
<?php
// PHP
require __DIR__ . '/vendor/autoload.php';

use VoiceML\Client;
use VoiceML\Model\CreateCallRequest;

$c = new Client(accountSid: 'AC00000000000000000000000000000001', apiKey: 'your-voiceml-api-key');
$call = $c->calls->create(new CreateCallRequest(
    to: '+14155550100', from: '+14155550101', url: 'https://example.com/twiml',
));
```

```ruby
# Ruby
require 'voiceml'

c = VoiceML::Client.new(account_sid: 'AC00000000000000000000000000000001', api_key: 'your-voiceml-api-key')
call = c.calls.create(to: '+14155550100', from: '+14155550101', url: 'https://example.com/twiml')
```

```swift
// Swift
import VoiceML

let c = try VoiceMLClient(options: .init(accountSid: "AC00000000000000000000000000000001", apiKey: "your-voiceml-api-key"))
let call = try await c.calls.create(.init(to: "+14155550100", from: "+14155550101", url: "https://example.com/twiml"))
```

## 🧩 Resource groups

Resource names below are conceptual: Python/Ruby use snake_case, TypeScript/PHP/Swift use camelCase, C#/Go use exported members, and Java uses accessor methods. **Released** means that the resource family exists in v0.9.2, not that every current spec operation was implemented then. **Pending** identifies additions in the unreleased source fixes.

| Resource group | Released v0.9.2 coverage | Pending source additions/fixes |
|---|---|---|
| Calls | Create, fetch, list, update, delete; call recordings; start/stop Streams, SIPREC and live Transcriptions; notifications, events, payment sessions, user-defined-message stub | Remove unsupported GETs below; request/model and transport fixes |
| Conferences | List, fetch, end; participants; recording list/fetch/update/delete | Start conference recording |
| Messages | SMS create/fetch/list/update/delete | MMS request fields and message-media list/fetch/delete |
| Queues | Queue management and member list/peek/dequeue | Continuation-link pagination fixes |
| Applications | Stored TwiML and callback configuration | SMS/delivery callback fields |
| Recordings and recorded transcriptions | Account recording list, metadata/audio fetch, delete | Account- and recording-scoped recorded-transcription list/fetch/delete; download fixes |
| Incoming phone numbers | Number management and Local/Mobile/TollFree variants | SMS routing fields and corrected list/request models |
| Accounts and balance | — | Fetch/update authenticated account; fetch balance |
| Outgoing caller IDs | — | Verify, list, fetch, update, delete |
| Usage records | — | List and named date windows |
| Notifications and exports | Account notification log | Daily event-log archive list/download |
| SIP | Domains, credential lists/credentials, IP ACLs/addresses, domain mappings for calls and registrations | Live SIP-registration listing |
| Voice v1 | BYOC trunks, connection policies/targets, dialing-permission settings, source-IP mappings, IP records | Model, path and transport fixes |
| Routes v2 | Inbound processing regions for SIP domains and phone numbers | Path-encoding fixes |
| Pricing v1/v2 | Read-only Voice, Messaging, Phone Numbers and Trunking country/number rate lookups | Path/model fixes |
| Conversations v1 | Conversations, messages, participants, receipts, webhooks, roles, users, credentials, configuration, services and service-scoped resources | Continuation-link and model fixes |
| Messaging v1 Services | Service create/list/fetch/update/delete on the messaging host | Service phone-number sender-pool list/add/fetch/remove |
| Assistants v1 | Assistants, tools, knowledge/status/chunks, sessions/messages, feedback and policies | Corrected list/request models |
| Diagnostics | `/health`, `/openapi.json` | Credential-less transport helpers; `/openapi.yaml`, `/openapi.yml` |

**Unsupported call-subresource GETs:** the server returns HTTP **405**, API code **20004**, for list/fetch at `/2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Streams.json`, `/Streams/{Sid}.json`, `/Siprec.json`, `/Siprec/{Sid}.json`, `/Transcriptions.json` and `/Transcriptions/{Sid}.json` (all under that call prefix). The pending SDK fixes remove those methods. Use the supported POST start/stop operations; recorded-transcription retrieval is a separate resource.

Conversations requests use `https://conversations.voicetel.com`; Messaging Service requests use `https://messaging.voicetel.com`. Other resources use `https://voiceml.voicetel.com`. Product-base-URL overrides are available for custom deployments; see the SDK-specific option names.

## 🔁 Twilio-compatible migration

Migration changes credentials, endpoint configuration and SDK method usage. For example, the VoiceML Python client accepts `auth_token` as an alias, but its value must be your **VoiceML API key**:

```python
from voiceml import Client

with Client(account_sid="AC00000000000000000000000000000001", auth_token="your-voiceml-api-key") as client:
    pass  # Use VoiceML resource methods here; api_key= also works.
```

Method names follow each language's resource map, such as `client.calls.create(...)`. Review supported fields and response models in the selected SDK before migrating an application.

VoiceML-specific details:
- `Conference.member_count` on the live conference response.
- `Stream` sids are `MZ`-prefixed; `Siprec` is `SR`; `Transcription` is `RT`.
- Live-transcription start requests select an engine and language; do not rely on those request fields being echoed in the response.
- Error helpers expose `more_info` when the server supplies a documentation URL.

Scope and limitations:
- Studio, Flex and Verify are outside this catalogue's API scope. Pricing lookups, SIP trunking configuration, Conversations and Messaging Services are included as described above; this is not a claim of support for every Twilio product or operation.
- `POST /Calls/{Sid}/UserDefinedMessages` returns 501 (mounted as a compat stub).
- `POST /Conferences/{Sid}` v1 supports only `Status=completed`; Twilio's `AnnounceUrl` / `AnnounceMethod` aren't yet implemented.

Every SDK's README lists the per-language nuances.

## 🔢 Versioning

- Latest **released SDK repository tags**: **v0.9.2**. See the release table for links and the C# note for package availability. This catalogue's latest release is **v0.9.1**.
- The eight language SDKs track the API spec version together at release time. The CLI has its own version line; collections and catalogue releases can lag.
- A spec version alone does not establish operation coverage: the document can change before the next version cut. Match coverage claims to a dated spec snapshot and a passing contract test, and check Unreleased changes separately from published packages.
- The public API reference is at [voicetel.com/docs/api/v0.9/voiceml/](https://voicetel.com/docs/api/v0.9/voiceml/). The path uses major.minor, so patch releases stay on `/v0.9/`.

## 🤝 Contributing

Each repo has its own contribution rules in its `README`. In general:

- Open an issue on the affected SDK's repo describing the change.
- Send a PR against `main` in the affected repository and run its documented checks.
- Bugs that span multiple SDKs (spec drift, model mistakes) should be reported here in `voicetel/voiceml-sdks` and we'll fan them out.

Catalogue CI checks links, advertised registry versions, and compilation of the Go and TypeScript quickstarts. Run `python3 scripts/check_examples.py --scratch /tmp/voiceml-catalogue-check` locally; optional `--go-module` and `--typescript-package` arguments verify a local SDK checkout/build without modifying it. Registry verification is read-only: `python3 scripts/check_registries.py`. The catalogue ships documentation, not an SDK package.

## 📄 License

This catalogue is licensed under the **MIT License**: see [LICENSE](LICENSE). SDK terms are separate. As checked on 2026-10-17:

- **Python, TypeScript, Go, Java, C# and PHP** carry **MIT with Commons Clause** terms in their repository `LICENSE` files.
- **Ruby and Swift** carry plain **MIT** licences.

Read the `LICENSE` in the specific SDK repository linked above; a registry badge or package metadata is not a substitute for that text.

---

| Sponsor | Contribution |
|---------|--------------|
| [VoiceTel Communications](https://voicetel.com) | Primary development and production hosting |
