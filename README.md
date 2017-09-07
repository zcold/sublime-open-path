# sublime-open-path

## Usage

1. Select a string, open it as a file/folder path(s)
2. Open line at cursor position as file/folder path(s)

## Environment varible conflect resolving is supported

Example:

In project `foo`: $MYPROJ = /projects/myprojects/foo

    In `/projects/myprojects/foo/src/foo_files.txt`:
    
        `$BARPROJ/src/bar_files.txt` in `foo_files.txt`
        
        open path `$BARPROJ/src/bar_files.txt` = open path `/projects/myprojects/bar/src/bar_files.txt`
        
    In `/projects/myprojects/bar/src/bar_files.txt`
    
        `$MYPROJ/src/one_bar_file.txt` in `bar_files.txt`
        
        since $MYPROJ = /projects/myprojects/foo
        
        `$MYPROJ/src/one_bar_file.txt` = `/projects/myprojects/foo/src/one_bar_file.txt`
        
    Cannot find `/projects/myprojects/foo/src/one_bar_file.txt`
    
    since it should be `/projects/myprojects/bar/src/one_bar_file.txt`

What we do is to replace $MYPROJ in any files that are not in current project folder to absolute file path.

Empty string (`project_path_var=""`) means do not modify file path.

