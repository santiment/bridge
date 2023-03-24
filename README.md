# Bridge Transaction Exporter
The liquidation repo contains exporters related with bridges.

This exporter provides a simple interface for exporting transactions of bridges from the current network to the destination network. The transaction data would be save in `bridge_transactions` table.


## Commands
- `PLATFORM: wbtc`
- `./bin/run.sh PLATFORM` - to run parsing events (e.g. `./bin/run.sh wbtc` )
- `./bin/test.sh` - to run tests
- Environment variables: `START_DT`, `END_DT`


## Add a new exporter
To add a new exporter you can use the example template as a general guideline. 
