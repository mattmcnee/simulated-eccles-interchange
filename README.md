# Eccles Interchange (M602 - M60)


### Example command to create random traffic
```
python "C:\Program Files (x86)\Eclipse\Sumo\tools\randomTrips.py" -n "merge.net.xml" -o "mergeTraffic.rou.xml" --period 2 --seed 42
```

```
duarouter --net-file merge.net.xml --route-files mergeTraffic.rou.xml --output-file mergeTrafficClean.rou.xml --remove-loops --repair
```

```
sumo-gui -c mergeSim.cfg --delay 200
```