import os
import threading
import server
import clients.desktop
import sys

# Set '01_PORT' if it's not already set
if '01_PORT' not in os.environ:
    os.environ['01_PORT'] = '10000'

# Check if --server argument is passed
if '--server' in sys.argv:
    # Create and run server thread only
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
    server_thread.join()
else:
    # Create threads for server and client
    server_thread = threading.Thread(target=server.run)
    client_thread = threading.Thread(target=clients.desktop.run)

    # Start and wait for the threads
    server_thread.start()
    client_thread.start()
    server_thread.join()
    client_thread.join()
