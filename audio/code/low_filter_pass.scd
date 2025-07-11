// Step 1: Get the current file's directory path
~fileDir = thisProcess.nowExecutingPath.standardizePath.dirname;

// Step 2: Load the sound file from the same directory
b = Buffer.read(s, ~fileDir +/+ "materials/quote2.wav");  // Replace "soundfile.wav" with your file's name

// Step 3: Play the sound with a low-pass filter
(
SynthDef(\playWithLPF, {
    var sound, filteredSound;
    sound = PlayBuf.ar(1, b, BufRateScale.kr(b), loop: 1);  // Load the buffer
    filteredSound = LPF.ar(sound, 500);  // Apply a low-pass filter with a cutoff frequency of 500 Hz
    Out.ar(0, filteredSound * 85);  // Output the sound, adjusting volume as needed
}).add;
)

x = Synth(\playWithLPF);
y = Synth(\playWithLPF);

x.free;
y.free;
