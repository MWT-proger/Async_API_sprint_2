import json


def raw_data_to_es(raw_data: list, index: str) -> list:
    data = []
    for row in raw_data:
        data.extend(
            [
                json.dumps(
                    {
                        'index': {
                            '_index': index,
                            '_id': row['id']
                        }
                    }
                ),
                json.dumps(row),
            ]
        )
    return data
