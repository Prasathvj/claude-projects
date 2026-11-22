# TechDecoded with Max — release folder & posting schedule

Each folder has everything for one upload: the **video (.mp4)**, **thumbnail.jpg** and **UPLOAD.md** (title, description with sources, tags, pinned comment, settings).
Folders are numbered in posting order. Times are **IST**. Channel: @TechDecodedWithMax.

| # | Folder | Title | Length | Publish (IST) | Status |
|---|--------|-------|--------|---------------|--------|
| – | [00_ep01_long](00_ep01_long) | This blank webpage can hijack your AI | 6:46 | — | ✅ Live |
| – | [00_ep01_short](00_ep01_short) | This blank webpage can hijack your AI | 0:39 | — | ✅ Live |
| 1 | [01_news02](01_news02) | The biggest IPO ever — and its rivals paid for it | 0:45 | **Sun 22 Nov, 6:30 PM** | ⏰ Scheduled — https://youtu.be/afiuq9Ru-W8 |
| 2 | [02_news01](02_news01) | Your AI moved your money. Who pays? | 0:47 | **Mon 23 Nov, 6:30 PM** | ⏰ Scheduled — https://youtu.be/1KGkVAtPK3M |
| 3 | [03_tip01](03_tip01) | Your AI just read a poisoned webpage. Now what? | 0:39 | **Tue 24 Nov, 12:30 PM** | ⏰ Scheduled — https://youtu.be/NIo9RcfA1ys |
| 4 | [04_job02](04_job02) | TCS & Infosys are hiring freshers. So why is headcount flat? | 0:42 | **Tue 24 Nov, 6:30 PM** | Uploads 23 Nov |
| 5 | [05_sat01](05_sat01) | GPS satellites have no idea where you are | 0:57 | **Wed 25 Nov, 12:30 PM** | Uploads 23 Nov |
| 6 | [06_job01](06_job01) | AI writes code. So why are developer jobs coming back? | 0:36 | **Wed 25 Nov, 6:30 PM** | Uploads 23 Nov |
| 7 | [07_goog01](07_goog01) | How Google knows what you're searching for | 0:54 | **Thu 26 Nov, 6:30 PM** | Uploads 24 Nov |
| 8 | [08_job03](08_job03) | AI got blamed for 120,000 layoffs. Then they stopped. | 0:40 | **Fri 27 Nov, 6:30 PM** | Uploads 24 Nov |
| 9 | [09_net01](09_net01) | What if the internet disappeared? | 0:55 | **Sat 28 Nov, 12:30 PM** | Uploads 24 Nov |
| 10 | [10_robo01](10_robo01) | Robots that work 24/7 — in the dark | 0:45 | **Sun 29 Nov, 12:30 PM** | Uploads 25 Nov |
| ▶ | next long video | Will Robots Replace Human Jobs? | ~7 min | target **Wed 2 Dec** | To make |

## Why this order
- **News first, while it's fresh:** the Anthropic IPO (18 Nov) and the bank AI-agent rule lose value every day they wait.
- **tip01 on day 3** follows the uploaded prompt-injection episode, so new viewers can go straight to the long video.
- **Alternating topics** (news → security → IT jobs → explainer) keeps the feed varied, and the three IT-jobs Shorts are spread out rather than back to back.
- **robo01 goes last** because it teases the next long video ("full video coming soon"). Publish the robots long video 3–4 days later.
- **Timing:** 2 Shorts a day for the first three days, then 1 a day. Uploaded and scheduled through vidIQ (free plan: 3 uploads per day). Weekdays at 6:30 PM IST, when Indian viewers are off work. Weekends at 12:30 PM IST.
- After about 2 weeks, check **YouTube Studio → Analytics → Audience → "When your viewers are on YouTube"** and move the time to your audience's peak.

## How to schedule a Short (YouTube Studio, desktop)
1. Go to studio.youtube.com, click **Create**, then **Upload videos**, and pick the `.mp4` from the folder.
2. **Details:** paste the Title, Description and Tags from `UPLOAD.md`. Set Audience to **No, it's not made for kids**.
3. **Thumbnail:** Studio on desktop doesn't let you set a Short's thumbnail. Use the **YouTube mobile app** instead (during upload, or later: tap the Short, then **Edit**, then the **pencil** on the thumbnail), choose a frame or upload `thumbnail.jpg`.
4. **Show more:** set **Altered content** to *No* (Max and Bit are clearly animated), Category to *Science & Technology*, and Language to *English*.
5. **Video elements:** skip; end screens and cards don't apply to Shorts.
6. **Visibility:** choose **Schedule**, then set the date and time from the table, and make sure the time zone says **(GMT+05:30) India**.
7. After it goes live, post the **pinned comment** from `UPLOAD.md` and pin it.
8. Optional: add a **Related video**. On the Short's edit page, link the long video `00_ep01_long` to tip01, news01 and news02.

## Notes
- The **subscribe outro** (spoken line plus animated button) is in job01, sat01, goog01, net01 and robo01. news01, news02, tip01, job02 and job03 were made before that rule; they can be updated before their slot if wanted.
- All narration is AI-generated (Gemini TTS). The "AI narrator" line is already in every description.
- Regenerate this folder after any re-render with `python3 tools/make_release.py <dir-with-thumb_<id>.png>` (thumbnails come from `hf/thumbs/thumb_short.html?id=<id>`).
