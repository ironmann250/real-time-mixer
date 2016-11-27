import numpy,os,random,time
#from sklearn import tree
from pydub import AudioSegment
from scipy.io.wavfile import read

cur_dir=os.curdir#+'\\Music'
mus_ext=['.mp3','.amr','.wav','.aac','.wma','.midi','.m4r','.m4p','.aud','.ogg','.flv','.mp4','.m4a']
sounds = []
def sumup(array):
    return abs(numpy.sum(array))

def buffer_io(path,ext='.mp3',perc=20):
    ext=ext[1:]
    sound = AudioSegment.from_file(path, format=ext)
    sound_len=len(sound)
    sound_5_perc_last =sound[sound_len-(len(sound)/(perc)):]
    sound_5_perc_first=sound[:(len(sound)/(perc))]
    sound_5_perc_last.export("last_buffer.wav",format="wav")
    sound_5_perc_first.export("first_buffer.wav",format="wav")
    sound,sound_5_perc_last,sound_5_perc_first=[None,None,None]
    first_data = read('first_buffer.wav')
    last_data =  read('last_buffer.wav')
    return [sumup(list(read('first_buffer.wav')[1])),sumup(list(read('last_buffer.wav')[1])),sound_len/1000]

def m3u_maker(playlist):
    m3u=open('playlist.m3u','w')
    m3u.write('')
    m3u=open('playlist.m3u','a')
    m3u.write('#EXTM3U\n')
    for node in playlist:
        m3u.write('#EXTINF:'+str(node[2])+","+node[1]+node[3]+'\n')
        m3u.write(node[0]+'\n')
    m3u.close()

def sort(sounds):
    rand=random.WichmannHill()
    rand.shuffle(sounds)
    ind=0
    playlist=[]
    for sound in sounds:
        if len(playlist)==0:#path,name,ext,first,last,len
            playlist.append([sound[0],sound[1],sound[5],sound[2]]) #path,name,length,extension
            print len(playlist),".",sound[1]
            sounds.remove(sound)
        else:
            tmp_pls=playlist[len(playlist)-1][2]
            sdiff=0
            pointer=0
            diff=None
            for snd in sounds:
                dif=abs(tmp_pls-snd[3])
                if diff == None:
                  diff=dif
                  sind=pointer
                elif dif<diff:
                  diff=dif
                  sind=pointer
                pointer=pointer+1
            sound=sounds[sind]
            playlist.append([sound[0],sound[1],sound[5],sound[2],sound[4]])
            print len(playlist),'.',sound[1]
            sounds.pop(sind)
    tmp_pls=None
    return playlist
now=time.time()
print 'fetching songs in',cur_dir,'...'
for dirName, subdirList, fileList in os.walk(cur_dir):
    for ffname in fileList:
        name,ext = os.path.splitext(ffname)
        fname= os.path.abspath(dirName+'\\'+name+ext)
        if ext in mus_ext and name not in ['last_buffer','first_buffer']:
            snd=os.path.abspath(fname) 
            sounds.append([snd,name,ext]+buffer_io(snd,ext))
            print "added",len(sounds),'songs'

print 'making the playlist'              
playlist=sort(sounds)
while len(sounds) !=0:
    print 'adding left overs'
    playlist=playlist+sort(sounds)
print 'witing to "playlist.m3u"'
m3u_maker(playlist)
print 'done in',time.time()-now,'sec'
