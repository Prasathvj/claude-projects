# How does AI actually work? (DRAFT, awaiting approval)
Character: plain stickman with big round glasses (Option A) + tiny robot sidekick "Bit" (tech videos only).

## Facts used (searched 2026-11-17; sources are mostly explainers, NOT primary; cite the primary ones in the description)
- LLMs are trained on next-token prediction: given text so far, estimate the probability of the next token (secondary explainers).
- Tokens are not always words: a whole word, a piece of a word, or a character; rare words are split into pieces; some models split numbers digit by digit.
- Training: when the guess is wrong, the weights are nudged slightly in the direction that would have improved it (backpropagation / gradient descent), repeated enormous numbers of times. A model has many billions of numeric parameters (explainers). No specific model numbers used.
- Attention (Vaswani et al., 2017, "Attention Is All You Need"): lets each word be re-read in the light of the other words, so "mole" differs in two sentences; transformers process all tokens at once.
- Generation: pick a token, append it, repeat; settings like temperature change how random the pick is.
- A pretrained model alone is a strong text predictor but not a helpful assistant; fine-tuning, including human ratings (RLHF), steers it toward helpful answers.
- Hallucination: models are optimised for plausible text, not verified truth; RLHF reduces but does not remove it (arXiv survey 2311.05232; TechCrunch).
- Open debate: some researchers (e.g. Yann LeCun) argue next-word prediction alone is a dead end; unresolved. Script says "scientists still argue".
- Primary sources to cite in the description (check links before publishing): "Attention Is All You Need" (arXiv 1706.03762); Google Machine Learning Crash Course; 3Blue1Brown, "Attention in transformers"; arXiv survey on hallucination 2311.05232.
- NOT claimed: specific parameter counts, training-data sizes, hallucination rates, or "AI understands/doesn't understand".

## LONG (about 5:00, ~650 words)
### 1. Hook (0:00)
You ask an AI to write a poem, fix your code, or explain the moon. It answers like it understands. So how does it work? The honest answer is both simpler and stranger than you think. At its core, it guesses the next word. Over and over.

### 2. Autocomplete, but huge (0:25)
You know the suggestions above your phone keyboard. Type "see you" and it offers "soon". That is next-word guessing. A chatbot does the same thing, just with far more power. Give it "The sky is" and it works out that "blue" is very likely, "green" is unlikely, "yellow" is possible at sunset. It does not look anything up. It scores the options.

### 3. Words become tokens (1:00)
First problem: computers do not read words. They read numbers. So the text is chopped into pieces called tokens. A token can be a whole word, a part of a word, or even a single letter. Common words stay whole. Rare words get split into smaller pieces. Each piece gets a number, and from there it is all maths.

### 4. How it learns (1:40)
Now the training. The model is shown huge amounts of text with the next piece hidden, and it guesses. Wrong at first, completely wrong. Then the system measures how wrong it was, and nudges millions of tiny dials, called weights, so that guess would have been a little better. Then the next sentence. And the next. Repeat this an enormous number of times, and those dials, many billions of them, end up holding patterns of grammar, facts and style. Nobody typed the rules in. The patterns were learned.

### 5. The trick that changed everything (2:30)
Early systems read words one by one and forgot the start of the sentence. In 2017 researchers published a paper called Attention Is All You Need. The idea is called attention. Each word gets re-read in light of the other words around it. Take the word "mole". In one sentence it is an animal. In another it is a spot on skin. Attention lets the model look at the neighbouring words and decide which meaning fits. And it reads all the words at once, which makes it fast to train.

### 6. How an answer gets written (3:15)
When you ask a question, the model picks one token, adds it to the text, and then guesses the next one, again and again. Why not always the single most likely word? Settings like temperature add a bit of randomness, which is why asking the same question twice can give two different answers.

### 7. From autocomplete to assistant (3:45)
A model trained only on guessing text is not a helpful assistant. So there is a second stage. People rate the answers, and the model is trained to prefer the ones people judge helpful. This is often called learning from human feedback. That is why chatbots sound polite and follow instructions.

### 8. Why it makes things up (4:10)
Here is the catch. The model is trained to produce text that fits the pattern, not text that has been checked. So sometimes it writes something that sounds right and is false, with a confident voice. People call it a hallucination. Human feedback helps, but does not remove it.

### 9. So is it thinking? (4:30)
Scientists still argue about that. Some say predicting the next word forces a model to learn something real about the world. Others say it is not enough on its own. Nobody has settled it, and anyone who sounds completely sure is guessing.

### 10. What to do with this (4:45) [tip card]
Use it as a fast helper, not as a judge. Check important facts, like medicine, money and legal questions, with a reliable source. Ask it to explain its steps, and check them. And remember: it is a very good guesser of what comes next.

### 11. Recap (5:00)
Words become tokens. Training nudges billions of dials. Attention reads words in context. It writes one piece at a time, and it can be confidently wrong. Follow for the next one: how a website actually loads.

## SHORT (about 50 s, ~120 words, V1-V10)
1. You ask an AI anything, and it answers. How? It guesses the next word.
2. Like phone autocomplete, but huge. "The sky is" and the likely word is "blue".
3. Computers can't read words, so text is chopped into tokens: pieces of words, turned into numbers.
4. It learns by guessing the next piece, getting it wrong, and nudging billions of tiny dials.
5. After many rounds, those dials hold patterns of grammar, facts and style.
6. Attention lets it read each word in context: mole the animal, or mole on skin?
7. Then it writes one piece at a time, which is why answers can differ.
8. People rate answers, so it learns to be helpful.
9. But it aims for text that sounds right, not text that is checked. So it can be confidently wrong.
10. Follow for more tech, explained.

Description sources: Vaswani et al., "Attention Is All You Need" (arXiv 1706.03762); Google Machine Learning Crash Course; 3Blue1Brown, "Attention in transformers"; arXiv 2311.05232 (hallucination survey). Verify links before publishing.

## ADDED CHAPTERS (verified 2026-11-17, explainers; no vendor figures)
- After ch.4: WORKED EXAMPLE. "The cat sat on the ___": show illustrative scores (mat 40%, sofa 20%, floor 15%...). Label on screen: ILLUSTRATIVE NUMBERS. A guess comes from scores over many tokens.
- After ch.6: CONTEXT WINDOW. The maximum amount of text, counted in tokens, the model can consider at once; it includes your question, the earlier conversation and the reply it is writing. Rule of thumb: 1,000 tokens is about 750 English words. Limits differ by model, so check the provider. Past the limit, older text can be dropped or the request rejected, depending on the system.
- After ch.7: WHAT IS INSIDE THE BOX. Training is a huge amount of the same simple maths (multiplying big tables of numbers). A GPU has thousands of small cores that do many of these at once, a CPU has a few strong cores. Big models are split across many GPUs, in data centres. Memory speed can be a limit. NOT claimed: dollar costs, GPU counts, energy figures.
- Length becomes about 6:30.
