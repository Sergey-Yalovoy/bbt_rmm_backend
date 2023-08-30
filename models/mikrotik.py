import ssl
from pydantic import ConfigDict
from controllers.mongo_controller import MongoDBModel
from routeros_api.api import RouterOsApiPool


class MikrotikRouter(MongoDBModel):
    host: str
    username: str
    password: str

    class Meta:
        collection_name = 'mikrotik_routers'

    def connect(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.set_ciphers("ADH:ALL:@SECLEVEL=0")
        connection = RouterOsApiPool(self.host, username=self.username, password=self.password,
                                     use_ssl=True, ssl_verify=True, plaintext_login=True,
                                     ssl_verify_hostname=True, ssl_context=ssl_context)
        return connection


def to_sneak(string: str) -> str:
    return string.replace('-', '_')


class Script(MongoDBModel):
    model_config = ConfigDict(alias_generator=to_sneak)
    name: str
    owner: str
    policy: str
    dont_require_permissions: str
    run_count: int
    source: str
    invalid: str