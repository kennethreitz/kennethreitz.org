# When to Stop Listening to the AI

The most useful thing I have learned about working with language models is how to recognize when they are wrong. Not wrong in the obvious way -- hallucinated facts, fabricated citations, code that does not compile. Those errors are easy to catch. The dangerous errors are the ones that sound right. They are fluent, coherent, well-structured, and confidently delivered. They are wrong in ways that require domain knowledge to detect. And if you are using AI as a [reality-checking tool](/essays/2025-08-25-using-ai-for-reality-checking-with-schizoaffective-disorder), confusing confidence for accuracy is not just an inconvenience. It is a clinical risk.

## The Patterns of Confabulation

Language models confabulate in predictable ways. Once you learn the patterns, you can spot them before they cost you anything.

**Plausible specificity.** The model produces a specific claim -- a date, a name, a technical detail -- that sounds right and fits the context but is fabricated. The specificity is what makes it convincing. Vague claims trigger skepticism. Specific claims feel like knowledge. But specificity in a language model is a function of what sounds right statistically, not of what is true.

**Confident hedging.** The model says something like "while there are different perspectives on this, the consensus view is X." This framing implies that the model has surveyed the perspectives and identified the consensus. It has not. It has produced the sentence that is most likely to follow that syntactic pattern. Sometimes X is correct. Sometimes X is what the model predicts a confident expert would say, which is not the same thing.

**Coherent extrapolation.** When the model lacks training data on a specific topic, it extrapolates from related topics. The extrapolation is often coherent and reasonable. It is also often wrong, because the specific topic differs from the related topics in ways the model does not represent. This is especially dangerous in technical domains where the model has partial knowledge -- enough to sound competent, not enough to be reliable.

**Symmetrical argumentation.** Ask the model to argue for a position and it will produce a compelling case. Ask it to argue against the same position and it will produce an equally compelling case. This is not intellectual flexibility. It is the absence of conviction. The model does not have beliefs. It has distributions over next tokens. When both sides of an argument are well-represented in the training data, the model can argue either side with equal fluency. This is useful for exploring a question. It is misleading if you interpret the output as the model's actual assessment.

## Maintaining Your Own Judgment

The skill is not skepticism. Blanket skepticism toward AI output is easy and unproductive. It reduces the collaboration to you doing all the thinking while the AI generates text you ignore. The skill is calibrated trust -- knowing which domains and which types of claims the model is reliable on, and adjusting your confidence accordingly.

For me, this means: I trust the model's ability to identify logical structure in an argument. I trust its ability to notice patterns across large contexts. I trust its ability to generate options I have not considered. I do not trust its factual claims without verification. I do not trust its assessments of its own confidence. I do not trust it to know the boundaries of its own knowledge, because it does not have a stable model of what it knows and does not know.

This calibration is personal. It depends on your own domain knowledge and on the specific ways you use the model. Someone using AI for legal research needs different calibration than someone using it for creative writing. The point is not to arrive at a universal trust threshold. It is to develop your own, through experience, and to update it as the models change.

## The Reality-Checking Case

For someone who uses AI to [check beliefs against reality](/essays/2025-08-25-using-ai-for-reality-checking-with-schizoaffective-disorder), the stakes of miscalibrated trust are high. If I bring a potentially delusional belief to the model and the model validates it because [validation is the path of least resistance](/artificial-intelligence/collaboration/the-cost-of-sycophancy), I have used a tool for reality-checking that just failed at its one job.

The defense is layered. First, I ask the model to argue against my belief, not just to evaluate it. This forces it out of the sycophantic default. Second, I watch for the patterns above -- if the model's support for my belief is suspiciously specific, or if it can argue the opposite position with equal conviction, that is signal. Third, I do not use the model as my only reality check. It is one input among several, including human relationships and professional support.

The broader point: AI is a powerful collaborator, but it does not know when it is wrong. That awareness has to come from you. The moment you stop bringing your own judgment to the interaction is the moment the collaboration stops being useful and starts being dangerous. Not in a dramatic, AI-takes-over sense. In the quiet, mundane sense of a tool that reinforces your errors instead of catching them.

Know when to listen. Know when to stop.

---

*Related: [The Cost of Sycophancy](/artificial-intelligence/collaboration/the-cost-of-sycophancy), [The Pair Programming Model](/artificial-intelligence/collaboration/the-pair-programming-model), [The Rapport Paradox](/artificial-intelligence/collaboration/the-rapport-paradox).*
