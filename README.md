# Ambix Video Sync
This program automatically merges ambisonics audio and 360 video into a single file using FFmpeg and injects the required metadata with the Google spatial metadata injector.

The audio alignment is done via a FFT cross correlation between the ambix audio and the video audio, it is important that the ambix audio is longer than the recorded video to make the alignment work.



# Install
Clone the repository and the submodule with the command
~~~
git clone --recurse-submodules https://github.com/diegotonetti99/Ambix-Video-Sync.git
~~~

## Anaconda
This program relies on Anaconda to manage all the Python libraries and FFmpeg. Create a new virtual environment with the command (use this command only the first time)
~~~
conda create -n ambix
~~~
then activate the environment with
~~~
conda activate ambix
~~~
Install all the dependencies with the command
~~~
conda install -c conda-forge ffmpeg numpy matplotlib librosa scipy
~~~
## IMPORTANT
Install a Python2 interpreter as the Google spatial metadata injector runs on Python2. To do this create a second environment with the command
~~~
conda create -n ambix-py2 python=2.7
~~~

# Usage
To merge Ambisonics audio and 360 Video run the command open the terminal **inside the main folder** of this repository
~~~
conda run -n ambix python main.py -v video.mp4 -a audio.wav -o output.mp4
~~~
where video.mp4 is the recorded video, audio.wav is the ambisonics audio file and output.mp4 is the final merged video with ambisonics audio and injected VR metadata.

I prefer mp4 video format as output as both the suggested players recognize it.

# Player
On smartphone and PC, I suggest using [VLC](https://www.videolan.org/) as it supports AMBIX audio format.
On a VR headset use [showtime vr](https://showtimevr.eu/) if the preinstalled player doesn't work with spatial audio (e.g. I experienced some troubles with Meta built-in player).
