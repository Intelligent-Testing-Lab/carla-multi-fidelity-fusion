# CARLA Multi-fidelity fusion

This repository contains several experiments for running CARLA at diffrent fidelity levels for evaluating ADS

## Repository structure

Repository is divided in following structure

- `experiments/`
  - `fidelity/` (main experiments showing influence of fidelity parameters on execution time and ADS behaviour)
  - `past_experiments/`
    - `determinism_check/` (checking if ADS is deterministic spoiler its NOT)
    - `paralelism_check/` (checking how much time we can save on running two instances of CARLA and ADS at once)
    - `old_fidelity_experiments/` (past fidelity experiments)

Each experiment directory contains `data` for this round of experiments and a Python notebook that loads the data and answear questions.

## Data genertion

Data was obtained by [evaluating InterFuser](https://github.com/opendilab/InterFuser?tab=readme-ov-file#evaluation) state of the art autonomous driving system (ADS).  

ADS was evaluated using [custom scripts](https://github.com/PanZWarzywniaka/InterFuser/tree/main/leaderboard/scripts) to chage simulator fidelity parameters.

<!-- Fidelity parameters:
- FPS: `int`  defined as: 1/[fixed_delta_seconds](https://carla.readthedocs.io/en/latest/python_api/#carla.WorldSettings.fixed_delta_seconds), default: 20
- [Substepping](https://carla.readthedocs.io/en/latest/python_api/#carla.WorldSettings.substepping): `bool`, default: True -->

<!-- #### Structure
Data structured in following way:

Each file is record of running 10 evaluations.
Name of the file indicates fidelity params underwhich [InterFuser](https://github.com/opendilab/InterFuser) has been evaluated.
So e.g. 
- `fidelity_eval_20_fps_substepping_1.json` CARLA was running at 20FPS with substepping turned ON (default evaluation)
- `fidelity_eval_10_fps_substepping_0.json` CARLA was running at 10FPS with substepping turned OFF -->


<!-- ### Determinism data

Subsidiary evaluation to check if ADS was deterministic. -->

## Requirements

- Python
- Pandas
- Numpy
- Scipy
- Matplotlib

Tested with provided `conda` enviroment (`environment.yml`).

## Contact

Please raise an issue here or send me an email: 

`amosikowicz1@sheffield.ac.uk`