# ep01 — Prompt injection: fact sheet (checked 2026-11-21)

| Claim in script | Source |
|---|---|
| Prompt injection is LLM01, the #1 risk, in the OWASP Top 10 for LLM Applications 2025 | https://genai.owasp.org/llmrisk/llm01/ |
| OpenAI (Dec 2025, hardening ChatGPT Atlas): prompt injection "is unlikely to ever be fully solved" | https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/ |
| Sept 2022: Riley Goodside's GPT-3 demo ("Ignore the above directions…"); Simon Willison named it "prompt injection" (12 Sept 2022). Note: an earlier use of the term (May 2022) exists, so the script says "the name that stuck", not "coined". | https://simonwillison.net/2022/Sep/12/prompt-injection/ · https://www.simonwillison.net/2025/Aug/4/himbodhisattva |
| UK NCSC: prompt injection is not SQL injection; SQL injection has a fix (parameterised queries), prompt injection may never be fixed that way (8 Dec 2025) | https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection |
| Indirect prompt injection paper, Feb 2023 (Greshake, Abdelnabi et al.), demonstrated against Bing's GPT-4 powered Chat; retrieval blurs data and instructions | https://arxiv.org/abs/2302.12173 |
| EchoLeak, CVE-2025-32711, Microsoft 365 Copilot, zero-click, found by Aim Labs (Aim Security); CVSS 9.3 critical; reported Jan 2025, fixed May 2025 (server-side); Microsoft: no evidence of exploitation | https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html · https://www.securityweek.com/echoleak-ai-attack-enabled-theft-of-sensitive-data-via-microsoft-365-copilot/ |
| The Promptware Kill Chain (Brodt, Feldman, Schneier, Nassi), arXiv 2601.09625, Jan 2026 (v2 Feb 2026): 36 studies/incidents, at least 21 attacks traverse 4+ stages | https://arxiv.org/abs/2601.09625 |
| Lethal trifecta (Simon Willison, 16 June 2025): private data + untrusted content + external communication; cut one leg | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ |
| Agents Rule of Two (Meta AI blog, 31 Oct 2025): no more than two of untrusted input / sensitive systems or data / change state or communicate externally, else human oversight | https://ai.meta.com/blog/practical-ai-agent-security/ |
| OWASP Top 10 for Agentic Applications (2026 edition, published Dec 2025): ASI01 Agent Goal Hijack | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |

## Labelled as illustration (not real data)
- The pancake page, its hidden text, both chat threads, the weather-tool description, the memory notes: ILLUSTRATION.
- EchoLeak email and the image-link code: RECREATION / SIMPLIFIED (not Aim's real payload).
- The kill-chain list is simplified to 5 plain-language steps (the paper's v2 has 7 stages).
- The counter "9 → 0 clicks" is an animation of "zero clicks", not data.

## Claims deliberately NOT used (could not trace to a primary source)
- "32% rise in malicious prompt-injection payloads" and "5x more indirect injections" (only in AI-assisted/secondary write-ups).
- A "GAO report on AI agents carrying out cyberattacks" (the verifiable GAO-27-108814 is about chatbots producing attack plans).
