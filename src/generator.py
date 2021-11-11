import argparse
from pathlib import Path
from template import Template

from spec import parse_spec


def spec_file(spath: str):
    p = Path(spath)
    if not p.is_file():
        raise ValueError
    return p


def out_file(spath: str):
    p = Path(spath)
    if p.exists():
        raise argparse.ArgumentError(None, "Output file exists")

    if not p.parent.is_dir():
        raise argparse.ArgumentError(None, "Cannot put output here")
    return p


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Create PaperPlay tokens")
    parser.add_argument('spec', type=spec_file, help='path to specification')
    parser.add_argument('output', type=out_file,
                        help='path to output file', default='tokens.pdf', nargs='?')
    parser.add_argument('--size', type=float,
                        help='side length of cards in mm', default=60)
    parser.add_argument('--margin', type=float,
                        help='minimal page margin', default=3)
    parser.add_argument('--img-padding', type=float,
                        help='Paddingn of images in mm', default=1)
    parser.add_argument('--qr-padding', type=float,
                        help='Padding of QR-codes', default=3)
    parser.add_argument(
        '--multiple-qrs', help='Multuple QR codes per card', action='count', default=1)
    return parser


if __name__ == "__main__":
    args = create_arg_parser().parse_args()
    cards = parse_spec(args.spec)
    template = Template(
        args.spec.parent,
        args.size,
        args.margin,
        args.qr_padding,
        args.img_padding,
        args.multiple_qrs)

    with args.output.open('wb') as f:
        template.make_tokens(cards, f)
