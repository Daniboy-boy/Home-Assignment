# Git Commit Info Script

## Overview

This Python script provides information about recent commits in a Git repository, for each commit separately and a little summary information for all of them.

The purpose of this readme is to clarify the motivation behind this assignment, as I perceive it.
Additionally, I will provide some justifications for the choice of information presented by the script.

## Usage

1. **Install Dependencies:**
   
   ```bash
   pip install GitPython

## General motivation
The motivation behind developing this script is to meet a DevOps engineer's requirements. I tried to imagine a scenario where the DevOps engineer may be tasked with gaining insights into a specific project branch and the team is considering merging the branch into the master. The script provides a convenient way to gather essential information without delving deeply into the code.

## Some justifications & clarifications
•	Branches pointing to the commit: I believe in most cases you see only the name of the branch you are looking at as other branches point to other development processes but in some cases could be interesting to spot more than one.

•	Percentage Change in Lines of Code: A large percentage does not mean a major code change and the same applies to a small percentage. But I think in some cases could provide some context to the development process on the branch.

## Demonstrative Output
Within this repository, you'll find a sample output generated from running the script on an open-source library named "deepchecks" on branch "main". 

## One last note
While I acknowledge that this script may not provide a comprehensive account of a branch's entire history, it might serves as a valuable starting point. It can offer insights and prompt further investigations or meaningful discussions with fellow engineers on the team.