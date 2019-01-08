#!/usr/bin/env python3

from git import Repo
import os
import re
import sys
import subprocess
from pprint import pprint

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# max size of a patch in bytes - bigger than that and we get issues with delivery to mailing lists
MAX_PATCH_SIZE = 200000

SIGNOFF='Jan Tulak <jtulak@redhat.com>'

PATCHES = [
    #	{'script': '0.sh',
    # 'msg': '''xfsdump: (style) remove trailing whitespaces
    #
    #There were many trailing whitespaces through the whole code. As the rate
    #of changes in xfsdump is low, it should not cause trouble if we fix it
    #in all files at once and avoid issues (unintended changes) with sensibly
    #configured editors that automatically remove these on a file save.''',
    #     'source_file': '0.sh'},
    #
    #
    #    {'script': '1.sh',
    #     'msg': '''xfsdump: do not split function call with ifdef
    #
    #In two files in xfsdump, a function call is split in half by an ifdef
    #macro to conditionally pick an argument at compile time. This causes the
    #code to be a bit less obvious and some analysis tools have trouble with
    #understanding it.
    #
    #So, instead of splitting the function in half, move the whole function
    #call into each of the ifdef macros.'''},
    #
    #    {'script': '1c.sh',
    #     'msg': '''common/types.h: Wrap #define UUID_STR_LEN 36 in #ifndef
    #
    #Current Fedora 28 has the constant it in uuid/uuid.h where it belongs (per
    #comment next to the define), so we should treat the define as a
    #backward-compatibility workaround, rather than enforcing it for all.'''},
    #
    #
    #    {'script': '1c.sh',
    #     'msg': '''common/drive.c: include stdlib.h
    #
    #We are using calloc() inside of this file, but it is not included in any
    #way (resultin in "implicit declaration" warnings from the compiler). So,
    #add the include.'''},
    #

    #    {'script': '2.sh',
    #     'msg': '''xfsdump: (style) remove spaces from parentheses
    #
    #Transform "( x, y )" to "(x, y)", and the same for [].''',
    #     'source_file': '2.sh'},
    #
    #
    #    {'script': '3.sh',
    #     'msg': '''xfsdump: (style) remove spaces in front of commas/semicolons

    #Turn all the "x , y , z" into "x, y, z" and "for (moo ; foo ; bar)"
    #to "for (moo; foo; bar)". The only exception is a double semicolon surrounded
    #by some other commands, e.g. for(bar ; ; baz), for increased readability.''',
    #     'source_file': '3.sh'},

    #
    ## do not use for all, requires manual changes
    ##    {'script': '4.sh',
    ##     'msg': '''xfsdump: (style) remove spaces in ptr dereferences''',
    ##     'source_file': '4.sh'},


    #    {'script': '5.sh',
    #     'msg': '''xfsdump: add a space after commas and semicolons where was none
    #
    #A simple change: x,y -> x, y
    #Manual modifications were for re-alignment, because expressions length changed, and when a few lines got over 80 chars.''',
    #     'source_file': '5.sh'},
    #
    #
        {'script': '6.sh',
         'msg': '''xfsdump: (style) insert a newline between type and fnt name in definitions
    
    The xfs style we want to have after this patch is:
    
    int
    foo(...)
    
    This patch only changes .c files. .h files use one-line style for
    declarations, as is the custom in xfsprogs.
    
    int foo(...)''',
         'source_file': '6.sh'},
    
    #
    #    {'script': '7.sh',
    #     'msg': '''xfsdump: (style) add a space after if, switch, for, do, while
    #
    #There should be a space in "if(" -> "if (", etc...''',
    #     'source_file': '7.sh'},
    #
    #
    #    {'script': '8.sh',
    #     'msg': '''xfsdump: (style) add first empty line for multiline comments
    #
    #Change the multiline comment style from /* foo to /*\n * foo''',
    #     'source_file': '8.sh'},
    #
    #
    #    {'script': '9.sh',
    #     'msg': '''xfsdump: (style) curly brackets should wrap with one space
    #
    #Add a space where it is missing "\{foo\}", and remove it where are
    #too many "{   foo   }".''',
    #     'source_file': '9.sh'},
    #
    #
    #exit 0
    #
    #    {'script': '10.sh',
    #     'msg': '''xfsdump: (style) indent and align the code
    #
    #Tab length is 8 spaces.''',
    #     'config_file': 'linux10.cfg'},
    #
    #
    #    {'script': '11.sh',
    #     'msg': '''xfsdump: (style) format intercharacter spaces
    #
    #This patch changes intercharacter spaces, e.g. adds a space around binary
    #operators, removes multiple spaces where they are not used for alignment,
    #removes a space in a function header ("fnt ()" -> "fnt()"), etc.''',
    #     'config_file': 'linux11.cfg'},
    #
    #
    #    {'script': '12.sh',
    #     'msg': '''xfsdump: (style) format newlines
    #
    #Add and remove newlines to conform to the xfs/kernel coding style.''',
    #     'config_file': 'linux12.cfg'},
    #
    #
    #    {'script': '13.sh',
    #     'msg': '''xfsdump: (style) add stars to multiline comments
    #
    #All lines of multiline comments should begin with a star.''',
    #     'config_file': 'linux13.cfg'},
    #
    #
    #    {'script': '14.sh',
    #     'msg': '''xfsdump: (style) remove parentheses after return
    #
    #"return (foo);" -> "return foo;"''',
    #     'config_file': 'linux14.cfg'},
]

class PatchInfo(object):
    """ An instance of one specific patch, including it's message """

    #def __init__(self, scripts_path, script, msg, source_file=None, config_file=None):
    def __init__(self, scripts_path, item):
        self.scripts_path = scripts_path
        self.script = os.path.join(scripts_path, item['script'])
        self.msg = item['msg']
        self.source_file = item.get('source_file', None)
        self.config_file = item.get('config_file', None)
        if self.source_file:
            self.source_file = os.path.join(scripts_path, self.source_file)
        if self.config_file:
            self.config_file = os.path.join(scripts_path, self.config_file)

        # ok, now add the source for whatever created the changes
        if self.source_file:
            with open(self.source_file, 'r') as myfile:
                self.msg = "{msg}\n\nCreated by this script:\n*****\n{source}\n*****\n".format(
                    msg=self.msg, source=myfile.read()
                )

        if self.config_file:
            with open(self.config_file, 'r') as myfile:
                self.msg = "{msg}\n\nCreated by Uncrustify with config file:\n*****\n{source}\n*****\n".format(
                    msg=self.msg, source=myfile.read()
                )

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

class Patch(object):
    def __init__(self, files, hunks=None, size=None, test_size=True, split=False):
        """[summary]

        Parameters
        ----------
        object : [type]
            [description]
        files : [type]
            [description]
        hunks : [type], optional
            [description] (the default is None, which [default_description])
        size : [type], optional
            [description] (the default is None, which [default_description])
        test_size : bool, optional
            [description] (the default is True, which [default_description])
        split : bool, optional
            [description] (the default is False, which [default_description])

        """

        self.files = []
        self.hunks = 0
        self.size = 0
        self.split = split

        self.add(files, hunks, size, test_size)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "%r" % (self.__dict__)

    def add(self, file, hunks=None, size=None, test_size=True):
        """ Add a file into the patch.
            Allowed usage:
                Patch.add(patch_object) # in this case, the Patch object passed can contain only one file
                Patch.add(filename, hunks, size) # filename is a string

            A PatchTooBig exception is raised if the patchsize would exceed the max size.
        """
        if isinstance(file, Patch):
            # we ignore hunks and size, should be None
            assert(hunks is None and size is None)
            # and the Patch can contain only one file
            assert(len(file.files) == 1)
            hunks = file.hunks
            size = file.size
            file = file.files[0]
        else:
            assert(hunks is not None and size is not None)

        if test_size and self.size + size > MAX_PATCH_SIZE:
            raise PatchTooBig()

        self.files.append(file)
        self.hunks += hunks
        self.size += size

class PatchTooBig(Exception):
    pass

class XfsdumpRepo(object):
    """ Repository wrapper """


    def __init__(self, repo_path, scripts_path):
        self.path = repo_path
        self.scripts_path = scripts_path
        self.repo = Repo(self.path)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def run(self, command, return_output=False, shell=False):
        if return_output:
            return subprocess.check_output(command, shell=shell)
        else:
            return subprocess.check_call(command, shell=shell)

    def get_diff_raw(self, paths=None, staging=False):
        """ Get the raw output, like from git diff. Paths can be a string or list of strings. """
        if paths is not None and not isinstance(paths, (tuple, list)):
            paths = [paths]

        if staging:
            return self.repo.git.diff(paths, cached=True)
        return self.repo.git.diff(paths)

    def diff_size(self, paths=None, staging=False):
        """ Get size of a diff. Paths can be a string or list of strings. """
        diff = self.get_diff_raw(paths, staging)
        return len(diff)

    def diff_hunks(self, paths=None):
        """ Get the number of hunks in diff """
        diff = self.get_diff_raw(paths)
        # the standard format is "@@ -197,7 +197,7 @@ ...". Count them all and divide by two is probably faster than regexes to grab only the first ones.
        return diff.count('@@')/2

    def diff_files(self):
        """ Get the files that are changed in current working tree and the size of their diffs.
            Return a list of Patch objects. """
        files = dict()
        # get the git diff stat without the last summary line
        lines = self.repo.git.diff('--stat', '--no-color').splitlines()[:-1]
        for line in lines:
            match = re.match(r' (.*\S) *\| *([0-9]+) ', line)
            fname = match[1]
            #changes = int(match[2])
            diff = self.get_diff_raw(fname)

            files[fname] = Patch(
                files=[fname],
                size=len(diff),
                hunks=diff.count('@@')/2,
                test_size=False)

        return files


    def _make_one_patch(self, patchinfo: PatchInfo):
        self.repo.git.add('-u')
        self.repo.git.commit('--signoff', '-m', patchinfo.msg)

    def _make_many_patches(self, patchinfo: PatchInfo):
        files = self.diff_files()
        patchset = [Patch([], 0, 0)]
        total_patches = 1 # we need this because some files will be split to more patches

        for name, file in files.items():
            if file.size < MAX_PATCH_SIZE:
                # the file is smaller than tha max size, so we can try to add it to other files
                try:
                    patchset[-1].add(file)
                except PatchTooBig:
                    patchset.append(Patch(file))
                    total_patches += 1
            else:
                # create a new patch first for this file we will split
                patchset.append(Patch(file, test_size=False, split=True))
                # and then for anything that will follow - we don't want to mix
                # these even if it would be small enough
                patchset.append(Patch([], 0, 0))
                total_patches += 3 # 2 for the split one and 1 for the empty one

        print("Total patches: {} (Patch objects: {})".format(total_patches, len(patchset)))

        this_patch = 1
        for patch in patchset:
            # if we split, we must have only one file
            assert(not(len(patch.files) > 1 and patch.split))

            if patch.split:
                print("Patch split in half ({a}/{total}, {b}/{total})".format(a=this_patch, b=this_patch+1, total=total_patches))
                self._patch_split_commit(patch, this_patch, total_patches, patchinfo)
                this_patch += 2
            else:
                print("Patch add ({}/{})".format(this_patch, total_patches))
                self._add_and_commit(patch.files, this_patch, total_patches, patchinfo)
                this_patch += 1

    def _patch_split_commit(self, patch: Patch, this_patch: int, total_patches: int, patchinfo: PatchInfo):
        assert(patch.split)
        assert(len(patch.files) == 1)

        targetfile = patch.files[0][0]

        split_at = int(patch.hunks / 2)
        if split_at > MAX_PATCH_SIZE:
            raise PatchTooBig("Patch is too big even after splitting. This needs to be imlemented...")
        # build a list of many "y" confirmations with one q for quit at the end
        confirmations = '{}q\n'.format('y\n'*split_at).encode()
        print("  splitting at {} (hunks {}, file: {})".format(split_at, patch.hunks, targetfile))
        proc = subprocess.Popen(['git', 'add', '-p', targetfile],
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout_data = proc.communicate(input=confirmations)[0]
        print("  cached tree:\t" + str(subprocess.check_output(['git', 'diff', '--cached', '--stat'])).replace('\\n', '\n').splitlines()[1])
        print("  working tree:\t" + str(subprocess.check_output(['git', 'diff', '--stat', targetfile])).replace('\\n', '\n').splitlines()[1])
        self._commit(this_patch, total_patches, patchinfo)
        this_patch += 1

        # now add the rest of the file
        self._add_and_commit(patch.files, this_patch, total_patches, patchinfo)

    def _add_and_commit(self, files: list, this_patch: int, total_patches: int, patchinfo: PatchInfo):
        self.repo.git.add('-u', files)
        self._commit(this_patch, total_patches, patchinfo)

    def _commit(self, this_patch: int, total_patches: int, patchinfo: PatchInfo):
        msg = patchinfo.msg.splitlines()
        msg[0] = msg[0].replace('xfsdump: ', 'xfsdump: ({}/{}) '.format(
            this_patch, total_patches
        ))
        msg.append('')
        msg.append('Signed-off-by: {}'.format(SIGNOFF))
        self.repo.index.commit('\n'.join(msg),  )


    def make_patch(self, item: dict):
        patch = PatchInfo(self.scripts_path, item)

        print("Running '{}'".format(patch.script))
        self.long_lines_before = self.count_long_lines()
        self.run([patch.script])
        self.long_lines_after = self.count_long_lines()

        # get diff size and decide if it needs to split the patch
        size = self.diff_size()

        if size < MAX_PATCH_SIZE:
            print("Creating only one patch.")
            self._make_one_patch(patch)

        else:
            print("Producing multiple patches.")
            self._make_many_patches(patch)

    def code_checks(self):
        """ Run a set of checks and reports to verify some basic sanity """

        if self.long_lines_after != self.long_lines_before:
            print("The number of long lines (>79) changed from {} to {}".format(
                self.long_lines_before, self.long_lines_after
            ))

        #
    def count_long_lines(self):
        """ get lines that are over 79 chars, in the format from grep

        Returns
        -------
        list(str)
            Lines over 79 characters
        """
        return int(self.run('find . -name "*.c" -o -name "*.h" | xargs grep -n ".\{80\}" | wc -l',
            return_output=True, shell=True
        ))



if __name__ == "__main__":
    repo = XfsdumpRepo(os.path.join(DIR_PATH, '..'), DIR_PATH)
    os.chdir(repo.path)

    for patch in PATCHES:
        repo.make_patch(patch)
    repo.code_checks()
