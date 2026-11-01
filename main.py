import socket
import argparse
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Set up command-line argument parsing.
    """
    parser = argparse.ArgumentParser(description="Map open ports and running services on a given host and port range.")
    parser.add_argument('host', type=str, help="Target host to scan (e.g., '127.0.0.1' or 'example.com').")
    parser.add_argument('--start-port', type=int, default=1, help="Starting port number for the scan (default: 1).")
    parser.add_argument('--end-port', type=int, default=1024, help="Ending port number for the scan (default: 1024).")
    return parser.parse_args()

def scan_port(host, port):
    """
    Check if a port is open on the given host.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set timeout for connection attempt
            # connect_ex folds every failure into a nonzero code that I never look at past the zero test. A refused connection, an unreachable host, and a filtered port that times out are all reported the same way: silence.
            result = s.connect_ex((host, port))
            if result == 0:  # Port is open
                # If this lookup raises OSError for an open port with no registered service name, the handlers below catch it and I return None for the port. The port was open, but it reaches main as if it were closed, and nothing in the output separates the two cases.
                service = socket.getservbyport(port, 'tcp') if port <= 65535 else 'Unknown'
                return port, service
    except socket.error as e:
        logging.error(f"Socket error on port {port}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error on port {port}: {e}")
    return None, None

def main():
    """
    Main function to handle the scanning process.
    """
    args = setup_argparse()
    host = args.host
    start_port = args.start_port
    end_port = args.end_port

    if not (1 <= start_port <= 65535) or not (1 <= end_port <= 65535) or start_port > end_port:
        logging.error("Invalid port range: start and end ports must each be within 1 to 65535, and start must not exceed end.")
        sys.exit(1)

    logging.info(f"Starting scan on host: {host} from port {start_port} to {end_port}")
    
    try:
        # I scan one port at a time and each attempt can sit for the full one second timeout, so a filtered host over the default range can hold this loop for close to seventeen minutes with no progress output between the start line and the finish line.
        for port in range(start_port, end_port + 1):
            # Reusing the name port for the result is safe only because range already handed me the next value. It also means a None result erases the number I just scanned, so the log line inside scan_port is the only place a failed port number survives.
            port, service = scan_port(host, port)
            if port:
                logging.info(f"Open port found: {port} (Service: {service})")
    except KeyboardInterrupt:
        logging.warning("Scan interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred during the scan: {e}")
    finally:
        logging.info("Scan completed.")

# Usage example:
# To scan localhost ports 1 through 1024, run the following:
# python main.py 127.0.0.1 --start-port 1 --end-port 1024
if __name__ == "__main__":
    main()