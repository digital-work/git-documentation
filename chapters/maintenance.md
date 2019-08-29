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

\subsection{Recover accidentally deleted files}
We can restore accidentally deleted files as described \href{https://stackoverflow.com/questions/11956710/git-recover-deleted-file-where-no-commit-was-made-after-the-delete}{here}:
\begin{verbatim}
git checkout path/to/file-I-want-to-bring-back.sth
\end{verbatim}

\section{Recurring Bugs}

In some cases, the following error might occur when trying to push/pull (a) commit(s):
\begin{verbatim}
LF will be replaced by CRLF.    
\end{verbatim}
A solution is described \href{https://stackoverflow.com/questions/5834014/lf-will-be-replaced-by-crlf-in-git-what-is-that-and-is-it-important}{here}:
\begin{verbatim}
git config core.autocrlf true
\end{verbatim}

