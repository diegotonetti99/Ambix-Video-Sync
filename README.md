# Install
Clone the repository and the submodule with the command
~~~
git clone --recurse-submodules https://github.com/diegotonetti99/Ambix-Video-Sync.git
~~~

## Anaconda
This program relies on anaconda to manage all the python libraries and ffmpeg. Create a new virtual environment with the command (use this command only the first time)
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
## IMPORTANT
Install a Python2 interpreter as the Google spatial metadata injector runs on Python2. To do this create a second environment with the command
~~~
conda create -n ambix-py2 python=2.7
~~~

# Usage
To merge Ambisonics audio and 360 Video run the command open the terminal inside the main folder of this repository
~~~
conda run -n ambix python main.py -v video.mp4 -a audio.wav -o output.mov
~~~
where video.mp4 is the recorded video, audio.wav the ambisonics audio file and output.mov is the final merged video with ambisonics audio and injected VR metadata.
