'''
    This program merges together ambisonics audio and 360 video self aliging the external audio track on the video audio track using cross correlation. 

    The external audio truck MUST BE LONGER than the video track, so start recording the external audio, than video, than stop video and finally stop recording the external audio.

    This program requires ffmpeg installed in the host machine.

    The resulting video is not recognized as 360video+ambisonics as it needs metadata that must be injected with another program like https://github.com/google/spatial-media/.

'''



import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, io
import librosa
import subprocess
import argparse
import os

def align(input_video, input_ambix, video_audio, trimmed_ambix):
    # Command to extract audio track
    command = [
        'ffmpeg',
        '-i', input_video,        # Input video file
        '-q:a', '0',             # Set audio quality to highest
        '-map', '0:a:0',         # Select the audio stream from the input file
        '-vn',                   # Disable the video recording
        '-y',
        video_audio        # Output audio file
    ]

    # run the ffmpeg command and print the output
    print(subprocess.run(command, capture_output=True))

    audio_video, _ = librosa.load(video_audio, mono=True)
    ambisonics, fs = librosa.load(input_ambix, mono=False)
    # resample audio_video if needed
    if _ != fs:
        audio_video = librosa.resample(audio_video, orig_sr=_, target_sr=fs)


    # filter the audio tracks with a low pass filter
    sos = signal.butter(10, fs//4, btype='low', analog=False, fs=fs, output='sos')
    audio_video_filtered = signal.sosfilt(sos, audio_video)
    w_filtered = signal.sosfilt(sos, ambisonics[0])

    # comupute cross-correlation between audio tracks
    correlation = signal.correlate(audio_video_filtered, w_filtered, mode='full')

    # find the time lag between the two audio tracks
    lags = signal.correlation_lags(audio_video_filtered.size, w_filtered.size, mode='full')
    time_lag = lags[np.argmax(correlation)]

    # calculate the time lag
    print(time_lag)

    # align the ambix audio with the video audio and trim the excess
    ambisonics_trimmed = np.roll(ambisonics, time_lag, axis=1)[:, 0:audio_video.size]

    # save the trimmed amibx audio
    io.wavfile.write(trimmed_ambix, fs, ambisonics_trimmed.T)
    return ambisonics_trimmed, audio_video

def merge(input_video, trimmed_ambix, merged_video):
    # Command to replace audio track
    command = [
        'ffmpeg',
        '-i', input_video,       # Input video file
        '-i', trimmed_ambix,   # Input new audio file
        '-c:v', 'copy',         # Copy the video stream as-is
        '-c:a', 'aac',          # Encode the audio to AAC format
        '-map', '0:v:0',        # Use the video stream from the first input
        '-map', '1:a:0',        # Use the audio stream from the second input
        '-y',
        merged_video            # merged file
    ]

    # run the ffmpeg command and print the output
    print(subprocess.run(command, capture_output=True))

    print('Video and Audio merged!')

def inject(merged_video, output_video):
    # use google spatial metadata injector to write metdatata for 360 + ambisonics
    path = os.path.dirname(__file__)
    command = [
        'conda',
        'run',
        '-n',
        'ambix-py2',
        'python',
        path+'/spatial-media/spatialmedia',
        '-i',
        '--stereo=none',         # Copy the video stream as-is
        '--spatial-audio',          # Encode the audio to AAC format
        merged_video,            # non metadata file
        output_video            # output video
    ]
    print(subprocess.run(command, capture_output=True))

def clear(merged_video, trimmed_ambix, video_audio):
    os.remove(merged_video)
    os.remove(trimmed_ambix)
    os.remove(video_audio)

def main(input_video, input_ambix, output_video):

    # temporary file - no need to edit
    video_audio = 'video_audio.wav'
    trimmed_ambix = 'trimmed_ambix.wav'
    merged_video = 'merged.mov'

    # align the ambix audio with the video audio and trim the excess
    ambisonics_trimmed, audio_video = align(input_video, input_ambix, video_audio, trimmed_ambix)

    # plot 
    _, ax = plt.subplots(2,1,sharex=True)
    ax[0].plot(audio_video)
    ax[1].plot(ambisonics_trimmed[0])
    plt.show()

    merge(input_video, trimmed_ambix, merged_video)

    inject(merged_video, output_video)

    clear(merged_video, trimmed_ambix, video_audio)    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide input video and audio and the output video file name ')
    parser.add_argument('-v', '--video', type=str, required=True,help='Path to the input video file')
    parser.add_argument('-a', '--audio', type=str, required=True,help='Path to the input audio file')
    parser.add_argument('-o', '--output', type=str, required=True,help='Path to the output file. Requires .mov extension!')

    args = parser.parse_args()

    input_video = args.video
    input_ambix = args.audio
    output_video = args.output

    main(input_video, input_ambix, output_video)
    exit()