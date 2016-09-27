# helpers
import wmi


def get_service_alive_info(service_name):
    '''
    get info that is service alive
    '''
    wmi_conn = wmi.WMI()
    proc_list = wmi_conn.Win32_Service(Name=service_name)
    return '1' if len(proc_list) != 0 else '0'
    