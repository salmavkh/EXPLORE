// Deep space soundscape with low-pass filter
(
{
    var baseFreq = LFNoise1.kr(0.05).range(20, 40); // Slowly changing base frequency
    var filterFreq = LFNoise1.kr(0.1).range(500, 2000); // Slow filter movement
    var panPosition = LFNoise1.kr(0.2).range(-1, 1); // Random panning

    // Base sound layer: a filtered saw wave
    var deepSpaceBase = LPF.ar(Saw.ar(baseFreq, 0.2), filterFreq);

    // Subtle background layer with noise
    var backgroundNoise = HPF.ar(PinkNoise.ar(0.1), 100) * 0.1;

    // Pulsing stars or signals: random blips
    var blips = Decay.ar(
        Dust.ar(0.2),
        0.2,
        SinOsc.ar(LFNoise1.kr(2).range(100, 400), 0, 0.3)
    );

    // Combined soundscape with random panning
    var spaceSound = (deepSpaceBase + backgroundNoise + blips).dup(2);
    spaceSound = Pan2.ar(spaceSound, panPosition);

    // Apply reverb
    spaceSound = FreeVerb.ar(spaceSound, mix: 0.3, room: 0.8, damp: 0.5);

    // Apply low-pass filter to the entire output
    spaceSound = LPF.ar(spaceSound, 800); // Adjust frequency as needed for depth

    // Output the final sound
    Out.ar(0, spaceSound);
}.play;
)
