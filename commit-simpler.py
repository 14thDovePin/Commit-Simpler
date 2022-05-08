import os
import sys


class CommitCurrentProject:
    """
    A script to commit the current project being worked on with ease.

    ...
    """

    pass

def write_cp_dir():
    """
    Writes "commit_cp.dat" that stores the current project directory.
    Before "commit_cp.dat" is written the input data is false checked
    first if its a valid directory and a repositry simply by checking
    the ".git" directory inside the directory.

    Writes "Current Commit Notes.txt" inside the current project directory.
    Here is where the notes for current project changes can be typed at, and
    the text is then used for the project commit. 
    [git commit -am "Current Commit Notes"]
    """
    print('CurrentProjectDirectory NotFound OR DirectoryNotRepository!')
    while True:
        current_project_dir = input('Input CurrentProjectDirectory: ')
        if os.path.exists(current_project_dir):
            print("\tDirectory Stored!\n")
            git_check = os.path.join(current_project_dir, ".git")
            if os.path.exists(git_check):
                break
            else:
                print("\tDirectoryNotRepository!")
        else:
            print("\tInvalidDirectory!")

    with open("commit_cp.dat", 'w') as f:
        f.write(current_project_dir)

    current_commit_notes = \
    f"{os.path.join(current_project_dir, 'Current Commit Notes.txt')}"
    with open(current_commit_notes, 'w') as f:
        pass


def check_file_integrity():
    """
    Checks if "commit_cp.dat" exists in currend working directory.
    Checks if data stored inside "commit_cp.dat" is a valid directory.
    Checks if the valid directory is a git repository.
    Checks if "Current Commit Notes.txt" exists in the valid directory. ##
    If any of the check fails, control flow is
    redirected to the function "write_cp_dir".
    Returns the valid directory.
    """
    if not os.path.exists("commit_cp.dat"):
        print('"commit_cp.dat" NotFound!')
        write_cp_dir()

    with open("commit_cp.dat", 'r') as f:
        current_project_dir = f.readline()

    if not os.path.exists(current_project_dir):
        print('InvalidDirectory!')
        write_cp_dir()

    git_check = os.path.join(current_project_dir, ".git")
    if not os.path.exists(git_check):
        print('DirectoryNotRepository!')
        write_cp_dir()

    com_txt = os.path.join(current_project_dir, 'Current Commit Notes.txt')
    if not os.path.exists(com_txt):
        print('"Current Commit Notes.txt" NotFound!')
        write_cp_dir()

    return current_project_dir


def print_gl(cpd):
    """
    Prints the last 3 git logs.
    """
    cwd = os.getcwd()
    fname = 'commit_cp.temp'
    cmd = f'git log --pretty=reference >> "{os.path.join(cwd, fname)}"'
    os.chdir(cpd)
    os.system(cmd)
    os.chdir(cwd)

    with open('commit_cp.temp', 'r') as f:
        commit_notes = f.readlines()
    os.remove(fname)
    print(fname)

    [print('*'+i.replace('\n', '')) for i in commit_notes[:3]]


def commit_project(cpd):
    """
    Displays commit notes as it is from text file and asks for confirmation.
    And finally commit current project.
    """
    print('\nCommiting Project..')

    fdir = os.path.join(cpd, 'Current Commit Notes.txt')
    with open(fdir) as f:
        cnotes = f.readlines()

    if cnotes:
        print('\nCommit Notes:\n')
        [print(i.replace('\n', '')) for i in cnotes]
    else:
        print('Warning there are no notes found in "Current Commit Notes.txt"')
        print(f'located at "{cpd}".')
        print('It is recommended to add a message during commits.')
        print('Are you sure you wish to commit? (y/n)')

        uinput = input()
        if uinput.lower() == 'y':
            pass
        elif uinput.lower() == 'n':
            main()
        else:
            commit_project()


def main():
    # Check if file for storing current project
    # directory exists if not create new file.
    """
    Checks if 
    """
    print('\nCommit Current Project\n')
    
    current_project_dir = check_file_integrity()

    print(f'Current Project Path: "{current_project_dir}"')
    print('Type [cdcp] to change the directory of the current project.')

    print('\nRecent Commits..\n')
    print_gl(current_project_dir)

    print('\nCommit Project? (y/n)')
    main_input = input()

    if main_input.lower() == 'y':
        commit_project(current_project_dir)
    elif main_input.lower() == 'n':
        sys.exit()
    elif main_input.lower() == 'cdcp':
        print('\nClearing CurrentProjectDirectory..')
        write_cp_dir()
    else:
        main()


if __name__ == "__main__":
    main()
