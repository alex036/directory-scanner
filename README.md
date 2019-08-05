# Directory Scanner
Provided with an input path and a log location, this script will output changes to the directory structure.

The first time the script is run, it generates a baseline file (`baseline_file.csv`). Every subsequent run it compares the current file structure against the baseline.
#### Log Output
Log file will be placed in `/logdir/scan_log.log` as well as output to the stdout.
 - Deleted
	 - `D <base filename>`
- New File
	- `N <new filename> <new size in bytes>`
- Updated
	- `U <base filename> <base size in bytes> <new size in bytes>`
- Moved
	- `M <base file> <new file>`

The log file will also output some stats at the end, for example:
```
Total files scanned: 10
Total files modified: 5
```
## Docker
The docker container **requires** two volumes to be mapped. Example is given in the run section.

 - `/scandir` - The script will start scanning at this location. This needs to be mapped to the 'root' of where you want to scan.
	 - eg
		 - `/home/user:/scandir`
		 - `/usr/bin:/scandir`
 - `/logdir` - The script will log to this location. Map this to where you want to place logfiles.
	 - eg
		 - `/home/user/scan-logs:/logdir`
		 - `/var/log:/logdir`

### Build
`sudo docker build -t directory-scanner .`
### Run
Example:
```
sudo docker run -v /home/alex/Development/directory-testing:/scandir \
                -v /home/alex/Development/directory-logs:/logdir \
                directory-scanner

```
