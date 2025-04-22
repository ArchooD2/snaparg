from snaparg import SnapArgumentParser

def main():
    parser = SnapArgumentParser(description="SnapArg demo script")
    parser.add_argument('--input', '-i', help='Input file')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite')

    args, unknown = parser.parse_known_args()
    if unknown:
        parser.error(f"unrecognized arguments: {' '.join(unknown)}")

    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Force: {args.force}")

if __name__ == "__main__":
    main()
