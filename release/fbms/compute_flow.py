import argparse
import logging
import pprint
import subprocess
import yaml
from pathlib import Path

from script_utils.common import common_setup

from release.helpers.flow import compute_flow_helper


def main():
    # Use first line of file docstring as description if it exists.
    parser = argparse.ArgumentParser(
        description=__doc__.split('\n')[0] if __doc__ else '',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--config', default=Path('./release/config.yaml'))

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.load(f)

    output_dir = Path(config['fbms']['output_dir']) / 'flow'
    output_dir.mkdir(exist_ok=True, parents=True)

    common_setup(__file__, output_dir, args)
    logging.debug('Config:\n%s', pprint.pformat(config))

    for split in config['fbms']['splits']:
        input_dir = config['fbms']['images_highres'][split]
        output_split = output_dir / split
        logging.info("\n\n###\n"
                     "Computing flow on FBMS %s set.\n"
                     "###\n\n", split)
        compute_flow_helper(config,
                            input_dir,
                            output_split,
                            extensions=['.png'])


if __name__ == "__main__":
    main()