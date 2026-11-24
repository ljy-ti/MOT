# Dependency notes

This is an inventory of dependencies visible in the project and bundled upstream requirements, not an exact locked or tested reproduction environment.

## Core runtime

The main tracking path imports NumPy, SciPy, OpenCV, PyTorch, torchvision, pycocotools, scikit-learn, FilterPy, torchreid, YOLOX and FastReID. The association code optionally uses LAP; SciPy is the fallback. A CUDA-capable GPU is expected by detector and ReID code.

```bash
# Create a clean environment, then install a mutually compatible
# PyTorch/torchvision/CUDA combination using the official PyTorch instructions:
# https://pytorch.org/get-started/locally/
python -m pip install -r requirements.txt
```

The original README listed Python 3.8+, PyTorch 1.10.1 and CUDA 11.3/11.8 as reference versions. Compatibility is not confirmed. The source uses the legacy `np.int` alias (removed in NumPy 1.24) and a `torch.load(..., weights_only=False)` call; select compatible versions and verify the installed API before running experiments. Do not treat the reference versions as a validated lockfile.

## Bundled libraries

Consult the upstream files before installation; some versions are historical and may conflict with newer packages.

| Component | Dependency file |
| --- | --- |
| YOLOX | [external/YOLOX/requirements.txt](external/YOLOX/requirements.txt) |
| Deep person re-identification | [external/deep-person-reid/requirements.txt](external/deep-person-reid/requirements.txt) |
| FastReID | [external/fast_reid/docs/requirements.txt](external/fast_reid/docs/requirements.txt) |
| TrackEval | [external/TrackEval/requirements.txt](external/TrackEval/requirements.txt) |

Install the bundled YOLOX and deep-person-reid packages using their setup instructions and ensure that `yolox`, `torchreid`, and `fast_reid.fastreid` are importable. The supplied root `setup.py` contains a local YOLOX installation helper, but it is not a complete environment setup. Do not assume all legacy requirements can be installed together without resolving conflicts.

For tracking, the model checkpoints and prepared COCO-style annotations described in the [README](README.md) are also needed. Cached detections are not a replacement for verified dependencies or complete checkpoint availability.

No installation or benchmark run was performed as part of this documentation update.
