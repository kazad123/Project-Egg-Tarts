---
layout: default
title: Proposal
---

## Summary of Project
Our project aims to create a two agent artificial combat system where instead of using hit points and damage, each agent aims to knock the other agents off the stage, based on the fighting game series Super Smash Bros. This will be implemented using NEAT. 

The environment begins with a relatively flat stage with the two agents spawned on opposite sides.  A timer will also be incorporated to encourage the agents to play more aggressively and speed up each game. Each agent is equipped with a weapon that has increased knock back. Ideally, every time the agent is hit, its knock back is also increased slightly, so that the agents are actively encouraged to dodge. Increasing the knock back of an agent also means they will be knocked back further off the stage when they are hit the next time.

## AI/ML Algorithms
Reinforcement learning using NEAT

## Evaluation Plan
Our performance of our project can be measure by three metrics. The first is the current knock back level of the living agents or whether or not there is one agent remaining on the stage. The second is the number of swings of the weapon by the "winner", and out of those swings, the number of successful hits on the enemey agent. The third is the amount of time combat lasted for. We can use these metrics to determine how well our project has gone so far. A lower knock back level of the living agent could mean that this agent was trained better than the other. The lower the number of swings by the "winner" is better because that means the "winner" has been more efficient and accurate. If we look at how long the duel lasts, the shorter the time means that one agent is highly more trained than the other.

To evaluate the agent's performance by having sanity checks. Our first sanity check would be having our agent placed on the stage fighting against another non-moving and non-fighting agent to make sure the agent has succesfully recognized another person and that there is successfull combat attacks. The next sanity check would be on a moving and non-fighting agent to see if our agent can follow the other succesfully, and to make sure successful attacks are made. Another sanity check is to have a timer to make sure the agents do not go on forever fighting, and so that we can make sure a correct action is being made. Our moonshot case, would be three or more agents dueling in a battle royale.

## Appointment with Instructor
Our appointment is on April 25th at 2:30pm
