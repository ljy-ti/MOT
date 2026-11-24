# Enhancing Multi-Object Tracking via Dynamic-Weight Linear Interpolation and Weak Clue Fusion

## Overview

This research code addresses multi-object tracking (MOT) in scenes with occlusion, non-rigid motion, and ambiguous association cues. The project builds on OC-SORT and Deep-OC-SORT and includes Dynamic-Weight Linear Interpolation (DWLI), height-modulated IoU (HMIoU), and confidence-state modeling (CST). Pseudo-Depth Association (PDA) is described in the manuscript; its integration into the exact experimental entry point remains to be confirmed. The repository contains multiple development variants, so the default command is not necessarily the full manuscript method.

## Repository layout

- `main.py`: tracking entry point using `trackers/strong_ocsort`.
- `main_third.py`: alternative tracking entry point.
- `trackers/strong_ocsort/association.py`: HMIoU and association cost functions.
- `trackers/strong_ocsort/ocsort.py`: tracking state, confidence and association.
- `trackers/strong_ocsort/interpolation/DWLI.py`: standalone DWLI post-processing.
- `dataset.py`: dataset loading and annotation requirements.
- `external/YOLOX/`, `external/deep-person-reid/`, `external/fast_reid/`: detector and appearance-model dependencies.
- `external/TrackEval/`: benchmark evaluation.
- `cache/`: precomputed detections and camera-motion data.
- `results/gt/seqmaps/`: evaluation sequence lists.

## Installation and environment

Clone this repository and work from the actual project directory:

```bash
git clone https://github.com/LJY-TI/MOT.git
cd MOT/sy-dwli-wcf-main/sy-dwli-wcf-main
```

See [DEPENDENCIES.md](DEPENDENCIES.md) for the dependency inventory and installation considerations. The earlier project documentation lists Python 3.8+, PyTorch 1.10.1, CUDA 11.3/11.8 and Linux as reference environment information. These versions have not been revalidated for the current checkout. In particular, check NumPy and PyTorch API compatibility and use a compatible CUDA build.

## Data preparation

Obtain the datasets from their official sources:

- MOT17 and MOT20: https://motchallenge.net/
- DanceTrack: https://github.com/DanceTrack/DanceTrack

The data loader expects the following directory names (case sensitive) relative to the project root, not a directory called `datasets`:

```text
data/
  MOT17/
    train/
    test/
    annotations/
      val_half.json
      test.json
  MOT20/
    train/
    test/
    annotations/
      val_half.json
      test.json
  dancetrack/
    train/
    val/
    test/
    annotations/
      val.json
      test.json
```

The JSON files must be in the COCO-style format required by `dataset.py`. Downloading raw benchmark images alone is not sufficient. The exact annotation conversion procedure and experimental split configuration still need to be documented and verified.

## Model weights

The code expects detector and appearance-model checkpoints under `external/weights/`. These are not included in the current checkout.

| Purpose | Expected filename |
| --- | --- |
| MOT17 test detector | bytetrack_x_mot17.pth.tar |
| MOT17 validation detector | bytetrack_ablation.pth.tar |
| MOT20 test detector | bytetrack_x_mot20.tar |
| DanceTrack detector | ocsort_dance_model.pth.tar |
| MOT17 test ReID | mot17_sbs_S50.pth |
| MOT20 test ReID | mot20_sbs_S50.pth |
| DanceTrack ReID | dance_sbs_S50.pth |
| MOT17/20 validation ReID | osnet_ain_ms_d_c.pth.tar |

Use the exact authorized checkpoints from the original experiments. See [Deep-OC-SORT](https://github.com/GerardMaggiolino/Deep-OC-SORT), [OC-SORT](https://github.com/noahcao/OC_SORT), and [ByteTrack](https://github.com/ifzhang/ByteTrack) for upstream resources. Exact checkpoint URLs and checksums have not been confirmed. Some detection caches are included, but their completeness and suitability for each split are unverified.

## Tracking and trajectory completion

The following examples use arguments present in the source. They are entry-point examples, not verified commands for reproducing the manuscript tables.

```bash
python main.py --help
python main.py --dataset mot17 --exp_name mot17_example --asso hmiou
python main.py --dataset mot20 --exp_name mot20_example --asso hmiou
python main.py --dataset dance --exp_name dance_example --asso hmiou
```

Use `--test_dataset` for the test split. The confidence-association cost can be enabled with `--tcm_weight`; the exact dataset-specific experimental value must be confirmed. By default, the entry point uses ordinary IoU and does not enable this cost. The `--post` flag calls conventional DTI, not DWLI.

For standalone DWLI, pass the experiment directory containing the tracking output `data/` subdirectory:

```bash
python trackers/strong_ocsort/interpolation/DWLI.py --help
python trackers/strong_ocsort/interpolation/DWLI.py --input_dir results/trackers/MOT17-val/mot17_example
```

The script writes an adjacent experiment directory with the suffix `_dwli`. The default minimum trajectory length is 30 and default interpolation gap is 20; these are source defaults, not confirmation of the reported paper configuration. DWLI fills missing frames using observations on both sides of a gap and is a separate trajectory-completion step.

## Evaluation

TrackEval is available in `external/TrackEval/`. Consult its [documentation](external/TrackEval/Readme.md) and run:

```bash
python external/TrackEval/scripts/run_mot_challenge.py --help
```

Provide the appropriate ground-truth directory, sequence map, benchmark split, and tracker output directory. Exact evaluation commands and full-method parameters for the manuscript tables are pending verification. Test-set evaluation may require the corresponding benchmark evaluation service.

## Known limitations and reproducibility status

- The source tree is accessible, but end-to-end reproduction has not been verified from a clean environment.
- Exact detector/ReID checkpoint sources, annotation conversion, full method configuration (including PDA), and table-specific evaluation commands still require confirmation.
- The entry points contain local visualization paths and development variants. Do not assume every variant represents the final paper method.
- The manuscript contains the reported benchmark results. No new results have been generated or independently validated by this documentation update.

## Attribution and archive

The earlier project documentation referenced https://github.com/fei528/sy-dwli-wcf and Zenodo DOI https://doi.org/10.5281/zenodo.17837164. These references are retained for provenance; their precise relationship to this checkout and archive contents still require verification.

This project acknowledges [Deep-OC-SORT](https://github.com/GerardMaggiolino/Deep-OC-SORT), [OC-SORT](https://github.com/noahcao/OC_SORT), [ByteTrack](https://github.com/ifzhang/ByteTrack), [YOLOX](https://github.com/Megvii-BaseDetection/YOLOX), and TrackEval. Respect the included licenses and third-party resource terms.

If you use the research code, please cite the corresponding manuscript once published.
