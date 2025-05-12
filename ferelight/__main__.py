#!/usr/bin/env python3
import argparse
import json

import connexion

from ferelight import encoder


def main():
    # Parse command-line arguments if called from entry point
    parser = argparse.ArgumentParser(description='Run the FERElight application')
    parser.add_argument('--config', '-c', default='../config.json',
                        help='Path to the configuration file (default: ../config.json)')
    args = parser.parse_args()
    config_path = args.config

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'FERElight'},
                pythonic_params=True)
    app.app.config.from_file(config_path, load=json.load)

    app.run(port=8080)


if __name__ == '__main__':
    main()
