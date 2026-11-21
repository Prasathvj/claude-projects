# Is your phone listening to you? (DRAFT 2, detailed, awaiting approval)

## Verified facts (searched 2026-11-17)
- Apple ML Journal: "Hey Siri" runs on device in two stages. A tiny always-on detector on a low-power chip uses a ring buffer of audio; audio without the phrase is discarded; only a candidate goes to a stronger checker. Speaker matching is local. (Primary, Apple.) NOT claimed: "raw audio is never transmitted" (inference only).
- Google: the device itself listens for "Hey Google" and audio is sent only after it detects it; if no activation, snippets are not sent or saved. "False accepts" happen: background noise read as the phrase; reviewers hear about 0.2% of snippets, only users with Voice & Audio Activity on (Google blog/support, 2019-21; may have changed).
- Apple settled the Siri class action (Lopez v. Apple) over recordings made without "Hey Siri"; Apple now does not keep audio by default. No amount/date in the script.
- Northeastern University, 2018, 17,000+ Android apps tested: no app secretly turned on the mic; but some apps sent screenshots/screen video to third parties (e.g. GoPuff to Appsee). Limits: could not sign into apps, may miss on-device processing. (Northeastern news release.)
- Cox Media Group "Active Listening" pitch deck (404 Media, Sept 2024); Google removed CMG from Partners Program; Meta reviewed. FTC settlement May 2026 alleged deceptive claims; reports say the service did not use voice data. CHECK ftc.gov before publishing. No dollar figures.
- Meta/Google say mic is not used for ads (press quotes). Apple's wording not found, do not attribute.
- Ad targeting: real-time bidding auction on every ad slot; bid request can include advertising ID, location, IP, device details, interests. Data brokers buy location from app SDKs; advertising IDs stitch apps together. Advertisers upload customer lists, platforms build "lookalike audiences". IP address ties devices to one home network. (Mozilla, EFF, EPIC, The Markup.)
- Frequency illusion is a known bias (general knowledge, uncited).
- Indicators: iPhone orange dot = mic, green = camera, Control Center names the app; Settings > Privacy & Security > Microphone. Android 12+: green dot; Settings > Privacy > Privacy dashboard / Permission Manager (names vary).
- TO VERIFY before publishing (not searched): iPhone Settings > Privacy & Security > Tracking ("Allow apps to request to track"); Android advertising ID reset/delete (Settings > Privacy > Ads).

## LONG (about 4:30, ~590 words). Pictures: character sheet, 4 locations, scenes, tip cards.

### Ch 1. The shoe ad (0:00)
You say it out loud: "I need new running shoes." Ten minutes later, your phone shows you running shoes. It feels like a crime scene. So let's find out what is really going on, step by step.

### Ch 2. What your phone really listens for (0:20)
Yes, your phone listens. But not the way you fear. Inside it, a tiny program runs all day on a low-power chip. Its only job is to spot one pattern: Hey Siri, or Hey Google. It keeps a few seconds of sound in a short loop, like a conveyor belt. If the pattern is not there, the sound falls off the end and is gone. Only when it hears the phrase does the full assistant wake up and start sending your request to a server.

### Ch 3. But it is not perfect (1:00)
Sometimes the tiny program is wrong. A noise or a similar phrase sounds like the wake word. Google calls this a false accept. Apple faced a lawsuit over Siri recordings made when nobody said the phrase, and it settled. Apple now does not keep audio by default. So accidents are real. But that is a bug, not a plan to sell you shoes.

### Ch 4. What researchers found when they tested (1:35)
Researchers at Northeastern University tested more than seventeen thousand Android apps. Not one secretly turned on the microphone. But they found something else: some apps were sending screenshots and screen recordings of what you do to other companies. Remember that, because it is the real privacy leak. The test had limits, so it is evidence, not proof.

### Ch 5. The company that bragged (2:10)
In 2024 a marketing company pitched something called Active Listening, saying it could hear your conversations to target ads. Google dropped it as a partner. Later the FTC settled with the company over deceptive claims, saying the service did not actually listen. A sales pitch, not a secret microphone.

### Ch 6. So how do they know? (2:40)
Here is how. One: your searches and the sites you visit. Two: your location. Apps sell it through ad software, so you walking into a shoe store can show shoe ads. Three: your purchases and the email you sign up with. Four: every ad slot you see is auctioned in a split second, and the bid carries your advertising ID, your rough location and your interests. Five: the same home Wi-Fi. If your friend searched for shoes on your network, the ad can follow you too. Six: lookalike groups. Advertisers give a list of buyers, and the platform finds people similar to them. People like you.

### Ch 7. And your brain does the rest (3:25)
Then there is your own mind. When you start thinking about shoes, you notice shoe ads. You never noticed the hundred ads that did not match. This is the frequency illusion. It makes coincidences feel like proof.

### Ch 8. Check it yourself (3:45) [tip card]
Look at the top corner of your screen. Orange dot on an iPhone: a microphone is in use. Green: the camera. Swipe down and it names the app. On Android 12 or newer, a green dot, and the Privacy dashboard shows every app that used your mic in the last day.

### Ch 9. Lock it down (4:05) [tip card]
Open Settings, Privacy, Microphone. Switch off any app that has no reason to hear you. A voice recorder needs it. A flashlight does not. Then limit the ad tracking: ask apps not to track you, and reset your advertising ID. Menus differ by phone, but they are all in Privacy.

### Ch 10. Recap (4:20)
Your phone listens for a wake phrase and throws the rest away. Ads come from the trail you leave: searches, places, purchases, your Wi-Fi. Check the dot, switch off the apps that do not need your mic, and you will see less of it. Follow for more.

## SHORT (about 50 s, ~120 words, V1-V10)
1. You say "running shoes" out loud, and minutes later you see shoe ads. Is your phone listening?
2. It listens for one thing: a wake phrase, like Hey Siri. Everything else is thrown away.
3. Researchers tested seventeen thousand apps. None secretly used the mic.
4. A company that bragged about spying on you? The FTC said it wasn't real.
5. So how do ads know? Your searches, your location, your purchases and your Wi-Fi.
6. Check yourself. Orange dot means microphone.
7. Green means camera.
8. Swipe down to see the app.
9. Settings, Privacy, Microphone.
10. Switch off what doesn't need it.
11. Follow for more tech you can trust.

Sources for descriptions: Apple Machine Learning Research (Hey Siri voice trigger); Google Assistant privacy blog/support; Northeastern University 2018 news release; FTC (Cox Media Group, check); Mozilla, EFF, EPIC on ad tracking; Apple and Google support pages on indicators.
