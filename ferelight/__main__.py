#!/usr/bin/env python3
import argparse
import json

import connexion
from flask import current_app

from ferelight import encoder


def add_cors_headers(response):
    """Add CORS headers to the response if enabled in the configuration."""
    cors_config = current_app.config.get('CORS', {})

    if cors_config.get('ENABLED', False):
        response.headers['Access-Control-Allow-Origin'] = cors_config.get('ALLOW_ORIGIN', '*')
        response.headers['Access-Control-Allow-Methods'] = cors_config.get('ALLOW_METHODS', 'GET, POST, OPTIONS')
        response.headers['Access-Control-Allow-Headers'] = cors_config.get('ALLOW_HEADERS', 'Content-Type, Authorization')

    return response


def handle_options_request():
    """Handle OPTIONS requests for CORS preflight."""
    response = current_app.make_default_options_response()
    add_cors_headers(response)
    return response


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

    # Register CORS-related handlers
    app.app.after_request(add_cors_headers)
    app.app.route('/<path:path>', methods=['OPTIONS'])(handle_options_request)
    app.app.route('/', methods=['OPTIONS'])(handle_options_request)

    app.run(port=8080)


if __name__ == '__main__':
    main()
