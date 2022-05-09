import os
import subprocess
import sys


class CommitCurrentProject:
    """
    A script to manage git commits and notes when working on projects.

    ...
    """

    def __init__(self):
        """Constructor docstring."""
        current_project_directory = ''


    def check_integrity(self):
        """
        Check for file and data integrity before usage of script.

        Check if "commit_cp.dat" exists in currend working directory.
        Check if data stored inside "commit_cp.dat" is a valid directory.
        Check if the valid directory is a git repository.
        If the last three checks before this line fails, control flow will be
        redirected to the function "write_cp_dir".
        Check if "Current Commit Notes.txt" exists in the valid directory.
        If the check before this line fails, control flow will be redirected to
        the function "commit_notes" with param 'Options="renew"'.
        Returns the valid directory.
        """
        if not os.path.exists("commit_cp.dat"):
            print('"commit_cp.dat" NotFound!')
            self.write_cp_dir()

        with open("commit_cp.dat", 'r') as f:
            self.current_project_directory = f.readline()

        if not os.path.exists(self.current_project_directory):
            print('DirectoryInvalid!')
            self.write_cp_dir()

        git_check = os.path.join(self.current_project_directory, ".git")
        if not os.path.exists(git_check):
            print('DirectoryNotRepository!')
            self.write_cp_dir()

        com_txt = os.path.join(self.current_project_directory, 'Current Commit Notes.txt')
        if not os.path.exists(com_txt):
            print('"Current Commit Notes.txt" NotFound!')
            self.commit_notes(Option='renew')

        return self.current_project_directory


    def write_cp_dir(self):
        """
        Asks for current project directory to be checked and stored.

        Check if input directory is a valid directory.
        Check if input directory contains ".git" directory.
        Stores input to file "commit_cp.dat".
        """
        while True:
            input_directory = input('Input New CurrentProjectDirectory: ')
            if os.path.exists(input_directory):
                git_check = os.path.join(input_directory, ".git")
                if os.path.exists(git_check):
                    print("\tDirectory Stored!\n")
                    break
                else:
                    print("\tDirectoryNotRepository!")
            else:
                print("\tDirectoryInvalid!")

        self.current_project_directory = input_directory
        with open("commit_cp.dat", 'w') as f:
            f.write(input_directory)


    def commit_notes(self, Option):
        """
        Renews "Current Commit Notes.txt" inside current project directory.

        Parameters
        ----------
        Option : str
            'renew' : Renews "Current Commit Notes.txt".
            'read' : Returns string bt 'readlines()' from
            "Current Commit Notes.txt".

        Notes
        -----
        "Current Commit Notes.txt" is the file for the developer to write and
        save his/her current projects commit messages at. Its contents will be
        read by the script and be sliced into the final commit command before
        being prompted for the last time before the final commit initiates.
        Once the commit is done the file will then be wiped clean for the new
        commit messages to be saved into.
        """
        fname = 'Current Commit Notes.txt'
        commit_notes_dir = \
        f"{os.path.join(self.current_project_directory, fname)}"

        if Option == 'renew':
            with open(commit_notes_dir, 'w') as f:
                pass
            print('"Current Commit Notes.txt" Created!\n')
        elif Option == 'read':
            with open(commit_notes_dir, 'r') as f:
                return f.readlines()


    def print_last_logs(self):
        """
        Neatly prints the last 3 git logs.

        Creates a subprocess.
        Subprocess runs a prettified git log with max count 3.
        Pipes subprocess output to current script output.
        """
        cmd1 = 'git --git-dir "C:\\Users\\Dit Laforteza\\Desktop\\'
        cmd2 = 'Main Project\\Skyrim-Alchemy-Booklet - Copy\\'
        cmd3 = '.git" log --pretty=reference --max-count=3'

        sp = subprocess.run(cmd1+cmd2+cmd3, stdout=sys.stdout, text=True)


    def print_commit_messages(self):
        """
        Prints the commit messages stored for review before final prompt.

        Pull commit notes by using the function "commit_notes" with param
        'Options="read"'.
        Check if pulled data is empty or not.
        If data is not empty, touch up string and print them.
        If data empty, print warning to console.
            Then prompt user whether to leave data empty or not.
                If yes then pass.
                If no then prompt exit.
        ......
        """
        commit_messages = self.commit_notes(Option='read')

        if commit_messages:
            [print(i.replace('\n','')) for i in commit_messages]
        else:
            print('Warning! There are no commit message found!')
            msg1 = 'Leaving "Current Commit Notes.txt" empty will result in '
            msg2 = 'the git log commit message empty once the current commit '
            msg3 = 'is finalized!\n'
            print(msg1+msg2+msg3)
            while True:
                txt1 = 'Are you sure you wish to leave '
                txt2 = 'the message empty? (y/n)'
                uinput = input(txt1+txt2)
                if uinput.lower() == 'y':
                    break
                elif uinput.lower() == 'n':
                    print('\nPlease make the necessary changes..')
                    input('Press "Enter" to end the script.')
                    sys.exit()


    def commit_project(self):
        """
        Finalize command and commits the current project.

        # f'git --git-dir "{self.current_project_directory}" commit -a -F "Current Commit Notes.txt"'

        Print commiting project and the project name.
        Pull commit notes by using the function "commit_notes" with param
        'Options="read"'.

        """
        project_name = self.current_project_directory.split('\\')
        project_name = project_name.pop()
        print(f'\nCommiting Project.. [{project_name}]\n')

        # commit_messages = self.commit_notes(Option='read')
        # command = 


    def start(self):
        """Starts the control flow of the script."""
        print('\nCommit Current Project\n')
        
        self.check_integrity()

        print(f'Current Project Path: "{self.current_project_directory}"')
        print('Type [-help] to see more commands details.')

        print('\nRecent Commits..\n')
        self.print_last_logs()

        print('\nCommit Message..\n')
        self.print_commit_messages()
        print()  # Purely asthetics

        while True:
            main_input = input('Commit Project? (y/n) ')

            if main_input.lower() == 'y':
                self.commit_project()
            elif main_input.lower() == 'n':
                print('\nScript Ending...')
                sys.exit()
            elif main_input.lower() == 'cdcp':
                self.write_cp_dir()
                break
            elif main_input.lower() == 'exit':
                sys.exit()
            elif main_input.lower() == '-help':
                self.help()

        self.start()


    def help(self):
        """Prints details about other input options/commands."""
        print('\n[cdcp] - Change current project directory.')
        print('[exit] - Stop and end script.')


if __name__ == "__main__":
    main = CommitCurrentProject()
    main.start()
