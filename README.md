xfsdump style cleaning scripts
==============================

A bunch of scripts intended for semi-automated style enforcement in
xfsdump/xfsprogs. It's a mix of bash, awk and Uncrustify scripts. The goal
initially was to have it fully automated, so `format-all.py` have been created,
but as it turned out, some changes (at least when done by "dumb" tools like
awk) require manual fixes, the python script is useful mainly for automated
splitting of large patch into multiple smaller ones that can pass through
mailing lists.

Current status (as of 12th June 2019): patches for scripts 1-5 has been merged.
Scripts 6+ probably needs some polishing. Scripts 1-9 are based on awk and
regular expressions, scripts 10-14 are using Uncrustify.

The reason for using a semantic tool like Uncrustify only for part of the
changes is the inability to enforce only some basic rules - in other words,
Uncrustify wasn't able to to produce a change like "fix spaces around braces,
but do not change anything else," but always reformat many other things which
would cause terribly big patches (effectively rewriting the whole xfsdump).

So, Uncrustify can be used only after the most glaring issues were fixed in
some other way.

Usage
-----
1) Run a specific .sh script, that will apply changes but won't create commit.
2) Review the changes, modify as needed
3) Commit and run the next script

However, if you see that the amount of changes produced in step 1 is too big
(the resulting patch has more than some 150kB), mailing lists will refuse to
sent such a large email and the patch has to be split.

If it is not easy to do it by hand (some files in one patch, other files in
another patch), if a single file results in a patch bigger than accepted, then
the `format-all.py` script should be able to help you, as it can add individual
hunks and split such file. Just uncomment relevant lines in the first part of
the script (which define the shell script used and commit message) and it
will apply the script and commit the changes.

This doesn't play well with manual changes, but so far, the only changes where
the automated splitting was necessary were also easy to fully automate.




