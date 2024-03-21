import pygame.midi
import time, os
import PySimpleGUI as sg

# 0: Piano, 19:Organ, 40:Violin 56:Trumpet, 91:Voice
# https://fmslogo.sourceforge.io/manual/midi-instrument.html
INSTRUMENTS = {
    'ピアノ': 0,
    'マリンバ': 12,
    'オルガン': 19,
    'ハーモニカ':22,
    'ギター': 24,
    'ヴァイオリン': 40,
    'ビオラ':41,
    'チェロ':42,
    'コントラバス':43,
    'ハープ':46,
    'ティンパニー':47,
    'トランペット': 56,
    'チューバ':58,
    'アルトサックス': 65,
    'クラリネット':71,
    'ファゴット':70,
    'ピッコロ':72,
    'フルート': 73,
    'リコーダー':74,
    '声': 91,
    '琴':107,
    '鳥':123,
}


NOTE_NAMES = [
    "ド",
    "C#",
    "レ",
    "D#",
    "ミ",
    "ファ",
    "F#",
    "ソ",
    "G#",
    "ラ",
    "A#",
    "シ",
]

def getNoteName(noteIndex: int):
    return NOTE_NAMES[(noteIndex) % len(NOTE_NAMES)]

class NotePlayer:
    def __init__(self, outputDevice: pygame.midi.Output):
        self.outputDevice = outputDevice
        self.shift = 0
        self.rowTL = None
        self.instrumentID = INSTRUMENTS['ピアノ']
        self.channel = 1
        self.velocity = 127
        self.cancel = False
    
    def setInstrument(self, instrumentID: int):
        self.instrumentID = instrumentID
        self.outputDevice.set_instrument(self.instrumentID, self.channel)

    def note1(self, note, length=0.25):
        note = int(note)
        note += self.shift
        self.setInstrument(self.instrumentID)
        self.outputDevice.note_on(note, self.velocity, self.channel)
        print(getNoteName(note) + str((note)//len(NOTE_NAMES)-2))
        time.sleep(length)
        self.outputDevice.note_off(note, self.velocity, self.channel)
    
    def noteM(self, noteL):
        n1L = [int(event) for i,event in enumerate(noteL) if i%2==0]
        print(len(noteL), noteL, n1L)
        for note in n1L:
            if note >= 0: self.outputDevice.note_on(note, self.velocity, self.channel)
        print(getNoteName(note) + str((note)//len(NOTE_NAMES)-2))
        time.sleep(float(noteL[1]))
        for note in n1L:
            if note >= 0: self.outputDevice.note_off(note, self.velocity, self.channel)
    
    def playrowTL(self):
        self.setInstrument(self.instrumentID)
        self.outputDevice.note_on(self.rowTL[1], self.velocity, self.channel)


def playScore(player: NotePlayer, score: str):
    for row in score.splitlines():
        if player.cancel:
            break
        print(row)
        L = row.split()
        if int(L[0]) == -1:
            time.sleep(float(L[1]))
        else:
            player.noteM(L)


KEY_BUTTON_SIZE = (3, 2)    # size 3が横,2がたて

def createKeySpacer() -> sg.Text:
    return sg.B(k=999, size=KEY_BUTTON_SIZE, button_color=sg.theme_background_color(), border_width=0, disabled=True)

def createKeyButton(key: int, color: str = 'black or white') -> sg.Button:
    return sg.Button(k=key, size=KEY_BUTTON_SIZE, button_color=(f'brown on {color}'))

def createWhiteKeyButton(key: int):
    return createKeyButton(key, 'white')

def createBlackKeyButton(key: int):
    return createKeyButton(key, 'black')

def createWindow() -> sg.Window:
    layout = [
        # 機能ボタン
        [
            sg.Button('pause'),
            sg.Push(),
            sg.Button('keep'),
            sg.Push(),
            sg.Button('play'),
            sg.Push(),
            sg.Button('stop'),
            sg.Push(),
            sg.Button('loading'),
            sg.Push(),
            sg.FileBrowse('Load', target='-CURRENT_FILE-'),
        ],
        [
            sg.Column([[sg.Push()]]),
            sg.Column([
                # 黒キー
                [
                    sg.Push(),
                    createBlackKeyButton(1),
                    createBlackKeyButton(3),
                    createKeySpacer(),
                    createBlackKeyButton(6),
                    createBlackKeyButton(8),
                    createBlackKeyButton(10),
                    createKeySpacer(),
                    createBlackKeyButton(13),
                    createBlackKeyButton(15),
                    sg.Push(),
                ],
                # 白キー
                [
                    createWhiteKeyButton(0),
                    createWhiteKeyButton(2),
                    createWhiteKeyButton(4),
                    createWhiteKeyButton(5),
                    createWhiteKeyButton(7),
                    createWhiteKeyButton(9),
                    createWhiteKeyButton(11),
                    createWhiteKeyButton(12),
                    createWhiteKeyButton(14),
                    createWhiteKeyButton(16),
                ],
            ]),
            sg.Column([[sg.Push()]]),
        ],
        # 入力
        [
            sg.Combo(list(INSTRUMENTS.keys()), k='-CURRENT_INSTRUMENT-', default_value='ピアノ', readonly=True, size=(13, 1)),
            sg.Input(k='-CURRENT_FILE-', enable_events=True, size=(30,1))
        ],
        [
            sg.Multiline(k='txt', size=(30, 5))
        ]
    ]

    win = sg.Window("Music", layout,finalize=True)
    return win


def startEventLoop(win: sg.Window, player: NotePlayer):
    score = ''
    length = 0.5

    while True:
        event, values = win.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        print(event, values)
        speed = win.read(timeout=125)
        if event == 'play':
            player.setInstrument(INSTRUMENTS[values['-CURRENT_INSTRUMENT-']])
            player.cancel = False
            win.start_thread(lambda : playScore(player, score))
        elif event == 'stop':
            player.cancel = True
        elif event == 'pause':
            time.sleep(length)
            score += f'{-1} {length}\n'
        elif event == 'keep':
            with open('score.txt', 'w') as f:
                f.write(score)
        elif event == 'loading':
            with open('score.txt', 'r') as f:
                score = f.read()
        elif event == '-CURRENT_FILE-':
            filename = values['-CURRENT_FILE-']
            if filename:
                print(f"filename: {filename}")
                if os.path.exists(filename):
                    with open(filename, 'r') as f:
                        score = f.read()
        elif int(event) in range(18):
            player.setInstrument(INSTRUMENTS[values['-CURRENT_INSTRUMENT-']])
                #()の中の数字はmajoescaleの[]の中の数
            player.note1(event + 60)
                # + 60,2)にすると音の出る長さが長くなる
            score += f'{event+60} {length}\n'


def main() -> int:
    # midiの初期化
    pygame.midi.init()
    outputDevice = pygame.midi.Output(0)
    
    # PySimpleGUIの初期化
    sg.theme('Lightgreen')
    bgColor = 'pink'
    sg.theme_background_color(bgColor)
    sg.theme_text_element_background_color(bgColor)
    sg.theme_element_background_color(bgColor)
    sg.set_options(font = (None, 24))

    # ウィンドウの初期化
    win = createWindow()
    
    # イベントループ開始
    player = NotePlayer(outputDevice)
    startEventLoop(win, player)
    win.close()

    # クリーンアップ
    pygame.quit()

    return 0

if __name__ == '__main__':
    main()
