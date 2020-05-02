Before committing new code, always make sure to update your local version from origin first!

\section{Cross-platform text documents}

\subsection{From Overleaf}

\begin{enumerate}[noitemsep]
    \item Make your changes and save with Ctrl + s / Cmd + s.
    \item Update your Overleaf repository from origin by choosing the GitHub option in the menu and choosing "Pull GitHub changes into Overleaf".
    \item Choose the GitHub option in the menu and choose "Push Overleaf changes to GitHub". Write a comment and commit.
\end{enumerate}

\subsection{From your PC/Mac}
All commands can be done from the command line after navigating to the folder containing the git repository:
\begin{verbatim}
cd <path\to\github\repository>
\end{verbatim}

\begin{enumerate}[noitemsep]
    \item Make your changes and save them.
    \item Update your local repository from origin:
    \begin{verbatim}
git pull   
    \end{verbatim}
    \item Stage the file(s) that have changes.
    \begin{verbatim}
git add <name-of-file>
    \end{verbatim}
    \item Commit the changes to the local repository with a change comment:
    \begin{verbatim}
git commit -m "Some useful and readable comment."
    \end{verbatim}
    \item Push the changes to origin.
    \begin{verbatim}
git push
    \end{verbatim}
\end{enumerate}

\section{General commands}

\subsection{Renaming version-controlled files}
If we want to change the name of a version-controlled document whil still preserving the history of its content, we can use the following command:
\begin{verbatim}
git mv old_filename new_filename
\end{verbatim}
Then, commit and push the changes as always.

\subsection{Moving version-controlled files}
If we want to move a version-controlled document whil still preserving the history of its content, we can use the following command:
\begin{verbatim}
git mv filename dir
\end{verbatim}
Then, commit and push the changes as always.

\subsection{Removing/Deleting files}
Remove a file from the repository by using:
\begin{verbatim}
git rm <file/folder>
\end{verbatim}

If you want to keep it in the file system, while removing it from the repository, you can use:
\begin{verbatim}
git rm --cached <file/folder>
\end{verbatim}

If you want to delete a file recursively, you can use:
\begin{verbatim}
git rm -r <folder>
\end{verbatim}

If you want to see what would be deleted use:
\begin{verbatim}
-n
--dry-run 
Don’t actually remove any file(s). 
Instead, just show if they exist in the index 
and would otherwise be removed by the command.
\end{verbatim}

\subsection{Bash commands on Mac}
Move multiple files as described \href{https://stackoverflow.com/questions/2212857/how-do-you-move-multiple-files-in-git}{here}:
\begin{verbatim}
for FILE in folder/*.ext; do git mv $FILE new-folder/; done    
\end{verbatim}

Remove prefix from filename as described \href{https://stackoverflow.com/questions/10535985/how-to-remove-filename-prefix-with-a-posix-shell}{here}:
\begin{verbatim}
for FILE in folder/*; do git mv "$FILE" "${FILE#prefix}"
\end{verbatim}

\subsection{Bash commands in Windows}
You can use the following bash commands as described \href{https://stackoverflow.com/questions/138497/iterate-all-files-in-a-directory-using-a-for-loop}{here}:
\begin{verbatim}
for /r %i in (*) do echo %i
\end{verbatim}
In bash scripts, we have to double the % signs:
\begin{verbatim}
for /r %%i in (*) do echo %%i
\end{verbatim}

\subsection{Removing files that are too big for the repository}

When adding media files like mp3 the repository might increase in size drastically since on each new upload the current file is stored in the repository. At some point we MIGHT have to remove some of the files, and just calling $git rm <file url>$ might not do the trick because the repository still contains the state of the previously committed and tracked media files. In that case we can follow the instructions described 
\href{https://freek.dev/879-how-to-remove-a-big-file-wrongly-committed-to-a-git-repo}{here}:

\begin{verbatim}
git filter-branch --tree-filter 'rm path/to/your/bigfile' HEAD
git push origin master --force
\end{verbatim}

If you encounter the following error
\begin{verbatim}
A previous backup already exists in refs/original/
\end{verbatim}

You might have to call the command with the -f option as described \href{https://stackoverflow.com/questions/6403601/purging-file-from-git-repo-failed-unable-to-create-new-backup}{here}:
\begin{verbatim}
git filter-branch -f --tree-filter 'rm -rf path/to/your/bigfile' HEAD
\end{verbatim}

\subsection{Recover accidentally deleted files}
We can restore accidentally deleted files as described \href{https://stackoverflow.com/questions/11956710/git-recover-deleted-file-where-no-commit-was-made-after-the-delete}{here}:
\begin{verbatim}
git checkout path/to/file-I-want-to-bring-back.sth
\end{verbatim}

\subsection{Show full history of moved files}
You can see the complete log as described \href{https://gist.github.com/ajaegers/2a8d8cbf51e49bcb17d5}{here}:
\begin{verbatim}
git log --follow file
\end{verbatim}

\subsection{Creating new repository from folder of an existing repository}
We start with this:
\begin{verbatim}
XYZ/
  .git/
  A/
  B/
  C/
\end{verbatim}
but want to end up with this:
\begin{verbatim}
XYZ/
  .git/
  A/
  B/
C/
  .git/
  C/
\end{verbatim}

Making new repository from a folder in an existing GIT repository following \href{https://stackoverflow.com/questions/359424/detach-move-subdirectory-into-separate-git-repository/6295550}{The Easy Way}:
\begin{enumerate}[noitemsep]
  \item Prepare the old repository:
  \begin{verbatim}
pushd <old-repo>
git subtree split -P <folder> -b <new-branch>
popd
  \end{verbatim}
  \item Create the new repository:
  \begin{verbatim}
mkdir <new-repo>
pushd <new-repo>
git init
git pull <path/to/old-repo> <new-branch>
  \end{verbatim}
  \item Link the new repository to Github:
  \begin{verbatim}
git remote add origin ...
git push origin -u master
  \end{verbatim}
  \item Cleanup if desired
  \begin{verbatim}
popd
pushd <old-repo>
git rm -rf <folder>
git commit
  \end{verbatim}
\end{enumerate}

\section{Recurring Bugs}

\subsection{CRLF bug}

In some cases, the following error might occur when trying to push/pull (a) commit(s):
\begin{verbatim}
LF will be replaced by CRLF.    
\end{verbatim}
A solution is described \href{https://stackoverflow.com/questions/5834014/lf-will-be-replaced-by-crlf-in-git-what-is-that-and-is-it-important}{here}:
\begin{verbatim}
git config core.autocrlf true
\end{verbatim}

\subsection{Ghost files in untracked files list}

It could happen that the untracked files list shows files that do not really exist on the file system:
\begin{verbatim}
git status
On branch master
Your branch is up to date with 'origin/master'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        file1.jpg
        file2.jpg
\end{verbatim}

This can be solved by \href{https://stackoverflow.com/questions/11525358/git-untracked-files-list-is-wrong}{this solution}:
\begin{verbatim}
git clean -f
\end{verbatim}