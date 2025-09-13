# The Future of Python Dependencies Management
*2018*

<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/ee6c0016a8f44dd98900659d225b6925" title="The Future of Python Dependency Management" allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>


## Introduction

This presentation introduced **Pipenv** as the next evolution in Python dependency management, offering a fundamentally streamlined approach that addressed the longstanding complexities and fragmentation of traditional methods like `pip` and `virtualenv`. The timing proved prescient—this vision would soon become Python's official recommendation.<label for="sn-pipenv-adoption" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-pipenv-adoption" class="margin-toggle"/>
<span class="sidenote">This talk coincided with Pipenv's adoption as the officially recommended packaging tool by Python.org, marking a significant shift in Python's packaging landscape and validating Kenneth's vision for better dependency management.</span>

## History and Challenges of Python Packaging

The presentation began by examining Python packaging's troubled history. In the early days, PyPI (formerly "The Cheeseshop") served merely as an index rather than a comprehensive package host. Packages were scattered across external hosts, the entire system ran on a single server, and manual processes combined with global installations created consistently poor user experiences that frustrated newcomers and experts alike.

Gradual evolution brought some improvements: **Pip** eventually replaced the problematic `easy_install` as the primary package manager, **virtualenv** became the standard solution for creating isolated environments, and **requirements.txt** files emerged as the conventional approach to tracking dependencies.

However, these tools introduced their own complications. Virtualenv presented a steep learning curve that proved particularly difficult for newcomers to Python. Requirements.txt files suffered from a fundamental impedance mismatch between what was actually installed and what was conceptually needed, often leading to non-deterministic builds that worked on one machine but failed on another.

## The Problem with Current Practices

The presentation detailed specific problems plaguing Python's dependency ecosystem. **Virtualenv**, while solving environment isolation, remained a difficult abstraction for beginners and felt manual and unnatural without additional tools like `virtualenv-wrapper`. This complexity barrier prevented many developers from adopting proper isolation practices.

**Requirements.txt** created its own set of complications by requiring two distinct types of dependency files: one containing unpinned dependencies for general requirements (like "Flask"), and another with pinned, all-inclusive dependencies for reproducible builds. This dual-file system confused developers and made dependency management unnecessarily complex.

Most critically, **Python lacked a lockfile** for deterministic dependency management—a feature that other language communities like Node.js and PHP had successfully implemented and relied upon.<label for="sn-lockfile-philosophy" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-lockfile-philosophy" class="margin-toggle"/>
<span class="sidenote">The introduction of lockfiles to Python represented Kenneth's broader philosophy of learning from other language ecosystems. Rather than accepting "that's just how Python works," he imported proven concepts from JavaScript and Ruby communities.</span>

This absence meant that Python developers couldn't guarantee that the same dependency versions would be installed across different environments, leading to the persistent "works on my machine" problem.

## The Solution: Pipfile and Pipenv

The solution emerged in the form of **Pipfile**, a new standard designed to completely replace requirements.txt with a more thoughtful approach. Pipfile uses the TOML format, making it both human-readable and machine-parseable. Its structure includes two logical sections: `[packages]` for production dependencies and `[dev-packages]` for development-only dependencies, eliminating the confusion of managing multiple requirements files.

**Pipfile.lock** complements this by providing a machine-readable JSON file containing pinned dependencies and acceptable hashes for each release, finally bringing deterministic builds to Python. This lockfile approach ensures that the exact same dependency tree can be reproduced across different environments and deployment targets.

However, the transition faced practical challenges. Pipfile wasn't yet integrated into `pip` itself, and full ecosystem integration would require time and resources that the Python packaging community needed to allocate carefully.

## Pipenv: The Recommended Tool

**Pipenv** emerged as the comprehensive solution that unified these improvements into a single, officially recommended tool by Python.org. Its key innovation was **automating virtualenv management** while seamlessly integrating Pipfile and Pipfile.lock for dependency management, creating a workflow that felt natural rather than mechanical.

The tool ensures **deterministic builds** through hash check verification during installation, finally solving Python's reproducibility problems. This comprehensive approach garnered significant praise from the Python community.

**User testimonials** validated the approach: **Jannis Leidel**, former pip maintainer, praised Pipenv for eliminating the need for manual virtualenv and pip calls. **Justin Myles Holmes** offered particularly insightful commentary, commending Pipenv for being "an abstraction that engages the mind, not just the filesystem"—recognizing that good tools should align with how developers think about problems rather than forcing them to manage low-level implementation details.

## Conclusion

The presentation positioned Pipenv as a significant evolutionary leap in Python dependency management, finally bringing the intuitive workflows and deterministic builds that other language ecosystems had long enjoyed. By abstracting away the mechanical complexities of virtualenv management while introducing proper lockfile semantics, Pipenv represented not just a tool improvement but a philosophical shift toward treating dependency management as a solved problem rather than an ongoing source of friction.

This advancement promised to lower barriers for Python newcomers while providing the reliability and predictability that production deployments demanded.
