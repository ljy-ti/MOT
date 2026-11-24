# Enhancing Multi-Object Tracking via Dynamic-Weight Linear Interpolation and Weak Clue Fusion

This repository contains research code associated with the manuscript of the same title.

- [Project documentation and run instructions](sy-dwli-wcf-main/sy-dwli-wcf-main/README.md)
- [Dependency notes](sy-dwli-wcf-main/sy-dwli-wcf-main/DEPENDENCIES.md)
- [Core tracker implementation](sy-dwli-wcf-main/sy-dwli-wcf-main/trackers/strong_ocsort/)
- [DWLI trajectory interpolation](sy-dwli-wcf-main/sy-dwli-wcf-main/trackers/strong_ocsort/interpolation/DWLI.py)

The working project is located in the nested directory shown below:

```bash
git clone https://github.com/LJY-TI/MOT.git
cd MOT/sy-dwli-wcf-main/sy-dwli-wcf-main
```

The repository includes tracking and evaluation code, development variants, and some cached detections. The full paper experiments have not been independently reproduced from this public checkout. See the project documentation for prerequisites, known limitations, and the remaining verification steps.
