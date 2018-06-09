:: Create git archive (so untracked files such as __pycache__ are ignored)
cd ..
git archive -o utils/package.zip HEAD ^
setup.py ^
militarytools ^
-9