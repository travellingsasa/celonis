def get_date():

    import datetime
    
    dt = datetime.datetime.now()
    
    return dt.strftime("%Y-%m-%d %H:%M").replace(':', '.')

def connect_to_celonis():

    from pycelonis import get_celonis
    
    celonis = get_celonis()
        
    return(celonis)


def select_datapool(celonis):
    
    pools = {"nr": [],"name": []}
    
    print(f"\nAvailable data pools:\n")
    
    for count, pool in enumerate(celonis.pools):
        
        pools['nr'].append(count)
        
        pools['name'].append(pool.name) 

        print(f"{count} : {pool.name}")

    while True:   

        user_input = input("\nPlease select a number or type the name of the data pool that you want to select:\n")
        
        if (not user_input.isnumeric() and user_input in pools['name']) or user_input.isnumeric() and int(user_input) in pools['nr']:

            if user_input in pools['name']:

                return(user_input)

            else:

                user_input = int(user_input)

                return(pools.get("name")[user_input])

        else:
            print(f'You have a typo somewhere. You typed: {user_input}') 



def get_datapool(celonis,pool_name = "SAP - ECC"):
    
    return (celonis.pools.find(pool_name))

def make_backup_dir():
    '''
    Creates a directory called backups in the current working directory.
    '''
    from pathlib import Path

    Path.mkdir(Path(Path.cwd(),'backups'), exist_ok=False)
    
    backup_dir = Path(Path.cwd(),'backups','backup - ' + get_date()) 
    
    Path.mkdir(backup_dir, exist_ok=False)
    
    return(backup_dir)

def is_empty_list(pth):
    
    return(len(pth) == 0)

def is_empty(file):
    
    return(file.stat().st_size == 0)

def no_markdowns(backup_dir):
    
    from pathlib import Path
    
    return(len(list(Path(backup_dir).glob("*." + 'py'))) == 0)


def get_job_name(job):
    return(job.name.replace(':', ' -'))
        
def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)


    
#-----------export helper-----------------------------------

def print_with_space(nr_spaces, string):
    print(' '* nr_spaces + string)


def export_transformations(backup_dir,job):
    
    
    pth  = []
    
    for tm in job.transformations:
        
        print_with_space(1,f' Exporting {tm.name}...') 
        
        pth.append(tm.backup_content(backup_dir))
    

    return(is_empty_list(pth))
    
                    
def get_exported_transformations(backup_dir,old_sffx):
    from pathlib import Path

    '''
    Gets the full name and base name of the sql export files and  
    sorts them according to time of last modification
    '''
    
    transformations_fullname = sorted(Path(backup_dir).glob("*." + old_sffx), key=lambda f: f.stat().st_mtime)
    
    return(transformations_fullname)

#-----------concat helper-----------------------------------

def make_md_fullname(backup_dir, job_name):
    
    from pathlib import Path
    
    return(Path(backup_dir, job_name  + '.md'))

def not_empty(file):
    return(file.stat().st_size != 0)

def add_header(markdown,tm):
    
    header = strip_transformation_name(tm)

    print_with_space(3,f'Adding {header}')

    markdown.write('# ' + header + '\n\n')

def add_text_as_code_block(markdown,file, code_style='sql'):
    
    with open(file) as infile:    

        markdown.write('```' + code_style + '\n')

        for line in infile:

            markdown.write(line)

        markdown.write('\n```\n\n')

def strip_transformation_name(file):
    from pathlib import Path
    
    return(Path(file).stem.rsplit('Backup of Transformation - ',1)[1])

def delete_exported_files(files):
    
    from pathlib import Path
    
    [Path.unlink(file) for file in files] 
    

def delete_empty_markdowns(backup_dir):
    
    from pathlib import Path
 
    for file in Path(backup_dir).glob("*." + 'md'):
    
        
        if file.stat().st_size == 0:
            
            print(f'{file} is empty. Will be deleted now ...')
            
            Path.unlink(file)
            
  
        
def concat_files(md_fullname, transformations_fullname):
    '''
    Loops through all transformations and concatinates the Celonis 
    
    exported sql files into one markdown file. Empty transformations 
    
    like Full and Delta Loads are skipped. A cleaned up version of the 
    
    file path is added as header and the script is added as a code block.
    
    Params:
    
    '''
    print_with_space(1, f'Creating {md_fullname}')

    with open(md_fullname, 'w') as markdown:
       
        for tm in transformations_fullname:
            
            if not_empty(tm):

                add_header(markdown,tm)

                add_text_as_code_block(markdown,tm)
            else:
                print(f'{strip_transformation_name(tm)} was an empty file.')

    print_with_space(4, f'Closing {md_fullname}')

    print_with_space(5, 'Deleting exported files\n')

    delete_exported_files(transformations_fullname)

    
def create_backup(data_pool ):

    backup_dir = make_backup_dir()

    for job in data_pool.data_jobs:

        job_name = get_job_name(job)

        print(f'Processing {job_name}...')

        no_transformation = export_transformations(backup_dir,job)


        if no_transformation:

            print(f'Skipping to next data job because transformation exports are empty.\n')

            continue

        else:

            transformations_fullname = get_exported_transformations(backup_dir, 'sql')

            md_fullname = make_md_fullname(backup_dir, job_name)

            concat_files(md_fullname, transformations_fullname)