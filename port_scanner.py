import socket
import common_ports

def get_open_ports(target, port_range, verbose = False):
    # check if target is url or ip
    try:
        float(target[0])
    except ValueError:
        target_type = 'url'
    else:
        target_type = 'ip'


    # check target validity
    try:
        host = socket.gethostbyname(target)
    except:
        if target_type == 'url':
            return "Error: Invalid hostname"
        else:
            return "Error: Invalid IP address"

    #create list of all ports
    ports = range(port_range[0], port_range[1] + 1)

    # check each port if open
    open_ports = []
    for port in ports:
        # create socket + timeout
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        # add to list if open
        if s.connect_ex((host, port)):
            pass
        else:
            open_ports.append(port)
        
        # close port
        s.close()

    # return open ports if not verbose
    if not verbose:
        return(open_ports)

    # create verbose string
    if target_type == 'url':
        verbose_string = f'Open ports for {target} ({host})\nPORT     SERVICE'
    else:
        verbose_string = f'Open ports for {target}\nPORT     SERVICE'

    # adding ports to string
    for port in open_ports:
        # finding service
        service = common_ports.ports_and_services[port]
        verbose_string += f'\n{port}{' ' * 9 - len(str(port))}{service}'

    return(verbose_string)
