#!/usr/bin/env python3
# =========================================================
# Convert AOI GeoTIFF raster to labeled text matrix
# - Pure Python (CLI-friendly), works in Colab or locally
# - Values: 0=outside, 1=inside, 2=boundary (from GEE script)
# - Writes each raster row as concatenated digits + latitude
#   and a bottom line of longitude labels at chosen spacing.
# =========================================================

import argparse
import sys
from pathlib import Path

try:
    import rasterio
except Exception as e:
    print('ERROR: rasterio is not installed. Install with: pip install rasterio', file=sys.stderr)
    raise

import numpy as np
from affine import Affine

def convert_to_matrix(input_path: Path, output_path: Path, label_every_n_cols: int = 10, round_decimals: int = 3) -> None:
    with rasterio.open(input_path) as src:
        matrix = src.read(1).astype(int)
        transform: Affine = src.transform
        width, height = src.width, src.height

    # coordinate arrays at pixel upper-left
    cols = np.arange(width)
    rows = np.arange(height)
    longitudes = np.array([(transform * (int(c), 0))[0] for c in cols])
    latitudes  = np.array([(transform * (0, int(r)))[1] for r in rows])

    lon_fmt = np.round(longitudes, round_decimals)
    lat_fmt = np.round(latitudes, round_decimals)

    # write text matrix
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for r in range(height):
            row_vals = matrix[r, :]
            # note: if class values exceed single digit, switch to space-separated output
            row_str = ''.join(str(int(v)) for v in row_vals)
            f.write(f"{row_str} {lat_fmt[r]:>12}\n")
        f.write('\n')

        # bottom line of longitude labels
        bottom_line = []
        for c in range(width):
            if c % label_every_n_cols == 0:
                lab = f"{lon_fmt[c]:.{round_decimals}f}"
                block = max(label_every_n_cols, len(lab))
                bottom_line.append(lab.rjust(block))
            else:
                bottom_line.append(' ')
        f.write(''.join(bottom_line) + '\n')

def main():
    parser = argparse.ArgumentParser(
        description='Convert AOI GeoTIFF raster (0/1/2) into a labeled text matrix.'
    )
    parser.add_argument('--input', '-i', type=Path, required=True, help='Path to input GeoTIFF (.tif) exported from GEE')
    parser.add_argument('--output', '-o', type=Path, required=True, help='Path to output text file (.txt)')
    parser.add_argument('--label-every-n-cols', type=int, default=10, help='Label every Nth longitude column (default: 10)')
    parser.add_argument('--round-decimals', type=int, default=3, help='Rounding for lat/lon labels (default: 3)')
    args = parser.parse_args()

    try:
        convert_to_matrix(
            input_path=args.input,
            output_path=args.output,
            label_every_n_cols=args.label_every_n_cols,
            round_decimals=args.round_decimals
        )
        print(f'✅ Wrote matrix to: {args.output}')
    except FileNotFoundError:
        print('ERROR: Input file not found. Double-check the --input path.', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
