class SysStats(object):
    def __init__(self):
        self._cpu_percent = None
        self._mem_used = None
        self._mem_total = None
        self._storage_used = None
        self._storage_total = None
        self._nas_used = None
        self._nas_total = None
        self._net_upload = None
        self._net_download = None

    def to_dict(self):
        return {
            "cpu_percent": self._cpu_percent,
            "mem_used": self._mem_used,
            "mem_total": self._mem_total,
            "storage_used": self._storage_used,
            "storage_total": self._storage_total,
            "nas_used": self._nas_used,
            "nas_total": self._nas_total,
            "net_upload": self._net_upload,
            "net_download": self._net_download
        }

    @staticmethod
    def _can_update_value(value):
        return value is not None and value != 0

    @staticmethod
    def _convert_value_to_gb(value):
        return value / (1024 ** 3)

    def update_cpu_percent(self, cpu_percent):
        if not self._can_update_value(cpu_percent):
            return
        self._cpu_percent = cpu_percent

    def update_mem_used(self, mem_used):
        if not self._can_update_value(mem_used):
            return
        self._mem_used = self._convert_value_to_gb(mem_used)

    def update_mem_total(self, mem_total):
        if not self._can_update_value(mem_total):
            return
        self._mem_total = self._convert_value_to_gb(mem_total)

    def update_storage_used(self, storage_used):
        if storage_used is None or storage_used == 0:
            return
        self._storage_used = storage_used

    def update_storage_total(self, storage_total):
        if storage_total is None or storage_total == 0:
            return
        self._storage_total = storage_total

    def update_nas_used(self, nas_used):
        if nas_used is None or nas_used == 0:
            return
        self._nas_used = nas_used

    def update_nas_total(self, nas_total):
        if nas_total is None or nas_total == 0:
            return
        self._nas_total = nas_total

    def update_net_upload(self, net_upload):
        if net_upload is None or net_upload == 0:
            return
        self._net_upload = net_upload

    def update_net_download(self, net_download):
        if net_download is None or net_download == 0:
            return
        self._net_download = net_download
