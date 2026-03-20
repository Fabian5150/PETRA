## Process Enhancement Toolkit with Reinforcement Agents (PETRA)
Needs python 3.9 for Simod and Prosimos to work. <br>
Create a venv, then install the requirements with ```pip install -r requirements.txt```

Different simulation models can be loaded with the load_sim_model.py script. <br>
Simply run ```python load_sim_model (logname) (simulation type)```

Lognames are:
- ```bpi_2012```
- ```bpi_2013```
- ```manufacturing```
- ```purchase```

Simulation types are:
- ```agents```
- ```control-flow```

To start the webserver, go into the /app directory and start fastapi with: <br>
```uvicorn main:app --reload```