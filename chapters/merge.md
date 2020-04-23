In some cases, it is very helpful to see differences between specific commits and/or the current version of the repository.
Likewise, it is very normal that you will encounter some conflicts while working on a projects with multiple contributors. Don't worry and follow these steps.

\section{Tools}
When comparing two states in git, we can use the default commands to get a patch of the main changes:
\begin{verbatim}
git diff
git diff <sha-1> <sha-2>
\end{verbatim}
If you have add the changes already you will have to call the following command:
\begin{verbatim}
git diff HEAD
\end{verbatim}
This is very helpful, if we want to send a patch to a co-worker, for example.

However, this might be very clunky in some settings because we do not get a smoot visual representation of the changes. Thus, we might use common diff tools to visualize changes like TortoiseGit (Win), FileMerge (Mac) by using the following commands:
\begin{verbatim}
git difftool
git difftool <sha-1> <sha-2>
\end{verbatim}
If you have add the changes already you will have to call the following command:
\begin{verbatim}
git difftool HEAD
git difftool --staged
\end{verbatim}

\subsection{FileMerge on Mac}
If you are doing this for the first time, you might have to set up an appropritate diff tool.
On Mac, you might want to use FileMerge that is already included on most MacOs's following \href{https://stackoverflow.com/questions/21486481/is-it-possible-to-view-git-diffs-using-a-gui-side-by-side-tool-on-mac}{these easy steps}:
\begin{enumerate}[noitemsep]
    \item Define FileMerge for the mergetool:
    \begin{verbatim}
git config --global merge.tool opendiff
    \end{verbatim}
    \item Define FileMerge for the difftool:
    \begin{verbatim}
git config --global diff.tool opendiff	
    \end{verbatim}		
    \item Suppress prompt at every comparison:
    \begin{verbatim}
git config --global diff.tool opendiff
    \end{verbatim}	
\end{enumerate}

\subsection{TortoiseGit on PC}
On PC, you might want use Tortoise following \href{https://gist.github.com/ellisda/25cdd92129c5b44406ab}{these easy steps}:
\begin{enumerate}[noitemsep]
  \item Download and install \href{https://tortoisegit.org/download}{TortoiseGit}.
  \item Locate the global .gitconfig file in your home folder.
  \item Add the following lines to the config file:
  \begin{verbatim}
[diff]
  tool = TortoiseGitDiff	
[difftool]
  prompt = false
[difftool "TortoiseGitDiff"]
  cmd = \"C:/Program Files/Path/To/TortoiseGitMerge.exe\"
 -mine:"$REMOTE" -base:"$LOCAL" 

[merge]
  tool = TortoiseGitMerge	
[mergetool "TortoiseGitMerge"]
  cmd = \"C:/Program Files/Path/To/TortoiseGitMerge.exe\"
 -base:"$BASE" -mine:"$LOCAL" -theirs:"$REMOTE" 
 -merged:"$MERGED"
  \end{verbatim}
  You might have to adjust the executable path to match the actual location of the program.
\end{enumerate}

\section{General approach}
You will most likely encounter a merge conflict, after calling git pull from the command line. You will recognize a merge conflict by a message similar to this one:
\begin{verbatim}
error: Your local changes to the following files would be 
       overwritten by merge:
       main.tex
Please commit your changes or stash them before you merge. 
Aborting
\end{verbatim}
We can solve it by the following simple steps:
\begin{enumerate}[noitemsep]
    \item Save the local changes:
    \begin{verbatim}
git stash
    \end{verbatim}
    \item  Download the latest changes from the remote repository:
    \begin{verbatim}
git pull
    \end{verbatim}
    \item Reload changes on the local copy:
    \begin{verbatim}
git stash pop
    \end{verbatim}
    \item Resolve conflict by calling the mergetool
    \begin{verbatim}
git mergetool
    \end{verbatim}
    \item Commit and push your changes to the repository.
    \item Call the following command to get rid of all the intermediary .orig-files. (If you want to delete folders recursively you can add the -d option):
    \begin{verbatim}
git clean -f
git clean -fd
    \end{verbatim}
\end{enumerate}

If you have some merge conflicts although you did not really have any local changes (e.g. merging wrong branches locally and remotely), you can abort merging with the following command:
\begin{verbatim}
git merge --abort
\end{verbatim}

\section{How to use a pull request on Github}

\begin{enumerate}[noitemsep]
  \item Update from latest comit on master
  \begin{verbatim}
git pull origin master
  \end{verbatim}
  \item Make a new branch and push it to Github
  \begin{verbatim}
git checkout -b pull-request-demo
git push origin pull-request-demo
  \end{verbatim}
  \item Do some changes and commit them.
  \item Go to Github {\textgreater} Pull requests {\textgreater} New pull request. Choose the branch you want to merge into master under the compare drop-down menue. Add title and description, and press "Create pull request".
  \item Merge pull request if you are content with the changes. If it cannot be done automatically, we have to do it locally which requires some more effort.
\end{enumerate}