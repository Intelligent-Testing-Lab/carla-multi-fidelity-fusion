# CARLA Multi-fidelity fusion

This repository contains several experiments for running CARLA at diffrent fidelity levels for evaluating ADS

## Repository structure

> [!NOTE]  
> Need to update
Repository is divided in following structure

- `experiments/`
  - `high_low_fidelity/` (main experiments showing influence of fidelity parameters on execution time and ADS behaviour)
  - `past_experiments/`
    - `fidelity_v1/` (past fidelity experiments on FPS and substepping)
    - `fidelity_v2/` (past fidelity experiments on FPS and render quality)
    - `determinism_check/` (checking if ADS is deterministic spoiler its NOT)
    - `paralelism_check/` (checking how much time we can save on running two instances of CARLA and ADS at once)

Each experiment directory contains `data` for this round of experiments and a Python notebook that loads the data and answer questions.

## Data generation

Data was obtained by [evaluating InterFuser](https://github.com/opendilab/InterFuser?tab=readme-ov-file#evaluation) state of the art autonomous driving system (ADS).  

ADS was evaluated using [custom scripts](https://github.com/PanZWarzywniaka/InterFuser/tree/main/leaderboard/scripts) to change simulator fidelity parameters.

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

Tested with provided `conda` environment (`environment.yml`).

## Contact

Please raise an issue here or send me an email: 

`amosikowicz1@sheffield.ac.uk`