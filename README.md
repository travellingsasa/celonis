# A soon to be collection of helpful pycelonis scripts

## md_backupper
This script should be executed from the pycelonis ML workbench.

Run in bash
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

## Event collection view
![event_collection_view](https://user-images.githubusercontent.com/21205508/147008910-adc3987b-b1ea-41fb-854a-8cfa1c2f67cc.png)

## ML workbench view after running the script
![workbench_view](https://user-images.githubusercontent.com/21205508/147009294-aca97ec8-1ecc-435e-9995-331b5e5c34ee.png)


TODO: 

automatic file download
