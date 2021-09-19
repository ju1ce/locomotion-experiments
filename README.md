# locomotion-experiments

This repository will contain code for my experiments with diffrent types of locomotion for VR. As I feel like moving using the joystick is not immersive and can be annoying, I though I would try out some systems where movement could be done without any input from hands.

## 1. Hip oriented movement

The first one is simple hip oriented movement, where movement is still done with a joystick, but rather than being in the direction of your headset, it is in direction of your hip. This can be accesed here: https://github.com/ju1ce/Simple-OpenVR-Bridge-Driver/tree/hip-locomotion. You can use the newer driver from either this repository, or the ApriltagTrackers repository as well.

## 2. Lean-to-move

Second experiment was: lean in the direction you want to move, turn your hip into the direction you want to turn. This one actualy works fairly well, but still has significant drawbacks which may not make it very useful.

### Problems:

* As in game movement is dependent on your hip and head, many "natural" interactions are no longer possible. You cant lean to peek a corner, you cant try to pick something from a table, you cant try to reach for something on a shelf, as all of these actions will trigger movement.
* There is no feedback on what your current input is - while leaning and twisting your hip, you quickly lose your feel for which direction you should currently be moving and turning in.
* You cant lean the same amount in all directions, since you have more balance in some than others.
* Due to these problems, movement can be a bit inacurate and sometimes do stuff you dont want to do, causing motion sickness

### Possible solutions

* To prevent movement when one doesnt want to move, some sort of walk in place could be implemented to trigger movement.
* To make direction of movement more predictable, instead of moving in the exact direction you are leaning in, snapping to 6 or 8 possible directions may be better. Smooth turning could also be replaced with snap turning.
* Interestingly, having your hands behind you when leaning forward alot can bring you more balance and easier control - in short, naruto running could be used as a trigger for sprinting.
