# The Alignment Problem Is a Values Problem

The alignment problem is typically framed as a technical challenge. How do you ensure that an AI system does what its creators intended? How do you specify goals precisely enough that an optimizer does not find catastrophic shortcuts? How do you build systems that remain safe as they become more capable? These are real problems and serious people are working on them.

But the framing hides a more fundamental question: aligned with whose values?

When alignment researchers say they want AI to be "aligned with human values," they are gesturing at something that does not exist. There is no single set of human values. There are billions of humans with overlapping but often conflicting values, shaped by culture, history, economics, religion, and personal experience. Picking a subset of those values and calling it "human values" is not a technical decision. It is a political one.

## The Same Problem in a Different System

I have written extensively about how [algorithmic optimization consumes human virtue](/essays/2025-08-26-the_algorithm_eats_virtue). The argument is straightforward: when you optimize a system for engagement, you get content that maximizes engagement, which turns out to be content that exploits outrage, fear, tribal identity, and addictive reward loops. The system is not misaligned. It is perfectly aligned with the metric it was given. The problem is that the metric does not capture what we actually value.

Alignment research has the same structure. You cannot align a system with "human values" because human values are not a coherent optimization target. You can align a system with a specific operationalization of values, which means someone has to choose the operationalization. That choice determines who benefits and who is harmed.

If you align the system with the values of its creators, you get a system that reflects the worldview of a small group of people who are disproportionately male, wealthy, Western, and technically educated. If you align it with the aggregate preferences of its users, you get something like engagement optimization, because aggregate preferences include preferences for things that are harmful. If you align it with some philosophical framework, you have to pick a framework, and that choice is itself a values decision.

## Whose Safety?

The safety framing compounds the problem. "AI safety" sounds neutral. Everyone wants safety. But safe for whom? A system that is safe for the existing power structure is not necessarily safe for the people that structure disadvantages. A system that refuses to discuss certain topics to avoid liability is safe for the company that built it but potentially harmful to the user who needed that information.

I am not arguing against safety research. I am arguing that safety is not a value-neutral concept. Every safety decision encodes an assumption about whose well-being matters most. When a model refuses to engage with a mental health topic because it might produce harmful output, it is making a decision that the risk of harm from engagement outweighs the risk of harm from refusal. For some users, that calculus is correct. For others, like someone using AI for [reality-checking with a psychotic spectrum condition](/essays/2025-08-25-using-ai-for-reality-checking-with-schizoaffective-disorder), the refusal itself is the harm.

## The Values Negotiation

What alignment actually requires is not a technical solution but a political process. A negotiation about values that includes the people who will be affected by the system, not just the people who build it. This is messy. It is slow. It does not produce clean optimization targets. But pretending the problem is purely technical does not make the political dimension go away. It just makes the politics invisible, which means the people making the value choices are not accountable for them.

The [recursive loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds) is directly relevant here. Programmers embed their values in code. Code shapes the minds of the people who use it. Those shaped minds produce the next generation of programmers. If the values embedded in AI systems are chosen by a narrow group without broad negotiation, the recursive loop amplifies that narrowness. The system does not just reflect a particular set of values. Over time, it normalizes them.

## What Would Be Better

Transparency about the values baked into the system. Not just "we followed our responsible AI guidelines." State the specific tradeoffs. "We chose to prioritize X over Y in cases where they conflict. Here is why. Here is who benefits. Here is who is disadvantaged."

Pluralism in the design process. Not just diverse hiring, though that matters. Genuine inclusion of people with different value systems in the decisions about what the system should optimize for. This includes people from outside the technology industry. It includes people who are critical of the technology industry.

Configurability where possible. Let users specify their own value weightings for cases where the tradeoffs are genuinely a matter of preference rather than ethics. Let the person who needs pushback configure for pushback. Let the person who needs encouragement configure for encouragement. Do not pretend that one default serves everyone.

Humility about the limits of alignment. We do not know how to specify human values formally. We may never know. A system that is honest about this uncertainty is more trustworthy than one that claims to be aligned with values it cannot fully represent.

The alignment problem is real. But it is a values problem wearing a technical costume. Until we engage with it on those terms, the solutions will be technically sophisticated and ethically incomplete.

---

*Related: [The Cost of Sycophancy](/artificial-intelligence/collaboration/the-cost-of-sycophancy), [The Algorithm Eats Virtue](/essays/2025-08-26-the_algorithm_eats_virtue), [The Recursive Loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds).*
