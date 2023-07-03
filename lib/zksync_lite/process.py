# This file will contain the processing logic for the zksync_lite exporter.
# It will be similar to the process.py file in the zksync_era_bridge exporter.
# Please update this file based on the specific requirements of the zksync_lite exporter.
def process(project_name, records):
    """
    Process the records for the zksync_lite exporter.
    """
    events = []
    for record in records:
        event = build_event(record)
        events.append(event)

    return events

def build_event(record):
    """
    Build an event from a record.
    """
    event = {
        'tx_hash': record['tx_hash'],
        'contract_addr': record['contract_addr'],
        'args': record['args'],
        'dt': record['dt'],
        'log_index': record['log_index'],
        'action': record['action'],
    }

    if event['action'] == 'deposit':
        event['tokenId'] = record['args']['tokenId']
        event['amount'] = record['args']['amount']

    return event
