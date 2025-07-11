(
SynthDef(\gamelanSound, {
    arg out = 0, freq = 220, amp = 0.3;
    var env, overtones, sound, delayedSound;

    // Generate layered tones to create a metallic ringing sound
    overtones = Mix.fill(5, { |i| SinOsc.ar(freq * (i + 1)) * (1 / (i + 1)) });

    // Use a percussive envelope to make the sound start quickly and fade out slowly
    env = EnvGen.kr(Env.perc(0.01, 1), doneAction: 2);
    sound = overtones * env * amp;

    // Add echo to create a richer, more resonant effect
    delayedSound = CombN.ar(sound, 0.5, 0.25, 4); // Delay settings: max delay time, delay time, number of echoes
    sound = sound + (delayedSound * 0.5); // Blend the echo into the main sound

    // Randomly pan the sound between left and right speakers
    Out.ar(out, Pan2.ar(sound, LFNoise1.kr(0.1).range(-1, 1)));
}).add;


SynthDef(\wind, {
    arg out = 0, amp = 5;
    var windSound;

    // Generate wind sound using filtered noise with slow modulation
    windSound = PinkNoise.ar(amp) * XLine.kr(0.2, 0.1, 60); // Slowly fades
    windSound = LPF.ar(windSound, LFNoise2.kr(0.05).range(300, 1000)); // Modulating low-pass filter
    windSound = windSound * EnvGen.kr(Env.asr(2, 1, 2), doneAction: 2); // Long envelope

    Out.ar(out, windSound);
}).add;


)

// Use Pbind to play a continuous pattern for the gamelan sound
(
Pbind(
    \instrument, \gamelanSound,
    \freq, Pseq([100, 100, 100, 100, 100], inf) + Pwhite(-10, 10, inf), // Randomize pitch
    \amp, 0.3,                      // Volume level
    \dur, Pexprand(0.9, 0.9, inf)   // Duration for faster notes
).play;
)

// Define the pattern with Pbindef
Pbindef(\tempGamelan,
    \instrument, \gamelanSound,
    \freq, Pseq([100, 100, 100, 100, 100], inf) + Pwhite(-10, 10, inf), // Randomize pitch
    \amp, 0.8,                      // Volume level
    \dur, Pexprand(0.9, 0.9, inf)   // Duration for notes
);


Pbindef(\tempGamelan2,
    \instrument, \gamelanSound,
    \freq, Pseq([600, 400, 600, 400], inf) + Pwhite(-10, 10, inf), // Randomize pitch
	\dur, Pseq([0.2, 0.2], inf), // Create a rhythm by alternating durations
    \amp, 0.1                      // Volume level

);

Pbindef(\tempGamelan3,
    \instrument, \gamelanSound,
    \freq, Pseq([300, 300, 300, 300, 300], inf) + Pwhite(-10, 10, inf), // Randomize pitch
    \amp, 0.3,                      // Volume level
    \dur, Pexprand(0.9, 0.9, inf)   // Duration for notes
);

x = (
Synth(\wind);
)
x.free;

Pbindef(\tempGamelan).play;
Pbindef(\tempGamelan2).play;
Pbindef(\tempGamelan3).play;

Pbindef(\tempGamelan).stop;
Pbindef(\tempGamelan2).stop;
Pbindef(\tempGamelan3).stop;




Server.default.options.numInputBusChannels = 0; // Disable input channels
s.reboot; // Reboot the server

Server.default.options.device = "SC Aggregate"; // Replace with your aggregate device name
Server.default.options.numInputBusChannels = 0; // Disable input if not needed
s.reboot; // Reboot the server

s.options.hardwareBufferSize = 512; // Try 512 or 256 for better quality
s.reboot;






