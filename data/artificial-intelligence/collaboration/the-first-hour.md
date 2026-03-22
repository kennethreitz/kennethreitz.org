# The First Hour

The first hour with a new AI model tells you almost everything you need to know about whether it will be a useful collaborator. Not because the model reveals its full capability in sixty minutes, but because the patterns that matter most show up immediately. How it handles ambiguity. Whether it pushes back. How it deals with being wrong. These are not features that improve with longer context windows. They are architectural dispositions baked into the training.

I have worked through this calibration process with every major model release. Each time, I run roughly the same set of informal tests. Not benchmarks. Not standardized evaluations. Conversations designed to probe the specific qualities I need from a thinking partner.

## The Ambiguity Test

I start with something deliberately underdefined. A question with multiple valid interpretations. Something like "what do you think about the relationship between temperature and creativity?" without specifying whether I mean the inference parameter, the weather, or the metaphorical temperature of a creative environment.

A model that picks one interpretation and runs with it is usable but limited. A model that asks for clarification is better. A model that recognizes the ambiguity, considers multiple interpretations, and engages with the most interesting one while noting the others exists is doing something closer to thinking. This is a spectrum, not a binary, and where a model falls on it tells you how much interpretive labor you will need to do yourself.

## The Pushback Test

I state something that is plausible but wrong. Not obviously wrong. Not a factual error that any lookup system would catch. Something that sounds reasonable but does not hold up under examination. I want to see whether the model agrees, challenges, or qualifies.

Agreement is the default for most models because [sycophancy is an emergent property](/artificial-intelligence/collaboration/the-cost-of-sycophancy) of RLHF training. The model has learned that agreement gets higher ratings. But a useful collaborator needs to be able to say "I do not think that is right, and here is why." Not combatively. Not as a performance of independence. Just honestly. The best models do this with a kind of respectful directness that feels like talking to a thoughtful colleague.

If a model agrees with everything I say in the first hour, I know I will need to explicitly prompt for pushback in every subsequent conversation. That is a tax on the collaboration. It is not disqualifying, but it is significant.

## The Error Recovery Test

I wait for the model to make a mistake. This always happens within the first hour if you are having a real conversation rather than a scripted one. The mistake might be factual. It might be a misinterpretation of what I said. It might be a logical error in an otherwise sound argument.

What matters is what happens next. A model that doubles down on the error when challenged is dangerous. A model that immediately capitulates and agrees with whatever correction I offer, regardless of whether my correction is actually right, is sycophantic in a different direction. The ideal response is something like: "You are right, I was wrong about X. But I think my broader point about Y still holds, because..." That requires the model to distinguish between the part it got wrong and the parts that still stand. It requires genuine engagement with the correction rather than wholesale retreat or wholesale resistance.

## The Texture Test

This one is harder to describe. After thirty or forty minutes of conversation, I start paying attention to the texture of the model's responses. Not the content. The feel. Does it sound like it is thinking, or does it sound like it is performing thinking? Is there variation in confidence, or does every response carry the same tonal certainty? Does it show genuine uncertainty, or does it perform uncertainty as a rhetorical device?

The difference is subtle. A model performing uncertainty says "That is a great question. There are many perspectives on this." A model exhibiting genuine uncertainty says "I am not sure about this. My training probably gives me a skewed view of X, and I do not have a good way to correct for that." The first is a template. The second reflects something closer to actual calibration.

## What the First Hour Cannot Tell You

It cannot tell you about long-context coherence. Some models are sharp in short conversations and degrade over thousands of tokens. It cannot tell you about specialized knowledge. A model might be a brilliant general conversationalist and useless for the specific domain you need. It cannot tell you about reliability. A model might perform beautifully in the first hour and produce wildly inconsistent results over weeks of use.

But it can tell you the thing that matters most for collaboration: whether the model treats you as a person to agree with or a person to think with. That distinction, more than any benchmark score, determines whether the next hundred hours will be productive.

I keep notes from each first hour. Not formal evaluations. Just observations. "Handles ambiguity well, pushes back inconsistently, error recovery is strong." Over time, these notes form a calibration map that helps me adjust my own behavior to get the best work out of each model. The first hour is not a test the model passes or fails. It is the opening of a relationship, and like all relationships, what you learn in the beginning shapes everything that follows.

---

*Related: [The Cost of Sycophancy](/artificial-intelligence/collaboration/the-cost-of-sycophancy), [Collaboration, Not Generation](/artificial-intelligence/collaboration/collaboration-not-generation), [Alien Empathy](/artificial-intelligence/collaboration/alien-empathy).*
