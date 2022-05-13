## Commit-Simpler

This script commits your project neatly while providing information about your current project's commit status for ease of work.

The script creates a text file named "Current Commit Notes.txt" inside your current project's directory at its initialization. This file is where you will store your current commit's notes and messages. The contents of this file will be the message of the final *git commit* command. Once the commit command has been finalized and initiated. This file will be renewed to just as it was in its inception, ready for more messages. The text file is automatically ignored inside the "*.gitignore*" file of the repository.

## How it works

   At the script's initial run, it will *prompt* the developer[^1] to *input their current project's directory* for it to be stored and used at later runs. It then creates a text file "*Current Commit Notes.txt*" inside the current project's directory using the stored data. This file is automatically excluded inside the ".gitignore" file at its inception. This is where the *commit message* will be pulled from when the script constructs the command and commits the project. Therefore it is crucial  for the developer to write their commit messages inside the text file or they will be *prompted* by the script when committing.

When committing, the script will print out the current project's name, its directory, 3 of the most recent logs, the commit messages, and its current *git status* so that the developer can review the project's commit in more details. If the git *working directory* is clean, the script will prompt the developer for an input if they wish to exit or change the *current project directory*. If there are any *unstaged* and/or *untracked* files. The script will *prompt* the developer whether or not if they wish to initiate the command  [*git add \**]. Doing so the script will initiate the command, otherwise it will not do anything to the current *git working tree*.

Once all of the prerequisites of the commit has been accounted for, the script will prompt the developer one last time if they wish to finalize the command and initiate commit.[^2] Doing so, the script will print out the finalized command before proceeding to initiate the commit. The script ends after the script has finished the command.

### Developer Notes
Creating this script was quite fun and has taught me a lot as a developer. Using git, its proper commit message convention, managing a bit of rebase, using the proper docstring convention of Python functions, methods, and classes according to [PEP-0257](https://peps.python.org/pep-0257/), and structuring the overall control flow of the script, has broaden my horizons and improved my thoughts as a developer.

Although the script's control flow and code structure is a bit of a mess (actualy might be too much lol), there is still so much to learn in structuring and writing fast and efficient code. I am personally happy by this simple yet intricate project of mine. Thank you for reading through my self thoughts and my comments about my journey. Cheers for a long and fruitful journey!

[^1]: I presume that most people here are developers. :D
[^2]: Developers are also presented with the option to change the *current project directory*.
