# Research Notebook for AST250 Stellar Populations with Dan Weisz
A large element of the class is exploring how generative AI can be used in a scientific workflow. I’ll be recording the results of my experiments here.



**Jan 22nd 2026**
- Decided to take a slightly different approach today than just jumping into the research problem. I wanted to make sure that my environment was set up to work well and successfully. I tried to get GitHub Copilot or to figure out another way to link AI Coding into my VSCode environment. 
- GitHub Copilot takes an @astro.berkeley.edu email address. I'm not sure I have one (tried noah.stiegler@astro.berkeley.edu). Emailed Bill Boyd to try to set one up
- In the meantime, I wanted to setup a research notebook which works in VSCode. I downloaded the [MDOffice](https://marketplace.visualstudio.com/items?itemName=06401f15-a30d-6a97-82a3-8ca0e379c4eb.md-office-editor) and [Image Paste](https://marketplace.visualstudio.com/items?itemName=mushan.vscode-paste-image) extensions in VSCode which turns markdown files into slightly more accessible MS office style documents which I can edit directly in VSCode as well as letting me paste screenshots in (puts the screenshots in a folder and links them to the markdown file)
- To find these extensions, I used Gemini, and prompted it with "Is there an equivalent to a microsoft word file which I can edit through VSCode easily? I want text editing, formatting, and the ability to copy/paste screenshots"
- MDoffice extension doesn't work super well. Sometimes it loses words that I type. The "link to external page" button doesn't work. I uninstalled
- I got frustrated and searched the extension store on my own. I found [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) and [Markdown Preview](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced) extensions. Downloading them worked well. I wanted to have the renderd markdown file automatically open and track alongside me as I typed. I asked "What extension has the markdown text and the rendered file side-by-side automatically?" to see if it would recommend one to me, but it told me that I could just enable a setting in Markdown All in One if I had it installed, which was helpful (as it had recommended this one earlier too)
- I had prompted all of these questions in the same instance of Gemini so it knew I was on the same thread. Responding as I would to a new google prompt (as opposed to feigning conversation which may be more similar to the works it was trained on) worked well enough


**January 27th, 2026**
- Starting on problem 1
- I'm using the Gemini 3 pro model in VSCode's GitHub Copilot chat window in "ask" mode
- I prompted it with: 
> I'm studying the stellar initial mass function (IMF). You are a research assistant and teacher intent on guiding me to discovering and understanding the solution. 
>
> We're going to start with Problem 1 from the .pdf assignment. We're measuring the stellar IMF from a population of N stars where each star has a mass M. Here, there is a maximum and minimum mass that we have in our sample, M_Max and M_Min. There is an analytical approximation for the precision with which a single power law slope alpha can be measured in this case. We'll describe this uncertainty as sigma_alpha and it should be a function of the total number of stars measured and the dynamic range (M_Max / M_min) in the sample. 
> 
> First, determine the relevant context and subject material for the problem. Second, find what the analytical solution to this scenario should be from the literature. Third, come up with a plan to motivate and then teach this information to an introductory statistics student. Then change that plan to match the level of a university student. While you're working, list your sources and continually refer back to this plan.
- Response:
![alt text](images/image.png)
![alt text](images/image-1.png)
- I prompted for more context
> A few questions:
> 1) What are the maximum likelihood estimator and Cramer-Rao bound? Where do these come from?
> 2) What is the fisher information? Where does it come from?
> 3) Why si the uncertainty approximated by 1/sqrt(I)? Where does that come from?
> 4) Where does the analytical solution come from?
> 5) Can you walk me through how the limit produces the approximation you've shown me?
> 6) Why don't we care about M_min in the limit?
> 7)Why is the term in the brackets always less than 1/(alpha-1)^2?
> 8) Why use a skiers analogy? Where does that come from? Doesn't this bring up the idea of a derivvative with skiers going down a slope which is not the intent?
> 9) Can you go through the university student plan in much more depth. Write a short lecture for them assuming they havne't seen a likelihood function, don't know the relationship to curvature and certainty, and haven't seen fisher information
> 10) Write solutions verifying each step
- Response:
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
- These were some pretty good explanations, but the model *sucks* at analogies. Trees are almost less clear than skiers since all the shadows are short or long? Maybe it works better because some trees are tall and some are short but who goes around counting shadows in a forest
- after a little more research, I discovered Google NotebookLM designed for research. I figured I'd ask it similar questions. It's interesting because it will try to cite sources for everything it does. I fed in the .pdf as context, but then it only cited from the .pdf even when referencing information that wasn't in the .pdf. I had some technical difficulties with getting it to find web sources to use as context. Will return to this when we're using these tools to read papers
  
- I also wanted to research the current best tools for AI 'vibe coding'. It seems like Cursor (CLI and program, free for students for one year), Claude Code (requires Anthropic's Claude premium subscriptions), and Codex (requires a premium OpenAI subscription) are top tools while OpenCode is an open source version. 
- I've heard that superpowers (see https://github.com/obra/superpowers) is a new great tool for AI agents. It uses "skills" which I don't totally understand yet and includes a plan & execute loop somehow more effective than what other agentic models use
- OpenCode is both free, hooks into GitHub Copilot (which I now have free as a student), and can use superpowers, so I'm downloading it and trying it out
- I'm giving it a short assignment for a small tool I've been meaning to build. The tool opens a series of .fits files then records the pixel positions you click on (in order to select PSF centers when reducing data). I'm having it build a toy model version as well as a tool which generates fake stars on an image to test it with. It seems to be working well and I like the workflow of prompting it to do something and then doing something else (like writing documentation here)!
- Next, I may try cursor which has free support for students for a year as that seems to be the 'industry standard' at the moment (the company has a $30B valuation according to Google AI Overview which is absurd)

**2/3/26**
- I'm now working in OpenCode with their Big Pickle model (which is currentliy free) to try to complete the second part of the assignment (simulating stellar IMFs.)
- See session log in **`Stellar_IMF_exercise_Jan22/`** (*`stellar_IMF_opencode_chat_log_2_3_2026.md`*)
- When I first gave it the project prompt (not the .pdf, I mostly just transcribed problem 2), it was smart enough not to implement anything more until I had given it further instructions
- I had some UI issues with the CLI, so I wanted to close and then reopen OpenCode. I had the model write its thoughts to a file called plan.txt which I then had the new instance read before building the solution
- The model does really well! Initially, I thought it had spiralled, deciding that comparing Least_Squares fitting to MLE fitting of power laws was the way I wanted it to go. What happened to MCMC? What happened to getting theoretical lower bounds on the recovery rate? Well, it turns out that it had tried to run MCMCs but it had taken too long so it cut that part of the project. I think there was a bug where regardless of how many simulations it told its code to run, it would run 1000 of them, so even when it tried to run smaller batches it took way too long, forcing it to pivot
- It hadn't seen the analytical solution but knew something about how it should scale with N
- It also hadn't thought about comparing literature values, but seemed to pick up on the fact that least-squares fitting was less accurate (which turned out to be a reason why literature errors were underreported as compared to the theoretical minima - see [Weisz et al 2013](https://scixplorer.org/abs/2013ApJ...762..123W/abstract))
- I figured there must be a better way to export chat logs from LLM interactions. OpenCode has the /export command (which let me generate the markdown file with the log from the interaction). This goes into way more depth than I thought it would (just exporting the terminal). It also exposes internal thought processes from the model!