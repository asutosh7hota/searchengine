#!/bin/bash
#SBATCH --time=0-00:05:00
#SBATCH --mem-per-cpu=500

srun python3 test.py
