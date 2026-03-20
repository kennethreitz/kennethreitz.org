# The Context Window as Working Memory

A language model can only think about what fits in its context window. Everything else does not exist for it. There is no background awareness, no subconscious, no vague sense that something relevant happened earlier. If the information is not in the window, it is not part of the computation. The boundary is absolute.

Human working memory is not as sharp, but the principle is the same. George Miller's famous estimate was seven items, plus or minus two. More recent research suggests the number is closer to four. You can hold about four chunks of information in active awareness at any given moment. Everything else is in long-term memory, which requires retrieval, which is lossy, which is biased, which fails in ways you do not notice.

The parallel is imperfect. Humans have long-term memory. Language models, in their basic form, do not. Humans can be primed by context they are not consciously aware of. Language models cannot. But the core constraint is shared: there is a finite space for active thought, and everything about how you think is shaped by what fits in that space and what does not.

What interests me is how both systems cope with the limitation.

Language models cope through architecture. The attention mechanism allows every token in the context window to attend to every other token, extracting maximum information from the available context. Techniques like retrieval-augmented generation simulate long-term memory by fetching relevant documents and injecting them into the context window. The model itself does not remember. External systems remember on its behalf and present the results as if they were always there.

Humans cope through chunking. You cannot hold the digits 1, 4, 9, 2 as four separate items and also hold 1, 7, 7, 6 as four separate items. But if you chunk them into "1492" and "1776," two historical dates, you have used two slots instead of eight. Expertise is, in large part, the ability to chunk more efficiently, to see patterns where novices see individual pieces. A chess grandmaster does not hold individual piece positions in working memory. They hold configurations, familiar patterns that compress dozens of positions into single chunks.

Both coping strategies are forms of compression. The question is always: given the finite space, what do you keep and what do you lose?

This is where it gets personal.

I have schizoaffective disorder. One of the less discussed symptoms is the effect on working memory. During episodes, my working memory degrades. The number of items I can hold simultaneously drops. The chunking becomes less efficient. I lose the thread of conversations. I start sentences and forget where they were going. I open a file to make an edit and cannot remember what the edit was supposed to be.

This is what it feels like to have a smaller context window. Not just forgetting things, but losing the ability to hold enough pieces of the current situation in mind to act coherently within it. The world does not change. Your capacity to model it does.

Using AI when my working memory is compromised is, in a concrete sense, extending my context window. I can put information into the conversation that I would otherwise lose. Claude holds the thread when I cannot. This is not a metaphor. It is the literal function of the context window: holding information in active computation that would otherwise be unavailable.

The context window also forces prioritization, and this is where the analogy becomes instructive. When the window fills up, something has to go. In language models, this is typically handled by truncating the oldest context or by summarizing earlier portions. In humans, the process is less orderly. Under cognitive load, you do not get to choose what drops out of working memory. Stress, fatigue, and psychiatric symptoms all bias what you retain and what you lose, often in unhelpful directions.

What both systems reveal is that thought is fundamentally constrained by bandwidth. Not by intelligence, not by knowledge, but by how much you can hold in active consideration at once. A brilliant model with a tiny context window will produce worse output than a mediocre model with a large one, if the task requires integrating information across a wide span. The same is true of humans. The smartest person in a state of severe cognitive depletion will be outperformed by an average person who is rested and focused.

This is not a comfortable insight. We like to think of intelligence as a fixed property, something you have. Context window theory suggests it is more like a resource, something you spend. And like any resource, it can be depleted, extended, managed well or poorly.

The practical takeaway is simple. If you are working with AI, give it the context it needs. Do not assume it knows what you have not told it. If you are working with yourself, respect the limits of your own context window. Write things down. Use external memory. Do not rely on your ability to hold everything in your head, because you cannot. Nobody can.

---

*This piece connects to [The Context Window Mind](/essays/2025-09-09-the_context_window_mind_how_ai_thinks_only_when_spoken_to), [Using AI for Reality-Checking with Schizoaffective Disorder](/essays/2025-08-25-using-ai-for-reality-checking-with-schizoaffective-disorder), and [Your Phone Is Part of Your Mind](/essays/2025-09-04-your_phone_is_part_of_your_mind).*
