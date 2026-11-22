# EP05 long video: ChatGPT Doesn't Know What It's Going to Say Next (How AI Really Works)
Draft for owner approval (22 Nov 2026). Target ~7:30 (~1,130 words). Voice: vidIQ ElevenLabs "Eric" (one voice for the whole video).
Look: cream theme, new background pattern. PICTURE SCENES (owner rule): every line acted out with animated illustrations (Fluent Emoji library + HyperFrames blocks such as ai-chat-reveal, flowchart, exploded-stack); text cards only for hard numbers. Max at key moments ★, Bit as "the AI".
Teaser Short already made and scheduled: ai01 "ChatGPT doesn't know what it's going to say next" (1 Dec).
Title options: "ChatGPT Doesn't Know What It's Going to Say Next" · "How ChatGPT Actually Works (In 8 Minutes)" · "ChatGPT Is Just Guessing. Here's Why It Works So Well"

## 1. Hook ★ Max
PICTURE: Max at a laptop types "Write a poem about chai". Bit's thought bubble shows a spinning roulette wheel of words; one word lands, drops into the chat, then the wheel spins again for the next word.
1. Right now, as ChatGPT writes its answer to you, it has no idea how its own sentence is going to end.
2. It doesn't plan the paragraph. It doesn't even plan the next sentence. It picks one small piece of a word, then the next, then the next.
3. And yet about a billion people use it every week, to write emails, fix code and explain homework.
4. So how can something that is basically guessing, one word at a time, sound so smart? Let's open the box.

## 2. Words become tokens
PICTURE: a sentence "ChatGPT is unbelievable" slides onto a conveyor belt; scissors snip it into coloured blocks "Chat", "G", "PT", " is", " un", "believ", "able". Each block gets a number tag stamped on it.
5. First, ChatGPT doesn't actually read words. It reads tokens.
6. A token is a chunk of text. Sometimes a whole word, sometimes just a piece of one. On average, a hundred tokens make about seventy-five English words.
7. Every token is turned into a number, because underneath it all, the model can only do maths.
8. This one detail explains a famous fail. For a long time, chatbots insisted the word "strawberry" has only two R's.
PICTURE: a strawberry; the word "strawberry" splits into two tokens "straw" + "berry"; Bit squints at the blocks and holds up two fingers; then a magnifier reveals s-t-r-a-w-b-e-r-r-y with three R's glowing.
9. Why? Because the model never saw the letters. It saw a couple of token chunks, like "straw" and "berry", each one just a number.
10. Counting letters inside those chunks is surprisingly hard for it, a bit like counting the letters in a word you only ever heard spoken. Newer models that work step by step usually get it right.
11. So when you type a question, ChatGPT sees a long row of numbers. And its only job is to answer one question about them.

## 3. The guessing game
PICTURE: phone keyboard autocomplete: "I'll be there in" → three suggestion chips "5", "10", "a". Then a giant version: a bar chart of possible next words with probabilities; a dice rolls and picks one.
12. What token is most likely to come next?
13. You already know this trick. It's the autocomplete on your phone keyboard. Type "I'll be there in", and it suggests "five minutes".
14. ChatGPT is that same idea, scaled up enormously. For every next token, it calculates a probability for tens of thousands of options.
15. Then it picks one, adds it to the text, and does the whole thing again. Word, by word, by word.
16. That's also why you can ask the same question twice and get two different answers. ChatGPT usually doesn't take the single most likely token. It rolls the dice a little, so the writing sounds natural instead of robotic.
PICTURE: two Max laptops side by side, same question, different answers appear.

## 4. It re-reads everything
PICTURE: a long chat scroll; every time Bit adds one word, a spotlight sweeps back over the whole conversation; lines connect the word "it" back to "the laptop" in an earlier sentence.
17. And here's something most people don't realise. Every single time ChatGPT adds one token, it looks back over the entire conversation so far.
18. Your question, its own earlier words, everything. That's how it keeps track of what "it" or "that" refers to.
19. The technique that makes this possible is called attention. It was introduced by Google researchers in twenty seventeen, in a paper called "Attention Is All You Need". It's the T in GPT: the transformer.
20. Attention lets the model decide which earlier words matter most for the next one. In "I dropped my laptop and now it won't start", attention links "it" back to "laptop", not "I".
21. But there's a limit to how much it can look back on, called the context window. In a very long chat, the earliest details can get less attention, or fall out completely. That's why it sometimes forgets what you said at the start.
PICTURE: a window frame sliding along the chat scroll; the oldest messages fade out on the left.

## 5. How it learned ★ Max
PICTURE: Bit sits in a gigantic library; books fly off the shelves into Bit; a fill-in-the-blank card "The capital of India is ___" appears, Bit guesses "Mumbai" (red ✗), a dial turns, guesses "New Delhi" (green ✓).
22. But how does it know which guesses are good? It learned by reading. An enormous amount of reading.
23. During training, the model is shown huge amounts of text from books, websites and code, with the next word hidden.
24. It guesses. It checks the real answer. And it adjusts itself a tiny bit to guess better next time.
25. Those adjustable parts are called parameters. Think of them as knobs. GPT-3, back in twenty twenty, had a hundred and seventy-five billion of them.
PICTURE: a wall of tiny knobs zooms out until it becomes a galaxy of dots; counter "175,000,000,000".
26. Repeat that guessing game billions of times, and something surprising happens. To predict the next word well, the model has to pick up grammar, facts, styles, and even some reasoning patterns along the way.

## 6. From parrot to assistant
PICTURE: a raw model as a parrot repeating random internet text; then a row of people (labelers) holding score cards ranking two answers, "Answer A 👍", "Answer B 👎"; the parrot turns into Bit wearing a helper badge.
27. A model trained only on the internet is a bit like a very well-read parrot. Ask it a question, and it might just continue your sentence, or ramble.
28. So companies add a second stage. Real people write good example answers, and rank the model's answers from best to worst.
29. The model is then trained to produce the kind of answers people prefer. This is called reinforcement learning from human feedback.
30. And it matters a lot. In OpenAI's twenty twenty-two study, people preferred answers from a small model trained this way over the giant GPT-3, a model a hundred times bigger.
PICTURE: a small robot on a podium with a gold medal; a huge robot beside it with silver.

## 7. Why it makes things up ★ Max
PICTURE: a student at an exam desk; a multiple-choice sheet; the student shrugs and ticks a random box; score "+1" for a lucky guess, "0" for "I don't know". Then Bit confidently says "Max's birthday is 12 March!" with a red "HALLUCINATION" stamp.
31. Now here's the catch. Remember, its job is to produce a likely-sounding next word, not a true one.
32. Most of the time, likely and true are the same thing. But when the model doesn't really know, it can still produce something that sounds perfectly confident. That's called a hallucination.
33. OpenAI researchers compared it to a student on a multiple-choice exam. If you get zero points for saying "I don't know", guessing always looks smarter.
34. And many of the tests used to grade AI models work exactly like that. They reward a lucky guess more than an honest "I'm not sure".
35. That's why rare facts are where it slips most: a specific date, a small company's details, a quote from a person who isn't famous. There's no strong pattern to predict from.

## 8. So does it understand anything?
PICTURE: a balance scale; on the left a brain, on the right a calculator; the scale wobbles and doesn't settle. Two groups of tiny scientists argue on either side.
36. So is ChatGPT just fancy autocomplete, or does it actually understand?
37. Honestly, researchers still disagree. It clearly isn't thinking the way you do. It has no memory of your life and no experience of the world.
38. But predicting text really well turns out to require surprisingly deep patterns. That's why it can explain code, translate languages and solve problems it has never seen word for word.
39. A useful way to think about it: it's an incredibly well-read prediction machine. Powerful, but not a source of truth on its own.

## 9. How to get better answers ★ Max
PICTURE: four tip cards, each acted out: (1) Max hands Bit a folder labelled "context"; (2) Bit raises a hand saying "I'm not sure"; (3) a magnifying glass checks a source link; (4) a staircase "step 1, step 2, step 3".
40. Once you know how it works, you can use it much better. Here are four habits.
41. One. Give it context. The more relevant details you put in, the better its predictions become. "Write an email" is weak. "Write a polite email to my manager asking for Friday off" is strong.
42. Two. Give it permission to say "I don't know". Simply adding that one line to your question can reduce confident made-up answers.
43. Three. Check anything that matters. Facts, numbers, dates, legal or medical advice. Ask for sources, then open them yourself.
44. Four. For hard problems, ask it to work step by step. Writing out the steps gives the model more text to build on before it reaches the answer.

## 10. Close ★ Max
PICTURE: Max and Bit side by side at the laptop; the roulette wheel of words slows and lands on "decoded". End screen.
45. So, ChatGPT doesn't know what it's going to say next. It predicts it, one token at a time, using patterns from an enormous amount of human writing.
46. That's what makes it so useful, and also why you should never switch your own brain off.
47. If you want to see what happens when an AI like this gets tricked by a webpage, watch this video next.
48. And subscribe to TechDecoded with Max for more tech, decoded.

---

## Fact sheet
| Line | Claim | Source |
|---|---|---|
| 3 | ~1 billion weekly users (OpenAI, Sept 2026; 900M in Feb 2026) | https://techcrunch.com/2026/02/27/chatgpt-reaches-900m-weekly-active-users · https://thenextweb.com/news/chatgpt-1-billion-weekly-active-users-openai-target |
| 6 | ~100 tokens ≈ 75 English words (OpenAI tokenizer guidance) | https://platform.openai.com/tokenizer |
| 8–10 | Chatbots miscounting the R's in "strawberry"; tokens hide letters; step-by-step/reasoning models do better | https://techcrunch.com/2024/08/27/why-ai-cant-spell-strawberry · https://arxiv.org/pdf/2412.18626 |
| 12–15 | Next-token prediction; generation loop; a probability for every vocabulary entry (GPT-2 vocabulary: 50,257 tokens) | https://sebastianraschka.com/faq/docs/next-token-prediction.html · https://huggingface.co/blog/alonsosilva/nexttokenprediction |
| 16 | Sampling instead of always taking the top token | https://dev.to/pudgycat/how-do-llms-work-tokens-attention-and-next-word-prediction-explained-1kmh |
| 17–21 | Attention and the transformer (Vaswani et al., Google, 2017); context window limits | https://arxiv.org/abs/1706.03762 |
| 23–24 | Pretraining = predicting the next word in huge amounts of text | https://openai.com/index/why-language-models-hallucinate/ |
| 25 | GPT-3: 175 billion parameters (2020) | https://arxiv.org/pdf/2005.14165 |
| 28–30 | InstructGPT/RLHF: labelers write demonstrations and rank outputs; 1.3B InstructGPT preferred over 175B GPT-3 | https://openai.com/index/instruction-following/ · https://arxiv.org/abs/2203.02155 |
| 31–35 | Hallucinations: plausible but false; training and evals reward guessing; arbitrary low-frequency facts | https://openai.com/index/why-language-models-hallucinate/ |
| 36–39 | "Researchers disagree" framing; not a source of truth | Commentary, presented as such |
| 41–44 | Prompting habits | General guidance; "can reduce" wording, no number claimed |
Illustrations (roulette wheel, library, exam, knobs, parrot) are metaphors. "Bit" stands in for the AI. The birthday example is fictional.
