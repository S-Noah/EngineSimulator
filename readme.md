# Sarge's Engine Simulator

## Warning

The audio produced by this appliation can unprediable. It has undergone signifigant testing but there are no guarantees. You have been warned.

## Introduction

Engine Simulator is a real-time thermodynamics simulation that attempts to mimic the sound commonly found in an engine. This Prototype implments the Ideal Gas Law represented by:
 $$PV = nRT$$ 
 as well as the Kinetic Theory of Gases represented by:
 $$E_k = nRT * 1.5$$

This simulation focuses on a single piston in no particular pattern. This is a good start at modeling the forces, pressures, and math behind a real Engine Simulation.

This simulation also takes a stab at producing audio from the pressures and forces, while this is not an exact science, this is an unfiltered approximation. There is some unwanted white noise due to the lack of filtering and equalization.

This prototype is built in Python to demonstrate the feasibility of the application.

## Dependencies
| Dependency    | Usage  |
| ------------- | ----------- |
| Python  | Main Programming Language |
| Pygame  | Graphics, Keyboard, and Mouse. (SDL2 port for Python)|
| Numpy   | For Waveform creation, calculation, and organization |
| Pyaudio | Streams Real-Time Audio (Port Audio port for Python)


## Controls
| Key / Slider  | Description |
| ------------- | ------- |
| W | Increase RPM |
| S | Decrease RPM |
|Base Frequency | Midpoint for Synthesized Audio |
|Base Amplitude | Filter for Synthesized Audio   |



## Requirements & Features

While none of the requirements or features are fully implemented, here are the ones attempted.
#### Requirements

- [x] Run Simulation                
- [x] Control Simulation
- [ ] View Simulation Data
- [x] Hear Synthesized Audio
- [ ] Input Custom Engine 
- [x] Adjust Settings

#### Features

- [x] Fluid Dynamics                
- [x] Physics-Based Sound Synthesis
- [ ] User Interface
- [ ] Various Input Methods
- [ ] Variable Engine Configuration
- [ ] Real Vehicle Compatibility

## Todo
- [ ] Include Work calculation for changing volume on an Ideal Gas
- [ ] Include Flow calculation for exhaust and intake manifolds
- [ ] Include white noise / mechanical chaos into the Sound Synthesis
- [ ] Create an engine with multiple pistons
- [ ] Create a better Sound Synthesis Algorithm
- [ ] Create a useful and intresting User Interface
- [ ] Create a true Engine / Vehicle with gears and other mechanial features
- [ ] Create an Engine Configuration Editor and GUI
- [ ] Create an Arduino Based Throttle Control
- [ ] Create an ODB2 Car Connection
- [ ] Add Low-Pass, High-Pass, Convolution Filtering to Sound Synthesis.
- [ ] Add Equalization to Sound Synthesis.
- [ ] Add more to the Todo list.
