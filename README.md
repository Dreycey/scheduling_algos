# Scheduling algorithms

This repository is dedicated to implimenting algorithms related to task
scheduling. 

## to run current code
```
python scheduler.py input.csv 
```

### input

The following graph as a csv:
 
A -> B
 \   |
  D->C->L

```
A,B,1000
A,D,100001
B,C,300
D,C,400
C,L,900
```

### output
```
[['101301.0' 'A']
 ['1200.0' 'B']
 ['1300.0' 'D']
 ['900.0' 'C']
 ['0' 'L']]
```
