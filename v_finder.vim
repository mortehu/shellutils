" v_finder.vim - Plugin to open a file with the given name in any subdirectory

function! FindFileAndEdit(filename)
    " Call the Python script to find the file
    let l:filepath = system("python3 -m shellutils.v --full --complete " . a:filename)
    let l:filepath = substitute(l:filepath, '\n$', '', '')

    " Check if the file was found
    if empty(l:filepath)
        echoerr "No file found with the specified name."
    elseif l:filepath =~ "Multiple files found"
        echoerr l:filepath
    else
        " Edit the found file
        execute "e " . l:filepath
    endif
endfunction

function! FilenameComplete(A, L, P)
    let l:files = system("python3 -m shellutils.v --complete " . a:A)
    let l:files_list = split(l:files, '\n')
    return l:files_list
endfunction

map ,v :call FindFileAndEdit(input("Filename: ", "", "customlist,FilenameComplete"))<CR>
