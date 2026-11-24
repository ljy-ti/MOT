import numpy as np
import glob
import os
import argparse


def interpolate_bbox_refined(left_bbox, right_bbox, left_frame, right_frame, curr_frame, gap_size=None):
    """
    Dynamic-weight interpolation
    Retain the core of the original algorithm with minor refinements
    """
    alpha = (curr_frame - left_frame) / (right_frame - left_frame)
    delta = right_bbox - left_bbox

    # Changes in width and height
    delta_w = abs(delta[2])
    delta_h = abs(delta[3])
    eps = 1e-6

    # Original weight calculation
    w_weight = delta_w / (delta_w + delta_h + eps)
    h_weight = delta_h / (delta_w + delta_h + eps)

    # The only refinement is weight decay for large gaps
    if gap_size and gap_size > 10:
        # For larger gaps, weights approach 0.5 (more conservative)
        decay_factor = min(1.0, 10.0 / gap_size)
        w_weight = 0.5 + (w_weight - 0.5) * decay_factor
        h_weight = 0.5 + (h_weight - 0.5) * decay_factor

    # Weight vector
    weights = np.array([1.0, 1.0, w_weight, h_weight])

    # Interpolation
    curr_bbox = left_bbox + weights * alpha * delta
    return curr_bbox


def DWLI(txt_path, save_path, n_min=30, n_dti=20, gap_threshold=None):
    """
    Main DTI function
    Retain most of the original code with a small gap-dependent adjustment
    """
    seq_txts = sorted(glob.glob(os.path.join(txt_path, "*.txt")))
    os.makedirs(save_path, exist_ok=True)

    total_files = len(seq_txts)
    print(f"Processing {total_files} files...")
    if gap_threshold:
        print(f"Using gap threshold: {gap_threshold}")

    for file_idx, seq_txt in enumerate(seq_txts):
        seq_name = os.path.basename(seq_txt)
        print(f"\rProgress: [{file_idx+1}/{total_files}] {seq_name}", end="", flush=True)

        seq_data = np.loadtxt(seq_txt, dtype=np.float64, delimiter=",")
        min_id = int(np.min(seq_data[:, 1]))
        max_id = int(np.max(seq_data[:, 1]))
        seq_results = []

        for track_id in range(min_id, max_id + 1):
            index = seq_data[:, 1] == track_id
            tracklet = seq_data[index]
            if tracklet.shape[0] == 0:
                continue
            n_frame = tracklet.shape[0]
            if n_frame <= n_min:
                continue
            tracklet = tracklet[tracklet[:, 0].argsort()]
            frames = tracklet[:, 0]
            frames_dti = {}

            for i in range(1, n_frame):
                left_frame = int(frames[i - 1])
                right_frame = int(frames[i])
                gap = right_frame - left_frame

                # Use the gap threshold if provided
                max_gap = gap_threshold if gap_threshold else n_dti

                if 1 < gap < max_gap:
                    left_bbox = tracklet[i - 1, 2:6]
                    right_bbox = tracklet[i, 2:6]
                    for j in range(1, gap):
                        curr_frame = left_frame + j
                        curr_bbox = interpolate_bbox_refined(
                            left_bbox, right_bbox, left_frame, right_frame, curr_frame, gap
                        )
                        frames_dti[curr_frame] = curr_bbox

            # Fill missing frames by interpolation
            if frames_dti:
                data_dti = np.zeros((len(frames_dti), 10), dtype=np.float64)
                for idx, (f, box) in enumerate(frames_dti.items()):
                    data_dti[idx, 0] = f
                    data_dti[idx, 1] = track_id
                    data_dti[idx, 2:6] = box
                    data_dti[idx, 6:] = [1, -1, -1, -1]
                tracklet = np.vstack((tracklet, data_dti))
            seq_results.append(tracklet)

        # Merge and save
        if seq_results:
            all_results = np.vstack(seq_results)
            all_results = all_results[all_results[:, 0].argsort()]
            save_seq_txt = os.path.join(save_path, seq_name)
            dti_write_results(save_seq_txt, all_results)

    print(f"\nFinished processing {total_files} files")


def dti_write_results(filename, results):
    save_format = "{frame},{id},{x1},{y1},{w},{h},{s},-1,-1,-1\n"
    with open(filename, "w") as f:
        for row in results:
            frame_id, track_id, x1, y1, w, h = row[:6]
            line = save_format.format(frame=int(frame_id), id=int(track_id), x1=x1, y1=y1, w=w, h=h, s=-1)
            f.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic-weight linear interpolation")

    parser.add_argument("--input_dir", type=str, required=True, help="Input directory path")
    parser.add_argument("--n_min", type=int, default=30, help="Minimum trajectory length (default: 30)")
    parser.add_argument("--n_dti", type=int, default=20, help="Maximum interpolation gap (default: 20)")
    parser.add_argument("--gap_threshold", type=int, default=None, help="Custom gap threshold for DanceTrack")

    args = parser.parse_args()

    base_input_dir = args.input_dir
    input_dir = os.path.join(base_input_dir, "data")

    dir_name = os.path.basename(base_input_dir)
    parent_dir = os.path.dirname(base_input_dir)
    output_dir_name = f"{dir_name}_dwli"
    output_dir = os.path.join(parent_dir, output_dir_name, "data")

    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")

    os.makedirs(os.path.dirname(output_dir), exist_ok=True)

    DWLI(input_dir, output_dir, args.n_min, args.n_dti, args.gap_threshold)
