# Mental Health (for Humans)

*June 2026*

Let me present my credentials.

I am sick as fuck. Disabled, in fact. I have schizoaffective disorder, bipolar type, with a side of PTSD. I have [watched an angel descend from the sky](/essays/2025-09-17-delusions-and-schizoaffective-disorder) and land in front of a neighbor's house, and I remember it more clearly than I remember most real things. I have [felt my wife's phone vibrate](/essays/2025-09-04-what_schizoaffective_disorder_actually_feels_like) in the middle of the night while she slept and it sat silent. I have been hospitalized more times than I can count on one hand, [diagnosed and re-diagnosed](/essays/2019-01-mentalhealtherror_three_years_later), and informed by a doctor, gently, that most people with my diagnosis are homeless.

I have spent more than ten years inside the mental health system. Not reading about it. *In* it. I have played the medicine game at every level: the gold standard that made me sleep until 4 p.m., the mood stabilizer whose side effects outweighed its benefits, the $2,000-a-month injection that finally worked, the scheduled gabapentin, the trial periods, the titrations, the tapers, the pharmacy phone calls, the prior authorizations. I know the vinyl smell of a behavioral health unit and the specific quality of light in the room where they tell you your new label.

These are my credentials. I mention them because this essay is going to argue with how the entire system frames itself, and I want it understood that I'm not arguing from a podcast. I'm arguing from the waiting room.

A long time ago I built an HTTP library and called it [Requests: HTTP, for Humans](/themes/for-humans-philosophy). The premise was simple: tools should serve human mental models instead of forcing humans to contort themselves around the tool's internals. That premise turned out to apply to almost everything. This essay applies it to the system I've spent a decade surviving, because mental health care, as currently practiced, is urllib2. The capability is in there somewhere. The interface is hostile to the people it exists for.

## You Have the Diagnosis Backwards

Here is the single most important reframe I can offer, the one I wish someone had handed me in 2016 along with the discharge paperwork:

**Diagnosis drives treatment. Treatment is what matters. That's the whole relationship.**

Patients almost universally have this backwards, because the system delivers diagnosis backwards. You sit in a room, and a professional pronounces a noun over you, and the noun arrives with the gravity of a verdict. Patients receive a diagnosis the way defendants receive a sentence: as a statement about who they are and what their life will now be. They go home and google the noun and read the prognosis statistics and the disability rates and the mortality numbers, and they begin, quietly, to become the label.

But that is not what a diagnosis is. A diagnosis is a routing function. It exists to answer exactly one question: *given this cluster of symptoms, which treatments are most likely to help?* That's it. That is its entire job. It is a lookup key into treatment space. It is the means; the treatment is the end. The diagnosis was never supposed to be a prophecy about you. It was supposed to be a query plan.

```python
# How patients are taught to receive a diagnosis
class Schizoaffective(LifeSentence):
    """Who you are now."""


# What a diagnosis actually is
def diagnose(symptoms):
    """A lookup key into treatment space. Nothing more."""
    cluster = dsm.nearest_known_population(symptoms)
    return treatments.with_evidence_for(cluster)
```

The first version is a noun you become. The second is a function you use. The difference between them is the difference between a life organized around a label and a life organized around what works.

I know this distinction in my body, because my label has changed underneath me. In 2016 I was [diagnosed with Bipolar I with psychosis](/essays/2016-01-mentalhealtherror_an_exception_occurred). Three years later, the diagnosis was revised to schizoaffective disorder, bipolar subtype. Here is the thing nobody tells you about that moment: on the day the label changed, *I did not change*. Same brain. Same symptoms. Same marriage, same work, same 3 a.m. phantom phone vibrations. What changed was the lookup key, because the resolver had accumulated better data about which population I actually resembled. If the diagnosis were an identity, I had just undergone a transformation. Since it's actually a pointer, all that happened was a re-index. The treatment plan barely moved.

If your sense of self survives a re-diagnosis intact, you've learned what a diagnosis is. If it doesn't, the system taught you wrong.

## The S Stands for Statistical

People talk about the DSM like it's scripture, a taxonomy of fixed disease entities handed down from somewhere. It isn't, and the confession is printed on the cover: *Diagnostic and **Statistical** Manual*. The name tells you exactly what it is. It is a statistical report on populations at scale, grouped by clusters of observable criteria, maintained by committees, revised by vote.<label for="sn-dsm-votes" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-dsm-votes" class="margin-toggle"/><span class="sidenote">Literally by vote. Homosexuality was removed from the DSM in 1973 by a vote of the APA board, ratified by a referendum of the membership. Asperger's was deleted as a diagnosis in 2013 and folded into the autism spectrum. Entire categories of human being appear and disappear by committee. This is not a complaint; revisability is a feature. But you cannot revise scripture by majority vote, which tells you the DSM was never scripture.</span>

Understand what that means for you, the patient. When you receive a diagnosis, you have not been identified. You have been *matched*. Some large population of past humans reported symptom clusters resembling yours, researchers studied what helped them, and the manual encodes that pattern so your clinician doesn't have to start from zero. That is genuinely useful. It is also *all that happened*. You were placed near a histogram. A histogram has no idea what your life will be. It describes the center of a population; it says nothing about where in that population you sit, and the spread is enormous.

The criteria themselves make this obvious. Most DSM diagnoses are checklists: five of nine, four of seven, two of five with one from column A. The checklist structure means two people who share a diagnosis can share almost none of the same experience.<label for="sn-combinatorics" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-combinatorics" class="margin-toggle"/><span class="sidenote">Borderline personality disorder requires five of nine criteria, which allows 256 distinct symptom combinations to carry the same label. Two people can both "have BPD" while sharing exactly one symptom. The label is doing population-scale compression, and compression is lossy.</span> The label is a lossy compression of millions of people. Useful for routing. Catastrophic as an identity.

So the DSM is a census, not a prophecy. It tells you which neighborhood of human suffering your symptoms currently live in, so the right tools can be tried sooner. The moment it gets used for anything else, for identity, for destiny, for the denial of care, it is being misused, and you are allowed to say so.

## The Medicine Game

Now we get to the part where the professionals themselves have it backwards, because the backwards-ness isn't only a patient problem.

Take clonazepam. Klonopin. A benzodiazepine, prescribed for decades, surrounded by one of the loudest controversies in psychiatry. There are, roughly, two schools of thought:

**School A:** Klonopin is a helpful medicine that enables success across an array of problems. It quiets panic that nothing else touches, makes sleep possible, makes work possible, makes *leaving the house* possible, and for many people does so stably for years.

**School B:** It KILLS. Dependence, tolerance, brutal withdrawal, cognitive decline, death. No one should be on it, and prescribers who maintain patients on it are committing slow malpractice.

Here is what I need you to notice: both schools speak with total certainty. Both can produce evidence, casualties, and testimonials. A patient can walk out of one office with a stable prescription and a functioning life, move to a new city, and be told by the next prescriber that their functioning life is actually a crisis that must be tapered immediately, for their own good, regardless of how they feel about it.<label for="sn-both-true" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-both-true" class="margin-toggle"/><span class="sidenote">The maddening part is that both schools are describing real populations. The drug that quietly enables one person's career destroys another person's decade. Population statistics cannot tell you which patient is sitting in front of you. Only careful, collaborative observation of the actual human can.</span>

```python
def klonopin(patient):
    # School A
    return "sleep, work, marriage, a life"


def klonopin(patient):
    # School B
    raise Dependency("IT KILLS")
```

Two functions. Same name. Same molecule. Which one runs depends not on the patient but on which prescriber the lottery assigned them. That is not medicine. That is theology with a prescription pad.

The "for humans" question, the only question, never changes: *does this molecule, in this body, enable this particular human's actual life, at a cost this particular human judges acceptable?* That is an engineering question, answerable only by N-of-1 trial, honest tracking, and a [collaborative relationship with a prescriber](/essays/2025-08-25-advocating-for-your-mental-health-care) who treats you as a partner rather than a compliance problem. I have been on medications that the literature adores and my body could not tolerate, and medications with scary reputations that quietly gave me my life back. The discourse was never once useful at the pharmacy counter. The data about *me* was.

When a clinician's ideology about a medication overrides the observable evidence of your functioning, the tool has stopped serving the human. The human is now serving the tool.

## The Label That Locks the Door

It gets worse than ideology. Sometimes the diagnosis, the thing whose entire purpose is to route you *toward* treatment, gets used as the reason to refuse it.

Ask anyone with borderline personality disorder. BPD patients routinely cannot get help because therapists refuse to work with them. Not "lack expertise in." *Refuse.* The label functions as a flag on the account. Practitioners see it in the chart and decline the referral, citing difficulty, liability, burnout. The diagnosis most defined by the terror of abandonment reliably produces institutional abandonment on contact.<label for="sn-linehan" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-linehan" class="margin-toggle"/><span class="sidenote">The bitter irony: BPD has one of the best-validated treatments in all of psychiatry. Dialectical behavior therapy was developed by Marsha Linehan, who revealed in 2011 that she had spent her own youth hospitalized with the same condition. The "untreatable" diagnosis got its treatment from a patient. It usually works that way.</span>

Think about what has happened there, structurally. A routing function has been repurposed as a firewall. The lookup key that exists to answer "which treatments help this cluster" is instead answering "which humans do we decline to serve." This is the diagnosis doing the exact opposite of its job, and the field mostly shrugs, because the people being turned away have a label that pre-discredits their complaints. Who are you going to believe, the clinician or the borderline?

And the same inversion runs even deeper with dissociative identity disorder, where patients are routinely dismissed because the practitioner is not personally "convinced it's a real ailment." Sit with that phrasing, because I've heard it nearly verbatim from professionals: whether you receive care depends on whether the person across the desk *believes in* your condition. Your access to treatment is contingent on your clinician's metaphysics. Imagine any other field operating this way. Imagine a cardiologist declining your arrhythmia because they're not convinced atrial fibrillation is real, they think it's an attention-seeking presentation of ordinary heartbeat.

Here's the thing: the etiology debate doesn't even matter at the point of care. Whatever a practitioner believes about how [plural self-states](/essays/2025-08-30-the-plural-self-what-did-reveals-about-all-consciousness) form, the human in the room is not hypothetical. The dissociation is real. The lost time is real. The distress is real and standing in front of you, having gathered the courage to ask for help with the most stigmatized presentation in the manual. "I'm not convinced your suffering's category exists" is not a clinical position. It is a refusal of the human, dressed up as epistemic rigor.

## What "For Humans" Actually Means Here

The pattern across all of this is the same pattern I spent my software career fighting. The system is optimized for its own internals: diagnostic categories, billing codes, school-of-thought loyalties, liability management, practitioner comfort. The human is expected to adapt to the system. A patient must learn the system's language, absorb its labels as identity, accept its theological disputes being fought across their body chemistry, and survive its gatekeeping, all while sick. That is exactly backwards, and it is backwards in the precise way urllib2 was backwards: the machinery's convenience placed upstream of the human's need.

Mental health care, for humans, would mean:

- **The diagnosis serves the patient.** It is a revisable lookup key that exists to find treatments faster. The moment it functions as identity, prophecy, or a reason to refuse care, it is malfunctioning.
- **Treatment is judged by the life it enables.** Not by the reputation of the molecule, the purity of the modality, or the prescriber's tribe. If it gives a particular human their particular life at a cost they accept, it is working.
- **The patient is a partner, not a compliance problem.** The patient holds data no clinician can access: what it's actually like in there, hour by hour, [tracked and brought to the table](/essays/2025-08-25-advocating-for-your-mental-health-care). Expertise without that data is guesswork with confidence.
- **The reality of suffering is not contingent on belief.** A clinician's personal conviction about a diagnostic category is not an eligibility requirement for care.
- **The label describes a population. You are not a population.** You are one data point the histogram never met.

None of this is utopian. Every item on that list is practiced, today, by good clinicians. I know because I finally have some, and the difference between the system at its worst and these people at their best is the difference between [a hospitalization a year](/essays/2019-01-mentalhealtherror_three_years_later) and [a winter where the cycle finally broke](/essays/2026-04-06-what_success_looks_like).

## Ten Years In

So here is where my credentials lead.

I am still sick as fuck. That hasn't changed and probably won't; schizoaffective disorder doesn't resolve, it gets *managed*. What changed is everything else. I'm married to a woman who [sees episodes coming before I do](/essays/2026-03-06-sarah_knows_first). I have a son. I build things constantly. I take my medicine, the specific medicine that works for this specific body, arrived at through a decade of the game, kept because it enables my actual life and not because any school of thought approves of it.

A doctor once told me most people with my diagnosis are homeless. He wasn't wrong about the population. But I was never the population. Neither are you. The histogram describes what happened to people who resembled you before anyone tried what might work for *you*, and the entire purpose of the label, the manual, the medicine, the whole creaking system, is to shorten the path to that treatment. The label is the means. The treatment is the point. Your life is the metric.

Diagnosis is just a lookup key. Don't build a house on it. Build a treatment on it, and build your house on that.

I'm doing much better than my label, statistically speaking. I'd like that for you too.
