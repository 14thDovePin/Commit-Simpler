import os
import subprocess
import sys


class CommitCurrentProject:
    """
    A script to manage git commits and notes when working on projects.
    """

    def __init__(self):
        """Initialize variable for current project directory."""
        self.current_project_directory = ''
        self.reprint_git_status = False
        # Content for "Current Commit Notes.txt" upon inception.
        self.fcontent = [
            'Subject (Main subject of the commit.)\n',
            '\n',
            'Body (Detailed description of changes before commit.)\n',
            ]


    def check_integrity(self):
        """
        Check for file and data integrity before usage of script.

        Check if "commit_cp.dat" exists in currend working directory.
        Check if data stored inside "commit_cp.dat" is a valid directory.
        Check if the valid directory is a git repository.
        If the last three checks before this line fails, control flow will be
        redirected to the method "write_cp_dir".
        Check if "Current Commit Notes.txt" exists in the valid directory.
        If the check before this line fails, control flow will be redirected to
        the method "commit_notes" with param 'Options="renew"'.
        Redirect control flow to "git_ignore" method.
        Store the directory name of the project's directory inside a class
        variable.
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

        fname = 'Current Commit Notes.txt'
        com_txt = os.path.join(self.current_project_directory, fname)
        if not os.path.exists(com_txt):
            print(f'"{fname}" NotFound!')
            self.commit_notes(Option='renew')

        self.git_ignore()

        project_name = self.current_project_directory.split('\\')
        self.project_name = project_name.pop()


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


    def git_ignore(self):
        """Assures that ".gitignore" file excludes script and git files.

        Check if ".gitignore" file does NOT exists.
            If so, create file.
        Check if any item inside 'lines' list file does NOT exists.
            If so, append line to the file.
        """
        lines = [
            ".gitignore\n",
            ".git\n",
            "__pycache__/\n",
            "Current Commit Notes.txt\n",
            ]
        fname = ".gitignore"
        fdir = os.path.join(self.current_project_directory, fname)

        if not os.path.exists(fdir):
            with open(fdir, 'w') as f:
                pass
        with open(fdir, 'r') as f:
            file = f.readlines()
        for line in lines:
            if line not in file:
                with open(fdir, 'a') as f:
                    f.write(line)


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

        Join file name and current project directory.
        If Option str arg is 'renew', then create file.
        If Option str arg is 'read', then return readlines() of file.
        """
        fname = 'Current Commit Notes.txt'
        commit_notes_dir = \
        f"{os.path.join(self.current_project_directory, fname)}"

        if Option == 'renew':
            with open(commit_notes_dir, 'w') as f:
                f.writelines(self.fcontent)
            print('"Current Commit Notes.txt" Renewed!\n')
        elif Option == 'read':
            with open(commit_notes_dir, 'r') as f:
                return f.readlines()


    def print_last_logs(self):
        """
        Neatly prints the last 3 git logs.

        Creates a subprocess.
        Subprocess runs a prettified git log command with max count 3 and pipes
        subprocess output to current script output.
        """
        f1 = 'format:"%C(brightyellow)%H%Creset  %C(brightgreen)%aD '
        f2 = '%C(brightred)| %C(BrightCyan)%ar%n    %s"'
        cmd1 = f'git -C "{self.current_project_directory}" log --pretty'
        cmd2 = f'={f1+f2} --max-count=3'
        command = cmd1+cmd2

        subprocess.run(command, stdout=sys.stdout, text=True)


    def check_git_status(self):
        """
        Checks the current project's git status.

        Checks the current git status output if working directory is clean or
        there are any untracked files. If working directory is clean then end
        script. If there are untracked files. Return False. Otherwise return
        True.
        """
        command = f'git -C "{self.current_project_directory}" status'

        txt = 'nothing to commit, working tree clean'
        txt1 = 'Untracked files:'
        sp = subprocess.run(command, capture_output=True, text=True)

        if sp.stdout.find(txt) != -1:
            print('Git Working Tree is clean!')
            print('Script ending..')
            sys.exit()
        if sp.stdout.find(txt1) != -1:
            print('Untracked Files Detected!\n')
            return False

        return True


    def print_git_status(self):
        """
        Prints the current git status and prompts for certain actions.

        Subprocess runs a git status command on the current project directory,
        and pipes subprocess output to current script output.
        Redirect control flow to "check_git_status" method and assign return
        value to a variable.
        if value is False then prompt to add files to staging area
        automatically.
            If prompt was accepted, break loop and redirect method to itself.
        """
        command = f'git -C "{self.current_project_directory}" status'
        subprocess.run(command, stdout=sys.stdout)

        check = self.check_git_status()
        if not check:
            msg1 = 'Do you wish to add untracked files to staging area? '
            msg2 = '(y/n) '
            prompt_msg = msg1+msg2
            while True:
                uinput = input(prompt_msg)

                if uinput.lower() == 'y':
                    self.reprint_git_status = True
                    print()  # Purely Asthetic
                    subprocess.run(
                        'git add *',
                        cwd=self.current_project_directory,
                        stdout=sys.stdout
                        )
                    break
                elif uinput.lower() == 'n':
                    print()  # Purely Asthetic
                    break

        if self.reprint_git_status:
            self.reprint_git_status = False
            print('\n\nGIT STATUS\n----------\n')
            self.print_git_status()
        else:
            print()  # Purely Asthetic


    def print_commit_messages(self):
        """
        Prints the commit messages stored for review before final prompt.

        Redirect control flow to "check_git_status" method.
        Pull commit notes by using the method "commit_notes" with param
        'Options="read"'.
        Check if pulled data is same as 'fcontent' class variable or not.
        If data is the same, print warning to console.
            Then prompt user whether to leave data empty or not.
                If yes then pass.
                If no then prompt exit.
        If data is not the same, touch up string and print them.
        """
        check = self.check_git_status()
        commit_messages = self.commit_notes(Option='read')

        if commit_messages == self.fcontent or not commit_messages:
            print('Warning! There are no commit message/s found!')
            msg1 = 'Leaving "Current Commit Notes.txt" empty/unchanged will '
            msg2 = 'result in the git log commit message\nto contain the '
            msg3 = 'template contents of the file instead once the current '
            msg4 = 'commit is finalized!\n'
            print(msg1+msg2+msg3+msg4)
            while True:
                txt1 = 'Are you sure you wish to leave '
                txt2 = 'the message empty? (y/n) '
                uinput = input(txt1+txt2)
                if uinput.lower() == 'y':
                    break
                elif uinput.lower() == 'n':
                    print('\nPlease make the necessary changes..')
                    print('Script Ending...')
                    sys.exit()
        else:
            [print(i.replace('\n','')) for i in commit_messages]


    def commit_project(self):
        """
        Finalize command and commits the current project.

        Print commiting status and project name.
        Pull commit notes by using the method "commit_notes" with param
        'Options="read"'.
        Finalize git command string.
        Commit using subprocess.
        Renew "Current Commit Notes.txt"
        End script.
        """
        print(f'\nCommiting Project.. [{self.project_name}]\n')

        cmd1 = f'git -C "{self.current_project_directory}" commit'
        cmd2 = f' -a -F "{self.current_project_directory}'
        cmd3 = '\\Current Commit Notes.txt"'
        command = cmd1+cmd2+cmd3
        
        print(command)
        subprocess.run(command, stdout=sys.stdout, check=True)
        print('\nRenewing.. "Current Commit Notes.txt"')
        self.commit_notes(Option='renew')
        print('Script Ending...')
        sys.exit()


    def help(self):
        """Prints details about other input options/commands."""
        print('\n[cdcp] - Change current project directory.')
        print('[exit] - Stop and end script.\n')


    def start(self):
        """Starts the control flow of the script.

        Redirect control flow to "check_integrity" method.
        Redirect control flow to "print_last_logs" method.
        Redirect control flow to "print_commit_messages" method.
        Redirect control flow to "print_git_status" method.
        Initiate loop.
        Prompt user to initiate command prompt.
            If yes, subprocess initiate cmd in current project directory.
            If no, break current loop.
        Initiate loop.
            Prompt user for input.
            If input y, then redirect control flow to "commit_project"
            method.
            If input n, then end script.
            If input cdcp, then redirect control flow to "write_cp_dir"
            method, and finally break loop.
            If input exit, then end script.
            If input help, then redirect control flow to "help" method.
        Redurect control flow to "start" method.
        """
        print('\nCommit Current Project\n')
        
        self.check_integrity()
        print(f'Project Directory Name: [{self.project_name}]')
        print(f'Project Path: "{self.current_project_directory}"')

        print('\n\nRECENT COMMITS\n--------------\n')
        self.print_last_logs()

        print('\nCOMMIT MESSAGE\n--------------\n')
        self.print_commit_messages()

        print('\nGIT STATUS\n----------\n')
        self.print_git_status()

        print('Type [help] to see more commands & details.')
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
            elif main_input.lower() == 'help':
                self.help()

        self.start()


if __name__ == "__main__":
    main = CommitCurrentProject()
    main.start()
