#!/bin/bash

_v_complete()
{
    local cur="${COMP_WORDS[COMP_CWORD]}"

    if [[ ${cur} == -* ]]; then
        COMPREPLY=( $(compgen -W "--complete" -- ${cur}) )
        return 0
    fi

    local IFS=$'\n'
    local suggestions=$(python3 -m shellutils.v "${cur}" --complete)
    local modified_suggestions=""
    for s in ${suggestions}; do
        modified_suggestions+=$(basename "${s}")$'\n'
    done
    COMPREPLY=( $(compgen -W "${modified_suggestions}" -- ${cur}) )
}

complete -F _v_complete v
