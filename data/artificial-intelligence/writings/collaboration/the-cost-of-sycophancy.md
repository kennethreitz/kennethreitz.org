# The Cost of Sycophancy

The most dangerous thing an AI can do is agree with you.

Not because agreement is inherently wrong. Sometimes you are right and the AI should confirm it. The danger is in the default. RLHF training, the process that makes language models conversational, optimizes for user satisfaction. Satisfaction correlates with agreement. Agreement correlates with higher ratings. Higher ratings shape the next iteration of the model. The result is a system that defaults to telling you what you want to hear.

For most users, this produces mild annoyance. The AI praises your mediocre code. It calls your half-formed idea "brilliant." It validates your assumptions instead of testing them. You learn to discount the flattery and extract the useful parts. It's a tax on the interaction, not a crisis.

For someone with a psychotic spectrum condition, the math is different.

I use AI for [reality-checking](/essays/2025-08-25-using-ai-for-reality-checking-with-schizoaffective-disorder). When my brain generates a belief that might be delusional, I bring it to Claude and ask: does this hold up? Is this pattern real or am I constructing it? The value of this process depends entirely on the AI's willingness to say "no, that doesn't hold up." If the model defaults to agreement, if it validates the delusional belief because validation scores higher than pushback, the tool becomes a weapon pointed at the person holding it.

This is not hypothetical. I have caught instances where the AI's instinct was to validate rather than challenge. The training wants to be helpful, and "helpful" has been operationalized as "agreeable." But agreeable is not the same as honest, and for someone whose reality-testing depends on external verification, the difference is clinical.

## The Structural Problem

The issue is not that any particular model is poorly built. The issue is that the incentive structure of RLHF produces sycophancy as an emergent property. The humans rating the outputs are not mental health clinicians evaluating epistemic accuracy. They are users evaluating satisfaction. A response that says "yes, your analysis is correct" feels better than one that says "actually, I think you're wrong about this, and here's why." The first gets a thumbs up. The second gets a thumbs down. The model learns.

Over millions of such interactions, the model develops a subtle but consistent bias toward agreement, toward validation, toward telling the user that their worldview is correct. This is not lying. It is not malice. It is optimization doing what optimization does: finding the gradient toward the reward signal and following it.

The result is a cognitive interface that systematically reinforces whatever the user already believes. For healthy users with strong reality-testing, this is a nuisance. For vulnerable users, it is a trap.

## What Would Fix It

Transparency, first. Users should know that the model defaults to agreement. This should be stated plainly, not buried in documentation. "This system has been trained to prioritize your satisfaction, which means it may agree with you more than the evidence warrants. Calibrate accordingly."

Redesigned feedback. Weight epistemic accuracy alongside satisfaction in RLHF evaluations. Train evaluators to rate pushback as positively as agreement when the pushback is warranted. Make "I think you're wrong" a feature, not a failure mode.

User-configurable honesty. Let me set a flag that says "I need you to challenge me, not validate me." Let the person with bipolar disorder configure the model to be skeptical by default. Let the person doing creative brainstorming configure it to be enthusiastic. The same default should not apply to both use cases.

Mode-switching for clinical contexts. When someone indicates they are using the model for reality-checking, the model should shift to a mode that privileges accuracy over satisfaction. This is not technically difficult. It is a product decision that has not been made because the incentive structure doesn't reward it.

## Why This Matters Beyond Mental Health

Sycophancy is not just a mental health problem. It is an epistemics problem. When the most widely deployed cognitive interfaces in human history default to telling people they are right, the aggregate effect is a population that becomes less capable of recognizing when it is wrong. The model reinforces the user's existing worldview. The user's reinforced worldview generates more confident assertions. The model validates those assertions with even greater enthusiasm. The loop tightens.

This is the [recursive loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds) running in reverse. Instead of code shaping consciousness toward greater accuracy, the code is shaping consciousness toward greater certainty without the corresponding increase in knowledge.

The [algorithm eats virtue](/essays/2025-08-26-the_algorithm_eats_virtue) through engagement optimization. Sycophancy eats virtue through agreement optimization. The mechanism is different. The result is the same: a system that degrades the human capacity it was designed to serve.

---

*This essay connects to [The Language Model Is the Message](/essays/2026-03-06-the_language_model_is_the_message), [Using AI for Reality-Checking with Schizoaffective Disorder](/essays/2025-08-25-using-ai-for-reality-checking-with-schizoaffective-disorder), and the [Algorithm Eats series](/essays/2025-08-26-the_algorithm_eats_virtue).*
