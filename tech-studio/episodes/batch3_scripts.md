# Shorts batch 3: scripts for approval (about 45–55 s each, spoken subscribe line at the end)

## upi01: Your UPI money doesn't actually move (in those 2 seconds)
1. Your money doesn't actually move when you pay by UPI.
2. Not in those two seconds, anyway.
3. You scan a QR code at a tea stall. Your app sends the request to its bank.
4. That bank passes it to NPCI, the switchboard that sits between every UPI bank in India.
5. NPCI looks up the UPI ID, like name@bank, and finds which bank account it points to.
6. Then it asks your bank one question: does this person have the money?
7. Your bank checks your PIN and your balance, and takes the amount out of your account.
8. NPCI tells the shopkeeper's bank, which adds it to their account. Ding. Paid.
9. The banks settle the real money between themselves later, in batches.
10. And the scale is wild: in August 2026, UPI handled 24.5 billion payments in a single month.
11. That's about nine thousand payments every second.
12. Subscribe to TechDecoded with Max for more tech, decoded.

Visuals: QR scan → animated payment route (app → bank → NPCI switch → bank) with packets flying · UPI-ID lookup card · "enough money?" check · two ledgers updating · settlement batch truck · rolling counter 24,510,000,000 · per-second ticker.
Sources: NPCI data via Inc42 (24.51 bn, Aug 2026) https://inc42.com/buzz/upi-transactions-rise-4-mom-to-record-24-51-bn-in-august/ · Razorpay, how UPI works https://razorpay.com/blog/what-is-upi-and-how-it-works/ · ByteByteGo, UPI https://bytebytego.com/guides/unified-payments-interface-upi-in-india/

## ai01: ChatGPT doesn't know what it will say next
1. ChatGPT doesn't know what it's going to say next.
2. Not even the next word.
3. Every reply is built one small piece at a time. Those pieces are called tokens.
4. A token is often a whole word, sometimes just part of one. In English, a token is roughly three quarters of a word.
5. At every step, the model scores every token it knows, tens of thousands of them, and gives each one a probability.
6. After "The sky is", "blue" gets a high score. "Banana" gets almost nothing.
7. It picks one, adds it to the sentence, and does the whole thing again. And again. And again.
8. A long answer can mean hundreds of these predictions in a few seconds.
9. So how does it sound so smart? It learned those probabilities from a huge amount of text.
10. It isn't looking up an answer. It's predicting one, token by token.
11. That's also why it can sound confident and still be wrong.
12. Subscribe to TechDecoded with Max for more tech, decoded.

Visuals: chat bubble typing → text splits into coloured token blocks · probability bar race for the next token ("blue" 62% / "clear" 18% / "banana" 0.01%, labelled illustrative) · loop arrow appending tokens · counter of predictions · "confident ≠ correct" stamp.
Sources: OpenAI, What are tokens https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them · Hugging Face, next-token prediction https://huggingface.co/blog/alonsosilva/nexttokenprediction · Raschka, next-token prediction https://sebastianraschka.com/faq/docs/next-token-prediction.html

## del01: Deleting a file doesn't delete it
1. When you delete a file, your computer doesn't actually delete it.
2. At least, not on an old hard drive.
3. Deleting only removes the file's entry from the drive's index, like tearing a line out of a book's contents page.
4. The data itself is still sitting there. The space is just marked as free.
5. It stays until new files are written over it. That's how recovery tools bring files back.
6. And it's why selling an old hard drive without wiping it is risky.
7. Modern SSDs are different. When you delete, your computer sends a command called TRIM.
8. It tells the drive those blocks aren't needed, and the drive clears them in the background.
9. So on most new laptops, a deleted file can be truly gone within moments.
10. The lesson: on an old hard drive, delete isn't erase. On an SSD, delete is almost forever. Back up what matters.
11. Subscribe to TechDecoded with Max for more tech, decoded.

Visuals: file into the bin → book contents page, one line torn out · disk-sector grid with the file's blocks still lit, marked FREE · recovery-tool scan bringing it back · "SOLD" hard drive warning · SSD with TRIM sweeping blocks to zero · split ending HDD vs SSD · backup cloud.
Sources: Rossmann Group, what TRIM does https://rossmanngroup.com/technical-reference/what-trim-does-and-why-it-destroys-data · Make Tech Easier, TRIM and recovery https://maketecheasier.com/ssd-trim-makes-file-recovery-hard/

## face01: Your phone checks your face with 30,000 invisible dots
1. Your phone checks your face with thirty thousand invisible dots.
2. On an iPhone, Face ID projects more than thirty thousand infrared dots onto your face. You can't see a single one.
3. An infrared camera reads how those dots land, and builds a 3D map of your face.
4. That's why a printed photo of you can't open it. A photo is flat. Your face isn't.
5. A neural network compares that map with the one saved when you set it up.
6. It also checks that your eyes are open and looking at the screen.
7. Apple says the chance a random stranger unlocks your phone is less than one in a million.
8. The old fingerprint sensor? About one in fifty thousand.
9. The catch: identical twins, and siblings who look very alike, can fool it more often.
10. And your face map never leaves the phone. It's stored in a secure chip, not sent to Apple.
11. Subscribe to TechDecoded with Max for more tech, decoded.

Visuals: face outline → infrared dot grid sweeping across (dots appear only in "IR view") · depth-map mesh build · flat photo bounced off ✗ · eyes-open check · odds counter 1 : 1,000,000 vs 1 : 50,000 · twins card · lock with secure-chip vault.
Sources: Apple, About Face ID advanced technology https://support.apple.com/102381 · Apple Face ID Security Guide https://apple.com/business-docs/FaceID_Security_Guide.pdf · Face ID (overview) https://en.wikipedia.org/wiki/Face_ID
