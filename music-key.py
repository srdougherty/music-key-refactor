import pygame.midi
import time
import time, sys, os
import PySimpleGUI as sg

instD = { 'ピアノ': 0, 'マリンバ': 12,
          'オルガン': 19,'ハーモニカ':22,
          'ギター': 24,'ヴァイオリン': 40,
          'ビオラ':41,'チェロ':42,
          'コントラバス':43,'ハープ':46,
          'ティンパニー':47,'トランペット': 56,
          'チューバ':58,'アルトサックス': 65,
          'クラリネット':71,'ファゴット':70,
          'ピッコロ':72,'フルート': 73,'リコーダー':74,
          '声': 91,'琴':107, '鳥':123, }


sg.theme('Lightgreen')
sg.set_options(font = (None, 24))

notename = ["ド","C#","レ","D#","ミ","ファ","F#","ソ",
            "G#","ラ","A#","シ"]

layout = [ [ sg.B('pause'),sg.Push(),sg.B('keep'),
             sg.Push(),sg.B('play'),sg.Push(),
             sg.B('loading'),sg.Push(),
             sg.FileBrowse('Load')],
          [  sg.Push(),
             sg.B(k=1, size=(3, 2),
                  button_color=('brown on black')),
             sg.B(k=3, size=(3, 2),
                  button_color=('brown on black')),
             sg.B(k=999, size=(3,2),
                  button_color='pink',border_width=0),
             sg.B(k=6, size=(3, 2),
                  button_color=('brown on black')),
             sg.B(k=8, size=(3, 2),
                  button_color=('brown on black')),
             sg.B(k=10, size=(3, 2),
                  button_color=('brown on black')),
             sg.B(k=999, size=(3,2),
                  button_color='pink',border_width=0),
             sg.B(k=13, size=(3, 2),
                  button_color=('brown on black')),
             sg.B(k=15, size=(3, 2),
                  button_color=('brown on black')),
             sg.Push(),],
          [  sg.B(k=0, size=(3, 2),  #3が横,2がたて
                  button_color=('brown on White')),
             sg.B(k=2, size=(3, 2),
                  button_color=('brown on White')),
             sg.B(k=4, size=(3, 2),
                  button_color=('brown on White')),
             sg.B(k=5, size=(3, 2),
                  button_color=('brown on White')),
             sg.B(k=7, size=(3, 2),
                  button_color=('brown on White')),
             sg.B(k=9, size=(3, 2),
                  button_color=('brown on White')),
             sg.B(k=11, size=(3, 2),
                  button_color=('brown on White')),
             sg.B(k=12, size=(3, 2),
                  button_color=('brown on White')),
             sg.B(k=14, size=(3, 2),
                  button_color=('brown on White')),
             sg.B(k=16, size=(3, 2),
                  button_color=('brown on White')),],
        [    sg.Combo(list(instD.keys()), k=88,
                      default_value='ピアノ'),
             sg.I(k='Ld', enable_events=1, size=(30,1))],
          [ sg.ML(k='txt', size=(30, 5)) ]]

win = sg.Window("Music", layout,finalize=True,
                background_color = 'pink')

# 0: Piano, 19:Organ, 40:Violin 56:Trumpet, 91:Voice
# https://fmslogo.sourceforge.io/manual/midi-instrument.html
instval = 0
pygame.midi.init()
odv = pygame.midi.Output(0)


majorscale = [0,1,2,3,4,5,6,7,8,9,10,
              11,12,13,14,15,16,17,18,
              19,20,21,22,23,24,25,26,
              27,28,29,30]

def note1(note, length=0.25):
    note = int(note)
    note += shift
    odv.set_instrument(instN, 1)
    odv.note_on(note, 127,1)
    print(notename[(note)%12] + str((note)//12-2))
    time.sleep(length)
    odv.note_off(note,127,1)
def noteM(noteL):
    n1L = [int(e) for i,e in enumerate(noteL) if i%2==0]
    print(len(noteL), noteL, n1L)
    for note in n1L:
        if note >= 0: odv.note_on(note, 127, 1)
    print(notename[(note)%12] + str((note)//12-2))
    time.sleep(float(noteL[1]))
    for note in n1L:
        if note >= 0: odv.note_off(note, 127, 1)
def playrowTL():
      odv.set_instrument(instN, 1)
      odv.note_on(rowTL[1], 127, 1)
        
time1 = 0
score = ''
length = 0.5
shift = 0
rowTL = None
scoreTL = []
txt = ''

while True:
     e, v = win.read()
     if e is None: break
     print(e, v)
     speed = win.read(timeout=125)
     if e == 'play':
        instN = v[88]
        for row in score.splitlines():
            print(row)
            L = row.split()
            if int(L[0]) == -1:
                time.sleep(float(L[1]))
            else:
                noteM(L)
     elif e == 'pause':
         time.sleep(length)
         score += f'{-1} {length}\n'
     elif e == 'keep':
         with open('score.txt', 'w') as f:
             f.write(score)
     elif e == 'loading':
         with open('score.txt', 'r') as f:
             score = f.read()
     elif e=='Ld':
         with open(v['Ld'], 'r') as f:
             score = f.read()

     elif int(e) in range(18):
         instN = instD[v[88]]
             #()の中の数字はmajoescaleの[]の中の数
         note1(e + 60)
             # + 60,2)にすると音の出る長さが長くなる
         score += f'{e+60} {length}\n'

        
pygame.quit()    

