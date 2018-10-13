'''
File: beatextractor.py uses madmom library from https://github.com/CPJKU/madmom to process a music file and generate a beat file
It takes wav file 
'''

from pydub import AudioSegment
import wave
import io
import numpy as np
import sys
import subprocess

beat_file = "beat1.wav"
audio_out_file = "beat_out.wav"
'''
Function: generatebeat: Extracts beat time stamps and generates the wav file only with the beats
Arg : musicfile: The file to be processed using madmom lib to extract beat timestamps
Author: Badarivishal Kinhal
'''

def generatebeat(musicfile):
	
	DBNCommand = "DBNBeatTracker single -o /home/deepspeech/orchestra/dbn1 " + musicfile
	
	subprocess.call(DBNCommand, shell=True)
	
	dbnarray = []
	for line in open('dbn1'):
		dbnarray.append(np.array([float(val) for val in line.rstrip('\n').split(' ') if val != '']))
		
	print "size of dbnarray: ", len(dbnarray)
	#print "dbnarray[10]: ", dbnarray[10]
	
	#read wav file to an audio segment
	beat = AudioSegment.from_wav(beat_file)
	beat_duration = len(beat)
	
	print "beat duration = ", beat_duration
	offset = 0
	final_song = 0
	
	#Need to remove beat duration from the output file. Else the total duration will exceed the original music file
	
	for i in dbnarray:
		# create 1 sec of silence audio segment
		silent_frames = AudioSegment.silent(duration=((float(i)-offset)*1000)-beat_duration)  #duration in milliseconds
		#print "Duration in s = ", float(i)-offset-(.001 * beat_duration)
		offset = float(i)
		#Add above two audio segments
		final_song += (silent_frames + beat)

	#Either save modified audio
	#audio_out_file = "beat_" + musicfile + ".wav"
	final_song.export(audio_out_file, format="wav")

def main():
	musicfile = sys.argv[1]
	print musicfile
	generatebeat(musicfile)	


if __name__ == "__main__":
	main()
