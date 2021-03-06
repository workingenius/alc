"python <<EOF
"print('alc worked with python')
"EOF

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)

from alc import main as alc_main
#help(vim)
EOF

function! Alc(...)
    python alc_main(*vim.eval('a:000'))
endfunction
command! -nargs=* Alc call Alc(<f-args>)

