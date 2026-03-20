# Tokenization Shapes Thought

Before a language model processes a single word, something has already happened that constrains everything it will be able to think. The text has been tokenized, broken into pieces that the model treats as atomic units. These pieces are not words. They are not characters. They are statistically derived chunks that represent the most efficient encoding of the training data, given a fixed vocabulary size.

The tokenizer for a typical large language model uses byte-pair encoding or a similar algorithm. It starts with individual bytes and iteratively merges the most frequently co-occurring pairs until it reaches a target vocabulary size, usually between 32,000 and 100,000 tokens. Common English words get their own tokens. Less common words are split into subword pieces. Very rare words are broken into individual characters or bytes.

This means the model does not see language the way you do. You see the word "understanding." The model might see "under" + "standing" or "understand" + "ing," depending on how the tokenizer was trained. You see a concept. The model sees pieces that have been glued together by statistical frequency in the training corpus.

This matters more than most people realize.

Consider what happens with compound concepts. If a word or phrase is common enough, it gets its own token, and the model can treat it as a single unit with a single learned embedding. The concept is represented as one thing. If the phrase is less common, it gets split across token boundaries, and the model has to reconstruct the meaning from parts. It can do this, transformers are good at composition, but it is an additional computational task that introduces noise. Some concepts are harder for the model to think about, not because they are inherently complex, but because they happen to straddle token boundaries.

Now consider the politics.

Tokenizers are trained on data that is overwhelmingly English. The byte-pair merges that form the vocabulary reflect the statistical structure of English text. Common English words are efficient to represent. They compress well. A language like Tibetan or Yoruba, which appears less frequently in the training data, gets a worse deal. Words in those languages are split into more tokens, which means they consume more of the context window, which means you can fit less text in the model's working memory, which means the model is literally less capable in those languages. Not because the architecture is biased, but because the tokenizer is.

The same applies to technical jargon, to slang, to neologisms, to the specialized vocabularies of marginalized communities. If your language was well-represented in the corpus the tokenizer was trained on, the model can think about your concepts efficiently. If it was not, the model has to work harder and has less room to work in.

This is not a conspiracy. It is a consequence of statistical optimization applied to unequal data. The tokenizer does not know or care about linguistic justice. It finds the most efficient encoding of its training distribution and implements it. The training distribution reflects who has produced the most digitized text, which reflects who has had access to computers, the internet, education, and the leisure to write. The tokenizer encodes the inequality and passes it forward as a structural constraint on what the model can think.

There is a parallel to human cognition that I find uncomfortable. The language I was raised in shapes what I can easily think. The concepts my culture names are the concepts I can readily manipulate. The experiences my community does not have words for are the experiences I struggle to articulate, even to myself. Cognitive linguistics has been making this argument for decades: the structure of your language is not just a medium for thought. It is a constraint on thought.

I have schizoaffective disorder, and I can tell you that some of the most important experiences of my life are ones that my language handles poorly. The specific texture of a psychotic episode. The way reality feels different, not just wrong but differently organized. English gives me "hallucination" and "delusion," words that encode the experience as deficit. Other frameworks might tokenize that experience differently, might give it different boundaries that reveal different structure. But I am stuck with the vocabulary I have, and the vocabulary shapes what I can communicate, which shapes what others can understand, which shapes how I am treated.

Language models have the same problem, just more visibly. Their constraints are written in a tokenizer file you can inspect. Ours are written in neural pathways we cannot see. Both shape thought before thinking begins.

---

*This piece connects to [The Language Model Is the Message](/essays/2026-03-06-the_language_model_is_the_message), [Language as Operating System](/essays/2025-09-11-language_as_operating_system_the_shared_runtime_for_consciousness), and [Consciousness as Linguistic Phenomenon](/essays/2025-08-28-consciousness-as-linguistic-phenomenon).*
