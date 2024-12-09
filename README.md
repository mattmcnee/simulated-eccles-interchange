# Eccles Interchange (M602 - M60)


### Example command to create random traffic
```
python "C:\Program Files (x86)\Eclipse\Sumo\tools\randomTrips.py" -n "merge.net.xml" -o "mergeTraffic.rou.xml" --period 2 --seed 42
```

### Convert OSM to XML
```
netconvert --osm-files map3.osm --output-file motorway.net.xml --geometry.remove --ramps.guess --junctions.join --tls.guess-signals --tls.discard-simple --tls.join
```

### Fix non-viable routes

```
duarouter --net-file merge.net.xml --route-files mergeTraffic.rou.xml --output-file mergeTrafficClean.rou.xml --remove-loops --repair
```

### Run merge sim 
```
sumo-gui -c mergeSim.cfg --delay 200
```


## Interchange

### Random traffic
```
python "C:\Program Files (x86)\Eclipse\Sumo\tools\randomTrips.py" -n "interchange.net.xml" -o "interchangeTraffic.rou.xml" --period 2 --seed 42
```

```
duarouter --net-file interchange.net.xml --route-files interchangeTraffic.rou.xml --output-file interchangeTrafficClean.rou.xml --remove-loops --repair
```

```
sumo-gui -c interchangeSim.cfg --delay 200 --step-length 0.1
```

```
sumo-gui -c interchangeSim.cfg --delay 200 --step-length 0.05
```