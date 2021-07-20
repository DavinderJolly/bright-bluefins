# Shell Commands

The shell supports a wide range of commands. These commands are very similar to the original DOS. The list of commands are given below:

1. [ECHO](#echo)
1. [EDIT](#edit)
1. [IMGVIEW](#imgview)
1. [CD](#cd)
1. [CWD](#cwd)
1. [DIR](#dir)
1. [TREE](#tree)
1. [DELTREE](#deltree)
1. [DEL](#del)
1. [TYPE](#type)
1. [MOVE](#move)
1. [PING](#ping)
1. [PATH](#path)
1. [RD](#rd)
1. [REN](#ren)
1. [DATE](#date)
1. [TIME](#time)
1. [FIND](#find)
1. [CLS](#cls)
1. [EXIT](#exit)

---

<br><br>

### ECHO

Reapeats the message passed to command.

```sh
ECHO Message
```

<br>

### EDIT

Opens the file given to the command in the Notepad text editor.

```sh
EDIT filename.txt
```

<br>

### IMGVIEW

Opens the image given in the Photos image viewer in ANSI mode.

```sh
IMGVIEW image.png
```

<br>

### CD

Changes the current directory of the shell to the specified path.

```sh
CD Path
```

<br>

### CWD

Returns the current working directory of the shell.

```sh
CWD
```

<br>

### Dir

Returns the names of all files and folders in the given directory, if no path is given it defaults to the current directory.

```sh
DIR Path
```

<br>

### TREE

Shows the files and subdirectories of the given directory as a tree structure, if no path is given it defaults to the current directory.

```sh
TREE Path
```

<br>

### DELTREE

Deletes a directory and all the subdirectories and files in it, if no path is given it defaults to the current directory.

```sh
DELTREE Path
```

<br>

### DEL

Deletes one or more files.

```sh
DEL Path1 Path2 Path3 ...
```

<br>

### TYPE

Displays the contents of a file to the screen.

```sh
TYPE Path
```

<br>

### MOVE

Moves a file from one directory to another directory.

```sh
MOVE Old_path New_path
```

<br>

### PING

Tests if an IP address or a domain name is active or not, also provides some information about it.

```sh
PING IP_address/domain_name
```

<br>

### PATH

Prints all the executable files (.exe) in the given path.

```sh
PATH Path
```

<br>

### RD

**Alias: RMDIR**

Removes an empty directory, shows error message if not empty.

```sh
RD Path
```

<br>

### REN

Renames a file or directory to the specified name.

```sh
REN Path_to_file New_name
```

<br>

### DATE

Shows the system date according to given unix date time format, defaults to %d-%m-%Y format if none provided.

```sh
DATE Format_string
```

<br>

### TIME

Shows the system time according to given unix date time format, defaults to %H:%M:%S format if none provided.

```sh
TIME Format_string
```

<br>

### FIND

Searchs for text within a file.

```sh
FIND Path
```

<br>

### CLS

**Alias: CLEAR**

Clears the whole screen.

```sh
CLS
```

<bv>

### EXIT

**Alias: QUIT**

Exits the shell.

```sh
EXIT
```
