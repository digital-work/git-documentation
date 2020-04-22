This chapter contains some extra gimmicks for \LaTeX documents. It is going to stay in this Git-documentation until we find a better location.

\section{How to create hard links / symlinks for the build folder}

The goal is to create a build folder that is added to .gitignore, in which we compile the PDF document of the  \LaTeX project. The build folder is no ordinary folder but a hard link (win) or symlink (mac) that links to another folder in which we gather the PDFs of multiple projects. In that way we can publish PDFs of otherwise private \LaTeX project.

\subsection{Hard links on Windows}

Create a directory junction as described \href{https://superuser.com/questions/67870/what-is-the-difference-between-ntfs-hard-links-and-directory-junctions}{here}:
\begin{verbatim}
MKLINK /J Link Original
\end{verbatim}

\subsection{Symlinks on Mac}

Create a symmlink as described \href{https://www.howtogeek.com/297721/how-to-create-and-use-symbolic-links-aka-symlinks-on-a-mac/}{here}:
\begin{verbatim}
ln -s original link
\end{verbatim}
OBS: Use absolute url on Mac!

\section{Conditionals}

We can define variables in the preamble and then check if the variable has been set anywhere inside the document:

\begin{verbatim}
\def\var1{1} % You can set the variable to true (1) or false (0)

\begin{document}

\if\var1
... % Do something if var1 has been set to 1.
\else
... % Do something else if var has been set to 0.
\fi

\end{document}
\end{verbatim}