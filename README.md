# CARLA Multi-fidelity fusion

## Raw data

Raw data sits in `results/` directory.

### Fidelity data

#### Generating data

Data was obtained by [evaluating InterFuser](https://github.com/opendilab/InterFuser?tab=readme-ov-file#evaluation) state of the art autonomous driving system (ADS).  

ADS was evaluated 8 times, executing 10 scenarios each using [custom script](https://github.com/PanZWarzywniaka/InterFuser/blob/main/leaderboard/scripts/run_fidelity_evals.sh) to chage simulator fidelity parameters.

Fidelity parameters:
- FPS: `int`  defined as: 1/[fixed_delta_seconds](https://carla.readthedocs.io/en/latest/python_api/#carla.WorldSettings.fixed_delta_seconds), default: 20
- [Substepping](https://carla.readthedocs.io/en/latest/python_api/#carla.WorldSettings.substepping): `bool`, default: True

#### Structure
Data structured in following way:

Each file is record of running 10 evaluations.
Name of the file indicates fidelity params underwhich [InterFuser](https://github.com/opendilab/InterFuser) has been evaluated.
So e.g. 
- `fidelity_eval_20_fps_substepping_1.json` CARLA was running at 20FPS with substepping turned ON (default evaluation)
- `fidelity_eval_10_fps_substepping_0.json` CARLA was running at 10FPS with substepping turned OFF


### Determinism data

Subsidiary evaluation to check if ADS was deterministic.

## Tools and visualisation

Please see Python notebook where data is loaded and visualised.

## Requirements

- Python
- Pandas
- Numpy
- Scipy
- Matplotlib

Tested with provided `conda` enviroment.
