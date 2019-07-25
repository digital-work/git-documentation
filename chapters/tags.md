Tags can be added to highlight specific releases. The can represent milestones, versions, etc.

\section{General commands}

Make a new tag:
\begin{enumerate}[noitemsep]
    \item
    \begin{verbatim}
git tag <name>
git tag <name> <short-sha>
    \end{verbatim}
    \item
    \begin{verbatim}
git push origin <name>
git push origin --tags
    \end{verbatim}
\end{enumerate}

Delete an existing tag:
\begin{enumerate}[noitemsep]
    \item 
    \begin{verbatim}
git tag -d <name>
    \end{verbatim}
    \item
    \begin{verbatim}
git push origin :refs/tags/<name>
    \end{verbatim}
\end{enumerate}

Rename \href{https://stackoverflow.com/questions/1028649/how-do-you-rename-a-git-tag}{an existing tag}:
\begin{enumerate}[noitemsep]
    \item 
    \begin{verbatim}
git tag <new-name> <old-name>
    \end{verbatim}
    \item
    \begin{verbatim}
git tag -d <old-name>
    \end{verbatim}
    \item
    \begin{verbatim}
git push origin :refs/tags/<old-name>
    \end{verbatim}
    \item
    \begin{verbatim}
git push --tags
    \end{verbatim}
\end{enumerate}

Remind all co-workers to run the following command:
\begin{verbatim}
git pull --prune --tags
\end{verbatim}