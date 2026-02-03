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

 > input: Yes! Good analysis. I'll describe the exercise since you can't read it. We're going to explore the statistical error bounds of stellar initial mass functions and how precisely we can measure them given a certain mass range and a limited number of stellar measurements. We're going to do this with a monte carlo method numerically. Together, we'll write a script that simulates synthetic stellar populations and attempts to recover their initial parameters. First, we'll generate our data. We'll create a list of N (input) stellar masses drawn randomly from a power-law distribution defined by a known slope \alpha bounded above and below by M_min and M_max, the maximum and minimum masses we can generate from our gas cloud. Then we'll fit the data. We'll fit our generated/synthetic data to a model power-law. Give the option to fit via the Maximum Likelihood Estimation, MCMC, or least-squares fit, as methods of recovering the simulated slope and its uncertianty. Finally, we'll repeat this process for K stellar clusters, varying N (the number of stars indicating the size of the cluster), as well as M_min and M_max within those clusters to build up a statistical profile of the recovery precision. Can you help me build these simulations? We're going to want to save all the data so that we can analyze it. Analysis should be graphical as well as text-based. If this is something that you can build in a Python Jupyter notebook (one already exists called exercise.ipynb that you should add to if you can), then do that.

        I'll help you build this stellar IMF simulation! Let me first explore the existing notebook and understand the current structure to plan the implementation.
        → Read exercise.ipynb 
        ✱ Glob "*.py" 
        ✱ Glob "*.md" 
        ✱ Glob "*" (2 matches)
        Now let me check what Python packages are commonly used for this type of work to understand the dependencies:
        # Check if key packages are available
        $ python -c "import numpy, scipy, matplotlib, emcee; print('Core packages available')" 2>/dev/null || echo "Need to install packages"
        Need to install packages
        Based on my analysis, here's a comprehensive plan for building the stellar IMF Monte Carlo simulation:
        Implementation Plan
        1. Core Infrastructure Setup
        - Add necessary imports: numpy, scipy, matplotlib, emcee (for MCMC), pandas
        - Set up random seed for reproducibility
        - Create data storage structure (possibly HDF5 or compressed numpy arrays)
        2. Data Generation Module
        - Function to generate stellar masses from power-law distribution using inverse transform sampling
        - Input parameters: N (cluster size), alpha (true slope), M_min, M_max
        - Storage format: structured arrays with metadata (true parameters, generation timestamp)
        3. Fitting Methods Implementation
        - Maximum Likelihood Estimation: Analytical solution for power-law slope
        - MCMC: Using emcee with appropriate likelihood and priors
        - Least Squares: Linear regression on log-transformed data
        - Each method returns: fitted alpha, uncertainty, convergence metrics
        4. Monte Carlo Simulation Framework
        - Function to run K simulations for given (N, M_min, M_max) parameters
        - Configurable fitting method selection
        - Progress tracking and intermediate results saving
        - Statistical analysis of recovery precision
        5. Parameter Space Exploration
        - Grid search over N (10, 100, 1000, 10000 stars)
        - Range of M_min/M_max ratios (10, 100, 1000)
        - Multiple true alpha values (1.35, 2.35, 3.35)
        - K ≈ 1000 iterations per parameter combination
        6. Analysis and Visualization
        - Recovery bias plots (fitted vs true alpha)
        - Precision vs N curves
        - M_min/M_max ratio effects
        - Method comparison plots
        - Statistical summaries with confidence intervals
        7. Data Management
        - Hierarchical data storage (ex: results_N1000_alpha2.35_r100.h5)
        - Metadata preservation
        - Easy loading for subsequent analysis
        Key Questions:
        1. Default parameters: What initial values should we use for alpha, M_min, M_max, N, K?
        2. Mass units: Should we work in solar masses (M_min ≈ 0.1, M_max ≈ 100)?
        3. MCMC specifics: How many walkers, burn-in steps, and total steps?
        4. Output format: Preference for HDF5, pickle, or individual CSV files?
        Would you like me to proceed with this plan, or do you have specific preferences for any of these parameters?
        ▣  Plan · big-pickle · 27.4s
        
 > A few questions. What is inverse transform sampling? Also can you give me the functional form of the power law so I know you have it correct? Also, don't vary alpha when performing experiments. It can stay the same while we try to figure out how precisely we can measure it. Let it be a configurable parameter though. Mass units should be solar masses. 0.1 and 100 solar masses look good for initial bounds, although we'll want to be able to change them as the user specifies. The MCMC shouldn't take too long to run. CSV files would be good for output since they're simple to double check.
      
        Great questions! Let me clarify the technical details and refine the plan:
        Inverse Transform Sampling
        Inverse transform sampling is a method to generate random numbers from any probability distribution. For a power-law, if the PDF is $p(m) \propto m^{-\alpha}$, then:
        1. Generate uniform random number $u \in [0,1]$
        2. Transform using the inverse CDF: $m(u) = \left[\frac{M_{max}^{1-\alpha} - M_{min}^{1-\alpha}}{1-\alpha} \cdot u + M_{min}^{1-\alpha}\right]^{1/(1-\alpha)}$
        Power-Law Functional Form
        The stellar IMF power-law is typically written as:
        $$ \frac{dN}{dM} = A M^{-\alpha} $$
        Where:
        - $dN/dM$ is the number of stars per unit mass
        - $M$ is stellar mass in solar masses
        - $\alpha$ is the slope (Salpeter value: 2.35)
        - $A$ is the normalization constant
        The probability density function (normalized) is:
        $$ p(M) = \frac{(1-\alpha) M^{-(\alpha+1)}}{M_{max}^{1-\alpha} - M_{min}^{1-\alpha}} $$
        Refined Implementation Plan
        1. Core Parameters (configurable, defaults shown)
        config = {
        'alpha_true': 2.35,      # Fixed for experiments
        'M_min': 0.1,             # Solar masses
        'M_max': 100.0,           # Solar masses  
        'N_values': [10, 50, 100, 500, 1000, 5000],  # Cluster sizes
        'K_simulations': 1000,    # Monte Carlo iterations
        'r_ratios': [10, 100, 1000]  # M_max/M_min ratios to test
        }
        2. MCMC Configuration (fast convergence)
        - Walkers: 20-50 (depends on parameter space)
        - Burn-in: 100 steps  
        - Production: 500 steps
        - Total: ~600 steps per fit (~few seconds each)
        3. CSV Output Structure
        iteration,N,M_min,M_max,alpha_true,fit_method,alpha_fit,alpha_uncertainty,convergence_status,timestamp
        4. Key Questions for Implementation:
        1. MCMC priors: Should I use uniform priors on alpha, or something more physically motivated (e.g., alpha ∈ 1, 4)?
        2. Convergence criteria: What threshold should determine if MCMC "failed" to converge? Gelman-Rubin statistic < 1.1?
        3. Progress tracking: Would you like real-time progress bars, or just periodic status updates?
        4. Experimental matrix: Should I vary:
        - Only N (keeping M_min/M_max fixed at 0.1/100)
        - Only mass ratio r (keeping N fixed)  
        - Both in a grid search?
        5. Analysis plots: Specific plots you want to see? I'm thinking:
        - Recovery precision (σ_α) vs N
        - Recovery bias (α_fit - α_true) vs N
        - Comparison of fitting methods
        - Effect of mass ratio r on precision
        Does this plan capture what you had in mind? Any adjustments needed


