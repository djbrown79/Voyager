# Voyager: An Open-Ended Embodied Agent with Large Language Models
<div align="center">

[[Website]](https://voyager.minedojo.org/)
[[Arxiv]](https://arxiv.org/abs/2305.16291)
[[PDF]](https://voyager.minedojo.org/assets/documents/voyager.pdf)
[[Tweet]](https://twitter.com/DrJimFan/status/1662115266933972993?s=20)

[![Python Version](https://img.shields.io/badge/Python-3.9-blue.svg)](https://github.com/MineDojo/Voyager)
[![GitHub license](https://img.shields.io/github/license/MineDojo/Voyager)](https://github.com/MineDojo/Voyager/blob/main/LICENSE)
______________________________________________________________________


https://github.com/MineDojo/Voyager/assets/25460983/ce29f45b-43a5-4399-8fd8-5dd105fd64f2

![](images/pull.png)


</div>

We introduce Voyager, the first LLM-powered embodied lifelong learning agent
in Minecraft that continuously explores the world, acquires diverse skills, and
makes novel discoveries without human intervention. Voyager consists of three
key components: 1) an automatic curriculum that maximizes exploration, 2) an
ever-growing skill library of executable code for storing and retrieving complex
behaviors, and 3) a new iterative prompting mechanism that incorporates environment
feedback, execution errors, and self-verification for program improvement.
Voyager interacts with GPT-4 via blackbox queries, which bypasses the need for
model parameter fine-tuning. The skills developed by Voyager are temporally
extended, interpretable, and compositional, which compounds the agent’s abilities
rapidly and alleviates catastrophic forgetting. Empirically, Voyager shows
strong in-context lifelong learning capability and exhibits exceptional proficiency
in playing Minecraft. It obtains 3.3× more unique items, travels 2.3× longer
distances, and unlocks key tech tree milestones up to 15.3× faster than prior SOTA.
Voyager is able to utilize the learned skill library in a new Minecraft world to
solve novel tasks from scratch, while other techniques struggle to generalize.

In this repo, we provide Voyager code. This codebase is under [MIT License](LICENSE).

# Installation
Voyager requires Python 3.10 and Node.js ≥ 16.13.0.

If you don't have them already, please download and install the following:

- [Python Download](https://www.python.org/downloads/release/python-31011/)
- [Node.js Download](https://nodejs.org/en/download/package-manager)

## Minecraft Installation

[Modrinth](https://modrinth.com/) is recommended for setting up your Minecraft client. You can also 
use any means you're comfortable with to install the necessary mods. 

In Modrinth, create a new profile and call it "Voyager" (or some other name meaningful to you). Use
Minecraft version 1.19.4. Install the following content:

- CompleteConfig 2.3.1
- Fabric API 0.87.2+1.19.4
- Mod Menu 6.3.1
- Multiplayer Server Pause 1.3.0
- iChunUtil 1.0.0

Modrinth will automatically select compatible versions: you don't have to specify them manually.
## Voyager Installation

In the Command Prompt, navigate to the Voyager repo and type the following: 
```
voyager install
```

You will see the following on the screen:
```
>voyager install
Starting installation...
Checking Python version...
Found Python version 3.10.11

Enter your OpenAI API key:
```
Copy and paste your OpenAI API Key and hit enter. It will be invisible when you paste it.

Next, you will see the following:
```
Available OpenAI models:
1. gpt-4
2. gpt-4o
3. gpt-4o-mini

Select a model by entering the corresponding number:
```
Select the OpenAI model you want to use. GPT-4 is the most capable, but also very expensive. Consider
starting with GPT-4o for the most balanced experience. After this, the installation should complete
after a few minutes.

Should you ever want to change these options, you can edit the `.env` file.

You should see the following:
```
✅ .env file created successfully!

Your configuration has been saved in '.env'.

Checking Node.js version...
Found Node.js version 22.12.0
Removing existing virtual environment...
Creating new virtual environment...
Activating virtual environment...
Installing Python dependencies...
Setting up Mineflayer environment...
Installing Node.js dependencies...
Setting up mineflayer-collectblock...

Installation completed successfully!
Run 'voyager.bat' without parameters to start the application.
```
## Let's Go!

After the installation process, you will need to start Minecraft.
  1. Start a single player game with Game Mode set to `Creative` and Difficulty set to `Peaceful`. 
  2. After the world is created, press the `Esc` key and press `Open to LAN`. 
  3. Select `Allow cheats: ON` and press `Start LAN World`. 

Once Minecraft is ready, you can run Voyager by executing the following on the Windows Command Prompt:
```
voyager
```
### First Run 
Note: The first time you run, answer "no" when prompted. On subsequent runs answer "yes".
```
>voyager
Starting Voyager...
                  _   _
                 | | | |
                 | | | | ___  _   _  __ _  __ _  ___ _ __
                 | | | |/ _ \| | | |/ _` |/ _` |/ _ \ '__|
                 \ \_/ / (_) | |_| | (_| | (_| |  __/ |
                  \___/ \___/ \__, |\__,_|\__, |\___|_|
                               __/ |       __/ |
                              |___/       |___/

        An Open-Ended Embodied Agent with Large Language Models

                          original authors:
             Guanzhi Wang and Yuqi Xie and Yunfan Jiang and
              Ajay Mandlekar and Chaowei Xiao and Yuke Zhu
                  and Linxi Fan and Anima Anandkumar

Do you want to continue from your previous session? (yes/no):
```

Enjoy!

# Advanced
## Resume from a checkpoint during learning

If you stop the learning process and want to resume from a checkpoint later, you can update `__main__.py` (as shown below) and restart Voyager:
```python
voyager = Voyager(
    mc_port=mc_port,
    openai_api_key=openai_api_key,
    ckpt_dir="YOUR_CKPT_DIR",
    resume=True
)
```

## Run Voyager for a specific task with a learned skill library

If you want to run Voyager for a specific task with a learned skill library, you should first pass the skill library directory to Voyager by making the following changes to `__main__.py` and restarting:
```python
# First instantiate Voyager with skill_library_dir.
voyager = Voyager(
    mc_port=mc_port,
    openai_api_key=openai_api_key,
    skill_library_dir="./skill_library/trial1", # Load a learned skill library.
    ckpt_dir="YOUR_CKPT_DIR", # Feel free to use a new dir. Do not use the same dir as skill library because new events will still be recorded to ckpt_dir. 
    resume=False, # Do not resume from a skill library because this is not learning.
)
```
Then, you can run task decomposition. Notice: Occasionally, the task decomposition may not be logical. If you notice the printed sub-goals are flawed, you can rerun the decomposition.
```python
## Run task decomposition
task = "YOUR TASK" # e.g. "Craft a diamond pickaxe"
sub_goals = voyager.decompose_task(task=task)
```
Finally, you can run the sub-goals with the learned skill library:
```python
voyager.inference(sub_goals=sub_goals)
```

For all valid skill libraries, see [Learned Skill Libraries](skill_library/README.md).

# FAQ
If you have any questions, please check our [FAQ](FAQ.md) first before opening an issue.

# Original Paper and Citation

If you find our work useful, please consider citing us! 

```bibtex
@article{wang2023voyager,
  title   = {Voyager: An Open-Ended Embodied Agent with Large Language Models},
  author  = {Guanzhi Wang and Yuqi Xie and Yunfan Jiang and Ajay Mandlekar and Chaowei Xiao and Yuke Zhu and Linxi Fan and Anima Anandkumar},
  year    = {2023},
  journal = {arXiv preprint arXiv: Arxiv-2305.16291}
}
```

Disclaimer: This project is strictly for research purposes, and not an official product from NVIDIA.
