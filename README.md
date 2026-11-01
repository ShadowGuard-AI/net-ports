## Net-Ports

### Project Description

Net-Ports is a cybersecurity tool designed to map open ports and identify running services on target systems. It provides a comprehensive view of the network environment and assists in detecting potential security vulnerabilities.

### Installation Instructions

Net-Ports is not published as a pip package. Clone the repository and run the tool from the cloned folder. No third-party packages are required: the tool uses only the Python standard library.

### Usage Examples

To use Net-Ports, open a terminal window in the cloned folder and type:

```Bash
python3 main.py target --start-port 1 --end-port 1024
```

Where:

* `target` is the IP address or hostname of the target system.
* `options` are additional command-line arguments (see below).

Common options include:

* `--start-port`: Starting port number for the scan (default: 1).
* `--end-port`: Ending port number for the scan (default: 1024).
* `-h`: Show help message and exit.

The start and end ports must each be within 1 to 65535, and the start must not exceed the end. An invalid range prints an error and exits 1 without scanning anything.

### Security Warnings

* Use Net-Ports responsibly and only with authorized targets.
* Scanning without permission may be considered a hacking attempt.
* Always adhere to ethical security practices and respect the privacy of others.

### License

GNU General Public License v3.0

This project is licensed to CY83R-3X71NC710N under the GNU General Public License v3.0.