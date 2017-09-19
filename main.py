from audioinput import AudioInput
import sys
import signal

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

def main():
    record_sound()


def record_sound():
    audioInput = AudioInput()
    audioInput.start_recording()
    return audioInput


if  __name__ =='__main__':
    print "in main"
    signal.signal(signal.SIGINT, signal_handler)

    main()