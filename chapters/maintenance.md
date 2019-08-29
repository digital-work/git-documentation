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

\subsection(Removing files that are too big for the repository)

When adding media files like mp3 the repository might increase in size drastically since on each new upload the current file is stored in the repository. At some point we MIGHT have to remove some of the files, and just calling $git rm <file url>$ might not do the trick because the repository still contains the state of the previously committed and tracked media files. In that case we can follow the instructions described 
\href{https://freek.dev/879-how-to-remove-a-big-file-wrongly-committed-to-a-git-repo}{here}:

\begin{verbatim}
git filter-branch --tree-filter 'rm path/to/your/bigfile' HEAD
git push origin master --force
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

