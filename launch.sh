#!/bin/bash
cd $(dirname "$(realpath "$0")")
conda run -n ambix python gui.py
