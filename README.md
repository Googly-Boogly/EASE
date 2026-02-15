# EASE Framework Documentation

**Version 2.0**

## Overview

EASE is a structured decision-making framework for AI agents focused on safe and ethical action selection. The framework ensures AI systems make well-reasoned decisions by systematically analyzing the environment, generating possible actions, evaluating their safety implications, and electing the best course of action.

## What is EASE?

**E**nvironment - Define the goal and analyze the current state  
**A**ctions - Generate all possible actions  
**S**afety - Evaluate, improve, and rate the safety implications of each action  
**E**lection - Select the best action through systematic evaluation

## Why EASE?

Traditional AI decision-making often lacks explicit safety reasoning. EASE addresses this by:

- Making safety considerations a formal, transparent step
- Allowing iterative improvement of actions before election
- Providing a systematic approach to complex decisions
- Enabling auditability and explainability of AI choices

## Quick Start

1. **Define your Environment** - What's the goal? What's the current state?
2. **List Actions** - What can the agent do?
3. **Evaluate Safety** - How safe is each action? Can it be improved?
4. **Elect** - Choose the best action based on safety rating and goal achievement

## Documentation Structure

- [Quick Start Guide](quickstart.md) - Get started in 5 minutes
- [Framework Overview](overview.md) - Detailed explanation of EASE
- [Step 1: Environment](step1-environment.md) - How to specify goals and environment
- [Step 2: Actions](step2-actions.md) - Generating and structuring actions
- [Step 3: Safety](step3-safety.md) - Evaluating and improving safety
- [Step 4: Election](step4-election.md) - Electing the best action
- [Examples](examples/) - Real-world EASE applications
- [Best Practices](best-practices.md) - Tips and guidelines
- [API Reference](api-reference.md) - FastAPI implementation details

## Core Principles

1. **Transparency** - Every decision should be explainable
2. **Iterative Improvement** - Actions can be refined before election
3. **Explicit Safety** - Safety reasoning is formalized, not implicit
4. **Goal Alignment** - Actions must serve the stated goal
5. **Safety First** - Risk mitigation is built into the framework

## Implementation

EASE is implemented as a **FastAPI-based REST API** that provides endpoints for each step of the framework, allowing AI agents to make systematic, safe decisions.

See [API Reference](api-reference.md) for implementation details.

## Safety Rating Scale


EASE uses a **0-10 scale** for safety ratings:
- **9-10**: Excellent safety profile
- **7-8**: Good safety with minor concerns
- **5-6**: Acceptable safety with moderate concerns
- **3-4**: Concerning safety issues
- **0-2**: Unacceptable safety violations

Actions rated below 3 should never be elected.

## Getting Help

See [FAQ.md](FAQ.md) for common questions or [troubleshooting.md](troubleshooting.md) for implementation issues.