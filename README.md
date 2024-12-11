# Eccles Interchange (M602 - M60)

SUMO (Simulation of Urban MObility) coverage of Eccles Interchange in Manchester.

This repository explores a lane removal through the interchange on the M60. This has the potential to reduce journey times from the M602 to the M60 by up to 15%.

A full report on these findings is available [here](https://github.com/mattmcnee/simulated-eccles-interchange/blob/main/results/Eccles_Interchange.pdf).

For more details on how to setup your own simulation, there's a helpful video by Dr. Joanne Skiles on YouTube [here](https://www.youtube.com/watch?v=wZycufsTEGU).

## Commands to run the experiment

#### Run experiment with existing lane structure
```
python .\runExperiment.py --net-file interchange.net.xml
```

#### Visualise simulation with existing lane structure
```
sumo-gui -c interchangeSim.cfg --delay 200 --step-length 0.05
```

#### Run experiment with proposed solution
```
python .\runExperiment.py --net-file interchange-variation-1.net.xml
```

#### Visualise simulation with proposed solution
```
sumo-gui -c interchangeNewSim.cfg --delay 200 --step-length 0.05
```

## Other useful commands

#### Convert OSM to XML
```
netconvert --osm-files map3.osm --output-file motorway.net.xml --geometry.remove --ramps.guess --junctions.join --tls.guess-signals --tls.discard-simple --tls.join
```

#### Create random traffic
```
python "C:\Program Files (x86)\Eclipse\Sumo\tools\randomTrips.py" -n "interchange.net.xml" -o "interchangeTraffic.rou.xml" --period 2 --seed 42
```

#### Fix non-viable routes

```
duarouter --net-file interchange.net.xml --route-files interchangeTraffic.rou.xml --output-file interchangeTrafficClean.rou.xml --remove-loops --repair
```