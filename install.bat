@echo off
echo Creating conda environment...
conda env create -f environment.yml
echo Activating environment...
call conda activate uni_rank_env
echo Installation complete.
pause