Branches can be helpful when we have a main project, from which we derive minor side projects. A branch can stand by itself or merged again with the main branch ($master$).

\section{General commands}

Make new branch:
\begin{verbatim}
git branch <branch-name>
\end{verbatim}

Delete an existing branch:
\begin{verbatim}
git branch -d <branch-name>
\end{verbatim}

Rename \href{https://multiplestates.wordpress.com/2015/02/05/rename-a-local-and-remote-branch-in-git/}{an existing branch}:
\begin{enumerate}[noitemsep]
    \item Rename the branch in your local repository:
    \begin{verbatim}
git branch -m <old-name> <new-name>
    \end{verbatim}
    \item Push the new branch to remote:
    \begin{verbatim}
git push origin :<old-name> <new-name>
    \end{verbatim}
    \item 
    \begin{verbatim}
git push origin -u <new-name>
    \end{verbatim}
\end{enumerate}

In some cases we want to merge to branches into each other, e.g. branch (b) into (a), as explained \href{https://superuser.com/questions/340471/how-can-i-merge-two-branches-without-losing-any-files}{here}:
\begin{enumerate}
  \item Switch to branch (a):
  \begin{verbatim}
git checkout a
  \end{verbatim}
  \item Merge branch (b) into (a):
  \begin{verbatim}
git merge b
  \end{verbatim}
  \item Commit your changes:
  \begin{verbatim}
git commit -a
  \end{verbatim}
\end{enumerate}

\section{Recurring bugs}

"Git push master fatal: You are not currently on a branch"
Explanation \href{https://stackoverflow.com/questions/30471557/git-push-master-fatal-you-are-not-currently-on-a-branch/30471627}{here} or \href{https://stackoverflow.com/questions/4735556/git-not-currently-on-any-branch-is-there-an-easy-way-to-get-back-on-a-branch}{here}.
General idea:
\begin{verbatim}
git branch <tmp-branch>
git checkout master
git merge <tmp-branch>
git push origin master
\end{verbatim}

The local branch is not tracking the remote branch anymore. When you use gitx or gitk to browse the repository, you will notice that the different branches have a label for the local and the corresponding remote branch. If a branch is not tracking its remote branch anymore, you will only see the local label. In this case, you will have to set the upstream tracking again, using the following command:
\begin{verbatim}
git branch --set-upstream-to=origins/pupsi pupsi
\end{verbatim}