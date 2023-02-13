import os
from pydub import AudioSegment

def commonvoice(srcpath: str, dstpath: str):
    if not os.path.exists(dstpath):
        os.makedirs(os.path.join(dstpath, 'audio'))
        os.makedirs(os.path.join(dstpath, 'transcript'))
    elif not os.path.exists(os.path.join(dstpath, 'audio')):
        os.makedirs(os.path.join(dstpath, 'audio'))
    elif not os.path.exists(os.path.join(dstpath, 'transcript')):
        os.makedirs(os.path.join(dstpath, 'transcript'))

    with open(os.path.join(srcpath, 'validated.tsv'), encoding='utf-8') as f:
        validated = [l.split('\t') for l in f.read().split('\n')] 
        validated_cols = validated.pop(0) #first line has column data

    paths = []
    sentences = []
    for v in validated: #using transpose would be faster but it does not work bc of irregularities
        try:
            paths.append(v[validated_cols.index('path')])
            sentences.append(v[validated_cols.index('sentence')])
        except IndexError as e:
            if v[0] == '':
                continue
            else:
                print(v)
                raise e
        except Exception as e:
            print(v)
            raise e
    
    for p, s in zip(paths, sentences):
        AudioSegment.from_mp3(
            os.path.join(srcpath, 'clips', p)
        ).export(
            os.path.join(dstpath, 'audio', p.replace('.mp3', '.wav')), format='wav'
        )

        with open(os.path.join(dstpath, 'transcript', p.replace('.mp3', '.txt')), 'w', encoding='utf-8') as f:
            f.write(s)

if __name__ == '__main__':
    commonvoice('extras/cv-corpus-12.0-delta-2022-12-07/es', 'data/commonvoice')