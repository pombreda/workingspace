
# in /home/jinpeng/svn/brainvisa/soma/soma-workflow
grep -r --exclude-dir="*.svn" --exclude-dir="./branches*" --exclude-dir="./tags/*"  "soma.workflow" . 

# in /home/jinpeng/svn/brainvisa
grep -r --exclude-dir="*.svn" --exclude-dir="./soma/soma-workflow" --exclude-dir="./axon/branches" --exclude-dir="./axon/tags" "soma.workflow" .

svn mv workflow ../soma_workflow

