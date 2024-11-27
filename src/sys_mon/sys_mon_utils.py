import psutil
import time
from simple_log_factory.log_factory import log_factory

from sys_mon.sys_stat_response import SysStats
from utils.env import LOCAL_DISK_PATH, NAS_PATH

_logger = log_factory("sys_mon_utils")

# Initialize last sent times
_last_sent_storage_total = None
_last_sent_nas_total = None
_current_time = None
_net_io_last = None
_current_server_status = None


def _get_disk_usage(path):
    _logger.debug("Getting disk usage")
    usage = psutil.disk_usage(path)
    return usage.used / (1024 ** 3), usage.total / (1024 ** 3)  # Convert to GB


def get_system_status():
    global _logger
    global _last_sent_storage_total
    global _last_sent_nas_total
    global _current_time
    global _net_io_last
    global _current_server_status
    _logger.debug("Getting system status")

    try:
        if _current_server_status is None:
            _current_server_status = SysStats()

        _net_io_last = psutil.net_io_counters()
        time.sleep(5)  # Wait a bit to let the network usage "settle"

        _current_time = time.time()

        _logger.debug("Setting CPU usage")
        _current_server_status.update_cpu_percent(psutil.cpu_percent())

        mem = psutil.virtual_memory()
        _logger.debug("Setting memory usage")
        _current_server_status.update_mem_used(mem.used)

        _logger.debug("Getting network usage")
        net_io_current = psutil.net_io_counters()

        _logger.debug("Setting network usage - upload")
        upload_rate = net_io_current.bytes_sent - _net_io_last.bytes_sent
        _current_server_status.update_net_upload(upload_rate)

        _logger.debug("Setting network usage - download")
        download_rate = net_io_current.bytes_recv - _net_io_last.bytes_recv
        _current_server_status.update_net_download(download_rate)

        _net_io_last = net_io_current

        # Update data every 10 minutes
        if _last_sent_storage_total is None or _current_time - _last_sent_storage_total >= 600:
            _logger.debug("Setting local storage usage")
            _current_server_status.update_storage_used(_get_disk_usage(LOCAL_DISK_PATH)[0])

            _logger.debug("Setting NAS usage")
            _current_server_status.update_nas_used(_get_disk_usage(NAS_PATH)[0])

            _last_sent_storage_total = _current_time

        # Update data every 24 hours
        if _last_sent_nas_total is None or _current_time - _last_sent_nas_total >= 86400:
            _logger.debug("Setting total local storage")
            _current_server_status.update_storage_total(_get_disk_usage(LOCAL_DISK_PATH)[1])

            _logger.debug("Setting total NAS")
            _current_server_status.update_nas_total(_get_disk_usage(NAS_PATH)[1])

            _logger.debug("Setting total memory")
            _current_server_status.update_mem_total(mem.total)

            _last_sent_nas_total = _current_time

        return _current_server_status.to_dict()

    except Exception as e:
        _logger.exception(f"Error while getting system status: {e}")
        return None
