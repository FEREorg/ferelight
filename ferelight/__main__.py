#!/usr/bin/env python3
import json

import connexion

from ferelight import encoder


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'FERElight'},
                pythonic_params=True)
    app.app.config.from_file('../config.json', load=json.load)

    app.run(port=8080)


if __name__ == '__main__':
    main()
