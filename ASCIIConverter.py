import argparse
import video_converter as vc
import photo_converter as pc

def main():
    parser = argparse.ArgumentParser(
        description='Image to ASCII art',
        epilog='Enjoy ;)'
    )

    parser.add_argument(
        'path',
        type=str,
        help='Input direction for image'
    )
    parser.add_argument(
        '-s',
        '--show_result',
        action='store_true',
        help='show result in new window'
    )
    parser.add_argument(
        '-i',
        '--inversion',
        action='store_true',
        help='invert image'
    )
    parser.add_argument(
        '-f',
        '--filename',
        default='ascii.txt',
        help='the name of the file to create. (default: ascii.txt)'
    )
    parser.add_argument(
        '-o',
        '--outdir',
        type=str,
        default='',
        help='output direction for ASCII art (default: executable directory)'
    )

    args = parser.parse_args()

    if args.path.endswith('.mp4'):
        vc.convert(args)
    else:
        pc.convert(args)

main()