# Install
Clone the repository and the submodule with the command
~~~
git clone --recurse-submodules git@github.com:diegotonetti99/Ambix-Video-Sync.git
~~~

## Anaconda
I suggest using anaconda to manage all the python libraries and ffmpeg. Create a new virtual environment with the command (use this command only the first time)
~~~
conda create -n ambix
~~~
then activate the enviroment with
~~~
conda activate ambix
~~~
Install all the dependencies with the command
~~~
conda install -c conda-forge ffmpeg numpy matplotlib librosa
~~~
