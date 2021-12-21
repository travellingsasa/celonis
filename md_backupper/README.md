## md_backupper
This script should be executed from the pycelonis ML workbench.

Run from bash/zsh
 
```bash
python md_backupper/md_backupper.py
```


- It connects to Celonis 

- Creates a backups folder in your home directory

- Asks the users which data pool they want to use

- It loops through all data jobs

- Exports the transformations

- Creates a markdown file for each non-empty data job by

  concatinating the exported files and adding them as code block 


Result:

You will get as many or fewer markdown files as data jobs in your pool. 

The Full Load and Delta Load transformations contain no sql scripts. This 

is why we won't create a markdown file for them. This way the directory 

structure from the Event Collection view is preserved as opposed to looping 

through all transformations and saving them in one directory. Also youl'll 

have searchable files.


TODO: 

automatic file download