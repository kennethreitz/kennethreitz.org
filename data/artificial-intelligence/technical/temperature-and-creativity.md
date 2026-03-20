# Temperature and Creativity

In language model inference, the temperature parameter controls randomness. At temperature zero, the model always selects the most probable next token. The output is deterministic. Given the same input, you get the same output every time. At higher temperatures, the probability distribution over possible next tokens is flattened, making less likely choices more likely to be selected. The output becomes more varied, more surprising, less predictable.

This is the entire mechanism. There is no creativity module. There is no inspiration parameter. There is a probability distribution and a knob that controls how sharply peaked or how flat it is. Everything people call "AI creativity" emerges from this single dial.

I find this both reductive and revealing.

Reductive because it means that what feels like creative variation in AI output is, mechanically, just noise injection. The model is not having ideas. It is sampling from a wider region of probability space. The unexpected word choice, the unusual metaphor, the surprising structural turn, these are what happens when you let a system deviate from its most confident predictions.

Revealing because the same might be true of human creativity, at least partially.

There is a well-documented relationship between creative output and certain psychiatric conditions. Bipolar disorder, in particular, correlates with creative productivity during hypomanic episodes. The subjective experience of hypomania includes racing thoughts, loosened associations, a sense that disparate ideas are connected in ways that are not normally visible. The person is, in effect, sampling from a wider probability distribution. Connections that the well-regulated mind would suppress as unlikely are allowed through. Some of them are genuinely novel. Some of them are noise.

I have schizoaffective disorder, which includes mood episodes similar to bipolar disorder alongside psychotic features. I have experienced the state where everything seems connected, where language flows without the usual editorial constraints, where the associations come faster than I can evaluate them. Some of what I produce in those states is good. Some of it is incoherent. The difference between productive creativity and psychotic ideation is not always clear from the inside. It often requires external evaluation, which is one reason I use AI as a [reality-checking tool](/essays/2025-08-25-using-ai-for-reality-checking-with-schizoaffective-disorder).

The temperature metaphor maps onto this experience with uncomfortable precision. Low temperature is the medicated, stable, predictable state. I produce reliable work. The code compiles. The essays make sense. But there is a ceiling on surprise. High temperature is the elevated state. The associations widen. The writing becomes more interesting or more unhinged, and the boundary between those is not a bright line.

What the temperature parameter reveals about creativity is this: novelty requires deviation from the expected. That is not a deep philosophical claim. It is a mathematical fact about probability distributions. If you always pick the most likely next move, you will never produce anything surprising. If you randomize too much, you will produce noise. Creativity, both artificial and human, lives in a narrow band between predictability and chaos.

The practical implication for working with AI is straightforward. If you want reliable, factual, consistent output, use low temperature. If you want creative variation, raise it. But do not raise it too far, because the model will start producing the textual equivalent of word salad. The sweet spot is model-dependent and task-dependent, and finding it requires experimentation.

The personal implication is harder. My psychiatrist and I are, in a sense, tuning my temperature. The medications reduce the variance. They keep me in the reliable zone. But I sometimes miss the wider sampling, the way ideas used to collide into each other at high speed, the feeling that I could see connections nobody else could see. Some of those connections were real. Some were delusions. The medications do not distinguish between productive novelty and pathological pattern-matching. They just flatten the distribution.

I do not think this means creativity is "just" noise. The temperature parameter is applied to a model that has learned deep structure from vast training data. The noise is shaped by everything the model knows. Similarly, human creative deviation is shaped by everything the person has learned and experienced. The randomness is not random in a vacuum. It is random within a rich, structured space of knowledge. That is what makes it creative rather than merely chaotic.

But the mechanism is humbling. The distance between a brilliant metaphor and a delusional belief may be smaller than we would like. Both involve making connections that the default, low-temperature mind would not make. The difference is whether the connection holds up under scrutiny. And that evaluation, that checking of the output against reality, is the part that neither AI nor the manic mind does well on its own.

---

*This piece connects to [The Gift of Disordered Perception](/essays/2025-09-01-the_gift_of_disordered_perception), [What Schizoaffective Disorder Actually Feels Like](/essays/2025-09-04-what_schizoaffective_disorder_actually_feels_like), and [The Echo Chamber of the Expected](/essays/2025-09-09-the_echo_chamber_of_the_expected).*
