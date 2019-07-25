\section{General settings}

\subsection{Changing the user and their options}

On your PC/Mac:
\begin{verbatim}
git config --global user.email "email@example.com"
got config --global user.name "John Doe"
\end{verbatim}
You can check that everything has been set correctly by typing
\begin{verbatim}
got config --global user.name
\end{verbatim}

On Overleaf:
Go to Account{\textgreater}Account Settings and add the email address. Confirm the address by opening the email that you received in your mailbox.

On GitHub:
Go to Settings\textgreater  Emails and add the email address. Confirm the address by opening the email that you received in your mailbox. Choose a primary email address(, which is the one that is going to show up in your commits). OBS: Make sure that you did not mark the "Keep my email address private"-option. The name (that will actually show up in your commits) can be changed in your GitHub profile.

\subsection{.gitignore}
In many cases, you will have files in your local repository that you do not want to have committed because they are not useful, they are experimental or too big. In those cases you might want to create a .gitignore file in your folder and commit it to the repository. Git will know automatically that all the fields that are listed in the .gitignore file are not supposed to be tracked for changes.

\section{Cross-platform text documents}
In case you want to version control a text document with GitHub, follow this tutorial.

\subsection{Starting in Overleaf}
Start in Overleaf, then push it to GitHub, and download from GitHub to your computer
($Overleaf \rightarrow GitHub \rightarrow PC/Mac$).

\begin{enumerate}[noitemsep]
    \item Make a new project in Overleaf.
    \item Choose the GitHub option in the menu and choose "Create a GitHub repository". Choose a name and add a description if wanted.
    \item Choose the GitHub option in the menu and choose "Push Overleaf changes to GitHub".
    \item Switch to your GitHub account and check if everything showed up correctly.
    \item Open a terminal on your computer, create and navigate to the folder in which you want to clone the repository.
    \item Obtain the url to the repository on the GitHub page under "Clone or download" and write the following lines in the terminal: 
    \begin{verbatim}
git clone <path/to/github/repository> <folder>
    \end{verbatim}
    (If no folder is specified, it will take the repository name as default name.)
\end{enumerate}

\subsection{Starting on GitHub}
Start on GitHub, then pull it from Overleaf and your PC/Mac
($Overleaf \leftarrow GitHub \rightarrow PC/Mac$).

\begin{enumerate}[noitemsep]
    \item Make a new repository on GitHub.
    \item Copy the repository address on GitHub.
    \item On your PC/Mac, navigate to the folder where you want to have the repository (or its parent folder).
    \item Clone the GitHub repository into a new folder with the name of the git repository or into a specified folder:
    \begin{verbatim}
git clone <url-to-repository>
git clone <url-to-repository> <path/name/of/folder>
    \end{verbatim}
    \item Get all branches and tags:
    \begin{verbatim}
#git fetch origin
    \end{verbatim}
    \item Check that all branches have been fetched:
    \begin{verbatim}
#git branch -a
    \end{verbatim}
    \item Go to Overleaf and chose "Import from GitHub" under "New Project".
    \item Choose the repository you want to import.
\end{enumerate}

\subsection{Starting on your PC/Mac}
Start on your PC/Mac, then push to GitHub, and pull it from GitHub from Overleaf
($PC/Mac \rightarrow GitHub \rightarrow Overleaf$).

\begin{enumerate}[noitemsep]
    \item Create a new project on you PC/Mac:
    \begin{verbatim}
git init
    \end{verbatim}
    \item Add files, make changes, commit to local repository.
    \item Create a new and empty repository on GitHub. (No README file!)
    \item Copy repository address.
    \item Navigate to the git repository folder on your computer. 
    \item Remove existing origins from the repository:
    \begin{verbatim}
git remote rm origin
    \end{verbatim}
    \item Add the GitHub repository as a new origin to your local repository on your PC/Mac:
    \begin{verbatim}
git remote add origin <url-to-repository>
    \end{verbatim}
    \item Push all changes from your PC/Mac to GitHub including all branches and flags:
    \begin{verbatim}
git push --all origin
git push --tags origin
    \end{verbatim}
    \item Go to Overleaf and chose "Import from GitHub" under "New Project".
    \item Choose the repository you want to import.
\end{enumerate}

If you want to migrate a repository from an existing remote to a new remote, you can use the following commands (based on \href{https://gist.github.com/niksumeiko/8972566}{the following tutorial}):
Move repository from Cloudforge to Github.
\begin{enumerate}[noitemsep]
    \item Open a terminal and go to the folder the repository is located in.
    \item Add a new remote origin:
    \begin{verbatim}
git remote add new-origin <path-to-new-repository>
    \end{verbatim}
    \item Push all branches and tags to the new repository:
    \begin{verbatim}
git push --all new-origin
git push --tags new-origin
    \end{verbatim}
    \item Show existing remotes
    \begin{verbatim}
git remote -v
    \end{verbatim}
    \item Remove old remote repository:
    \begin{verbatim}
git remote rm origin
    \end{verbatim} 
    \item Rename new remote repository to origin
    \begin{verbatim}
git remote rename new-origin origin
    \end{verbatim}
\end{enumerate}