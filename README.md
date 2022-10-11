### Write a command line program in Python3 that will do the following:
- It will be able to execute two different commands: 'scan' and 'detect'.
- Command 'scan' will receive parameter (or multiple parameters) with directory path(s) to be
scanned.
  - It will scan for all files in those directories and all their subdirectories (to a maximum
  depth).
  - It will generate metadata about the files and save it to result file (in format you prefer).
  - The result file destination will be also specified by user as a parameter.
- Command 'detect' will take the result file generated by command scan (as a parameter) and it
will re-scan the directories and detect changes.
  - It will generate output with information describing which files were added, which were
  removed, which stayed the same and witch were modified (by content).
  - The output will be saved to file in destination defined by user as a parameter (in format
  you prefer).
- Program should log meaningful events and allow user to select log verbosity (support multiple
levels). Allow user the option to specify log output destination (console, logfile).
- The solution should support synchronous and asynchronous (asyncio) implementation of both
commands. Please note that synchronous processing may be faster in this case.


### Arguments for running:  
`scan` or `detect` (internaly argument 'run_option')  

`-d`, `--directory`: One or more paths to directories to execute scan or detect on  
- Note:  You will likely want to run detect with the same directories that were used to run scan with, as doing otherwise will result in detecting removed and new files  

`-m`, `--metadata`: File to save `scan` output and to load for `detect` comparison

`-v`, `--verbose`:  0-2  
- Amount of information printed by `detect`  
  - 0: prints files changed  
  - 1: adds metadata changed (e.g. size)  
  - 2: adds metadata values changed (e.g. from 3 to 6)  

`-l`, `--log`: File to save `detect` output  

`-a`, `--asyncio`: Run command asynchronously