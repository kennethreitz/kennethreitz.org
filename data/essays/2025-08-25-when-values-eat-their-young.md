---
*August 2025*

tags: [community, psychology, organizations, social-dynamics, activism, open-source]
---

# When Values Eat Their Young: How Ideal-Driven Groups Drift into Their Own Shadow


## The Vignette

Picture this: A Slack channel for an open-source project that prominently displays "Be excellent to each other" in its community guidelines. Six months later, a maintainer posts a thoughtful critique of a proposed code of conduct change. Within hours, they're called "toxic," told they're "literally causing harm," and face demands for their removal. The pile-on continues for days. 

Nobody seems to notice the irony.

This isn't a strawman. This is real shit that happens. I've watched it unfold in projects I love.<label for="sn-pattern" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-pattern" class="margin-toggle"/>
<span class="sidenote">I've been in the Python community since 2008. I've seen us go from "be nice" to... something else. The same community that talks about mental health awareness will pile on someone having a breakdown. The cognitive dissonance is breathtaking.</span>

## The Paradox

The more a community cares about its values, the more vulnerable it becomes to betraying them.

Not because the values are wrong. Not because the people are bad. But because human social dynamics create predictable failure modes that turn principles into their opposite.

> "Every great cause begins as a movement, becomes a business, and eventually degenerates into a racket." — Eric Hoffer

Your community will face these pressures. The question is whether you'll build guardrails before you need them.

## The Machinery of Inversion

### Virtue Signaling: When Performance Replaces Practice

Virtue signaling gets a bad rap, often weaponized to dismiss legitimate moral concerns. But the phenomenon is real. In any community with strong values, there's social currency in being seen as embodying those values. 

The problem? Performance gets rewarded more than practice.

Think about it like code coverage metrics. The goal is good: write tested, reliable code. But once coverage percentage becomes the metric that determines promotion, you get developers writing meaningless tests that check nothing but boost the numbers.<label for="sn-metrics" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-metrics" class="margin-toggle"/>
<span class="sidenote">I've literally seen tests that assert `true === true` just to hit coverage targets. Goodhart's Law in action: "When a measure becomes a target, it ceases to be a good measure."</span> The measure became the target, and the target became meaningless.

In value-driven communities, this looks like competitive displays of ideological purity. Increasingly elaborate pronoun signatures. Lengthy self-flagellating acknowledgments that crowd out actual work.<label for="sn-land" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-land" class="margin-toggle"/>
<span class="sidenote">When your project README is 90% virtue signaling and 10% documentation, you've lost the plot. Users need to know how to use your software, not your politics.</span>

The person who speaks most loudly about inclusion might be the same one privately blacklisting colleagues for minor infractions.

### Purity Spirals: The Revolution Eating Its Children

A purity spiral begins innocently: someone raises the bar for what counts as living up to the community's values. Others, not wanting to appear less committed, raise it further. Soon, you're in a bidding war where yesterday's progressive position is today's problematic stance.

Consider what happened in one climate activism group: It started with "reduce your carbon footprint." Then "go vegan." Then "don't fly." Then "don't have children." Eventually, members were being shamed for taking jobs that required commutes. The group hemorrhaged members, keeping only the most privileged who could afford such restrictions — ironically undermining their stated goal of building a mass movement.<label for="sn-purity" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-purity" class="margin-toggle"/>
<span class="sidenote">A historian friend describes this as "la surenchère" from the French Revolution — revolutionary one-upmanship where yesterday's radical becomes today's moderate becomes tomorrow's enemy. The Jacobins who sent others to the guillotine eventually found themselves condemned by even purer revolutionaries.</span>

### The Iron Law of Institutions

Jonathan Schwarz articulated this perfectly: "The people who control institutions care first and foremost about their power within the institution rather than the power of the institution itself."

Watch what happens when a community leader's position depends on there being problems to solve. Suddenly, problems become very hard to solve. The Code of Conduct committee that needs violations to justify their existence. The working group that creates more working groups. The board member more interested in their board seat than the community itself.

You know what's fun? Watching these same leaders give keynotes about empathy while actively ignoring maintainer burnout in their own projects.

This isn't conscious villainy. It's structural incentive. When your position in a community depends on fighting dragons, you'll always find dragons to fight — or create them.<label for="sn-dragons" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-dragons" class="margin-toggle"/>
<span class="sidenote">This is why I'm skeptical when any group claims they need "permanent" positions to address "systemic" issues. If the issue is truly systemic, why would your job exist to solve it? The incentives are backwards from the start.</span>

### Goal Displacement: When the Means Become the Ends

Every organization starts with a mission. Over time, the processes created to achieve that mission become the mission itself. The meeting about the meeting. The committee to oversee the committee. The elaborate consensus process that ensures nothing ever gets decided.

One collective I observed spent six months perfecting their decision-making process. During those six months, they accomplished exactly zero of their actual goals.<label for="sn-process" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-process" class="margin-toggle"/>
<span class="sidenote">Process matters, but when your process for deciding how to help people takes longer than actually helping them would have taken, you've lost the plot. Ship something. Help someone. Then iterate.</span>

### Cognitive Dissonance: The Stories We Tell Ourselves

When behavior and beliefs conflict, something has to give. Usually, it's the beliefs that bend. A community that prides itself on kindness but regularly engages in cruel pile-ons doesn't admit hypocrisy. Instead, it develops elaborate justifications: "This isn't cruel, it's accountability." "We're not being exclusive, we're maintaining safety." "It's not censorship, it's consequences."

The human brain is exceptionally good at resolving dissonance through narrative. The problem is, these narratives become the water we swim in — invisible, unquestionable, and ultimately destructive to the very values they claim to protect.

## Case Studies in Contradiction

### The Inclusive Space That Wasn't

An online community for marginalized tech workers established itself with values of "radical inclusion" and "brave spaces for difficult conversations." Within a year, they'd developed an elaborate set of speech norms so restrictive that only those with graduate degrees in critical theory could navigate them safely.

A member asked, in good faith, about the practical implications of abolishing prisons for violent crime victims. They were immediately labeled as "perpetuating carceral violence," subjected to a days-long struggle session, and ultimately banned. The community's response to someone seeking education on their values was to exclude them for not already embodying those values perfectly.

The bitter irony: the banned member was a formerly incarcerated person trying to understand how abolition frameworks addressed their own complex experiences with violence.<label for="sn-irony" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-irony" class="margin-toggle"/>
<span class="sidenote">This one still makes me angry. The person with the most lived experience of the system being discussed was excluded for not already knowing the "correct" academic language to discuss it. That's not justice — it's gatekeeping by people who've never seen the inside of a cell but have strong opinions about those who have.</span>

### The Kind Open-Source Project

A popular JavaScript framework prided itself on its welcoming community. "Kindness is our superpower" adorned their README. They had a comprehensive Code of Conduct, a community team, and regular appreciation posts.

Then a maintainer made a technical decision that some disagreed with. The disagreement escalated. Soon, GitHub issues became battlegrounds. The maintainer, overwhelmed by hundreds of hostile messages, took a mental health break. The community's response? Accuse them of "weaponizing mental health to avoid accountability."

The kindness was performative. When tested by real conflict, the community defaulted to the same toxic behaviors they claimed to stand against, but wrapped in the language of justice and accountability.<label for="sn-kindness" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-kindness" class="margin-toggle"/>
<span class="sidenote">I took a break from open source in 2019 because of this. Mental health crisis? Too bad — you're "weaponizing" it. The same people who put mental health in their bios will destroy someone having a public breakdown. "We're holding you accountable" hits different when you're already suicidal.</span>

### The Corporate Culture Initiative

A tech company launched an ambitious "Psychological Safety" initiative. Consultants were hired. Workshops were mandated. Managers were trained to create environments where people could take risks and make mistakes without fear.

Six months later, an engineer raised concerns about a technical decision in a very psychologically safe way — using "I" statements, assuming positive intent, focusing on impact. Their manager's response? Mark them as "not a team player" in their performance review for "creating conflict."

The initiative had become a checkbox exercise. Managers attended the trainings, mouthed the words, but when push came to shove, protecting hierarchy mattered more than living the values.

Oh, and that engineer? They were later let go for "culture fit." The manager who retaliated? Promoted. Psychological safety, indeed.

## The Steelman: Why This Matters Anyway

Before you conclude that all value-driven communities are doomed to hypocrisy, let's acknowledge some crucial truths:

**These communities exist for good reasons.** The tech industry really does have inclusion problems. Open-source really can be hostile to newcomers. Traditional institutions really do perpetuate harm. The values these communities espouse aren't just nice-to-haves — they're attempting to address real, documented problems that cause real human suffering.

**Many communities succeed.** For every horror story, there are quiet success stories. Communities that actually embody their values, resolve conflicts constructively, and create genuine change. These don't make headlines because "community functions as intended" isn't news.<label for="sn-success" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-success" class="margin-toggle"/>
<span class="sidenote">Some communities get it right. They recognize that mental health isn't a weapon or an excuse — it's a reality. They understand that "be kind" means being kind even when someone's struggling, not just when they're productive.</span>

**The alternative is worse.** Communities without stated values don't avoid these problems — they just make them invisible. At least a hypocritical community can be called out on its hypocrisy. A community that never claimed to care about inclusion can exclude with impunity.

**Structural forces are real.** Social media algorithms reward outrage. Venture capital demands growth over health. Academic incentives favor publication over practice. These aren't excuses, but they are context that explains why even well-intentioned communities struggle.

## The Anti-Drift Checklist (For Humans)

Here's your practical playbook for keeping your community aligned with its actual values:

### Design for Dissent
- **Designate devil's advocates** on rotation — make disagreement someone's explicit job
- **Create "loyal opposition" roles** — people whose job is to argue the other side
- **Establish "what would change our mind?" criteria** before making decisions
- **Practice "red teams"** — groups tasked with finding flaws in proposals

### Process Over Personalities
- **Write down enforcement procedures** before you need them
- **Create sunset clauses** for all rules — force regular re-evaluation
- **Separate investigation from decision-making** — different people, different roles
- **Document precedents** — what we did last time and why

### Anti-Purity Mechanisms
- **Ban competitive suffering** — no Olympics of oppression
- **Celebrate course corrections** — make changing your mind high-status
- **Institute "proportionality checks"** — is the response proportional to the harm?
- **Create "safety valves"** — anonymous feedback channels, ombudspeople

### Metric Hygiene
- **Rotate metrics regularly** — prevent Goodhart's Law
- **Measure what matters, not what's easy** — resist the dashboard's tyranny
- **Ask "what would we do if this metric were perfect?"** — would we actually be done?
- **Track unintended consequences** — what got worse when this got better?

### Leadership Humility
- **Publish your mistakes** — model fallibility
- **Step aside regularly** — prevent entrenchment
- **Submit to your own rules** — no exceptions for founders
- **Create "kill switches"** — mechanisms to disband if mission is achieved or failed

## Common Failure Modes

| Stated Value | Common Failure Mode |
|--------------|-------------------|
| Inclusion | Exclusion of those who don't speak the "right" language |
| Kindness | Cruel enforcement of kindness norms |
| Safety | Using "safety" to shut down disagreement |
| Accountability | Accountability for thee but not for me |
| Consensus | Minority veto that creates paralysis |
| Transparency | Performative transparency that hides real decisions |
| Growth | Growth at the expense of founding principles |

## Re-aligning Means with Ends

The tragedy of values eating their young isn't that people are hypocrites. It's that good people with genuine commitments to important values can create systems that betray those values through entirely predictable social dynamics.

The solution isn't to abandon values or become cynical. It's to recognize these patterns as universal human tendencies and design systems that account for them. Just as we write tests because we know code will have bugs, we need to build guardrails because we know communities will drift.

> "The curious task of economics is to demonstrate to men how little they really know about what they imagine they can design." — Friedrich Hayek

The same humility applies to designing communities. We can't perfect human nature, but we can create structures that fail gracefully, correct course, and keep the gap between stated values and lived reality as small as possible.

Look.

I still believe in open source. I believe in communities built on values like kindness, inclusion, and collaboration. But good intentions aren't enough. You need systems. You need guardrails. You need to actually give a shit about people when they're at their worst, not just when they're shipping code.

Build the guardrails *before* you need them. Because once you've driven out the people who came to you for help — the ones who believed in your stated values, who were vulnerable enough to show their struggles — you can't un-eat them.

And they won't come back.

I didn't.

---

## Further Reading

- *The Righteous Mind* by Jonathan Haidt — moral psychology and why good people divide
- *The True Believer* by Eric Hoffer — mass movements and fanaticism
- *Seeing Like a State* by James C. Scott — how well-intentioned schemes fail
- *The Tyranny of Metrics* by Jerry Z. Muller — when measurement goes wrong
- *Exit, Voice, and Loyalty* by Albert O. Hirschman — organizational decline and response

---

