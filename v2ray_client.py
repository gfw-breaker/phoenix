import os
import sys

sys.path.append(os.path.dirname(__file__))
from grpc._channel import _Rendezvous
from errors import *
from config import *
from v2ray.com.core.common.net import port_pb2, address_pb2
from v2ray.com.core import config_pb2 as core_config_pb2
from v2ray.com.core.proxy.vmess import account_pb2
from v2ray.com.core.proxy.vmess.inbound import config_pb2 as vmess_inbound_config_pb2
from v2ray.com.core.common.protocol import user_pb2
from v2ray.com.core.common.serial import typed_message_pb2
from v2ray.com.core.app.proxyman import config_pb2 as proxyman_config_pb2
from v2ray.com.core.app.proxyman.command import command_pb2
from v2ray.com.core.app.proxyman.command import command_pb2_grpc
from v2ray.com.core.app.stats.command import command_pb2 as stats_command_pb2
from v2ray.com.core.app.stats.command import command_pb2_grpc as stats_command_pb2_grpc
from v2ray.com.core.proxy.shadowsocks import config_pb2 as shadowsocks_server_config_pb2
from v2ray.com.core.transport.internet.headers.wechat import config_pb2 as header_wechat_config_pb2
from v2ray.com.core.transport.internet.headers.srtp import config_pb2 as header_srtp_config_pb2
from v2ray.com.core.transport.internet.headers.utp import config_pb2 as header_utp_config_pb2
from v2ray.com.core.transport.internet.headers.wireguard import config_pb2 as header_wiregurad_config_pb2
from v2ray.com.core.transport.internet.kcp import config_pb2 as kcp_config_pb2
from v2ray.com.core.transport.internet.headers.tls import config_pb2 as header_tls_config_pb2
from v2ray.com.core.transport.internet.headers.noop import config_pb2 as header_noop_config_pb2

import v2ray.com.core.transport.internet.config_pb2 as internet_config_pb2
import v2ray.com.core.transport.internet as internet


from v2ray.com.core.transport.internet.websocket import config_pb2 as websocket_config_pb2
import uuid
import grpc
kcp_headers_config = {"wechat-video":header_wechat_config_pb2.VideoConfig(),"srtp":header_srtp_config_pb2.Config(),
                      'utp':header_utp_config_pb2.Config(),
               'wireguard':header_wiregurad_config_pb2.WireguardConfig(),
                      'dtls':header_tls_config_pb2.PacketConfig(),
                      "noop":header_noop_config_pb2.Config()}

def to_typed_message(message):
    return typed_message_pb2.TypedMessage(
        type=message.DESCRIPTOR.full_name,
        value=message.SerializeToString()
    )


def ip2bytes(ip: str):
    return bytes([int(i) for i in ip.split('.')])


class Client(object):
    def __init__(self, address, port):
        print(f"{address}:{port}")
        self._channel = grpc.insecure_channel(f"{address}:{port}")


    def add_user(self, inbound_tag, user_id, email, level=0, alter_id=16):
        """
        在一个传入连接中添加一个用户（仅支持 VMess）
        若email已存在，抛出EmailExistsError异常
        若inbound_tag不存在，抛出InboundNotFoundError异常
        """
        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.AlterInbound(command_pb2.AlterInboundRequest(
                tag=inbound_tag,
                operation=to_typed_message(command_pb2.AddUserOperation(
                    user=user_pb2.User(
                        email=email,
                        level=level,
                        account=to_typed_message(account_pb2.Account(
                            id=user_id,
                            alter_id=alter_id
                        ))
                    )
                ))
            ))
            return user_id
        except _Rendezvous as e:
            details = e.details()
            if details.endswith(f"User {email} already exists."):
                raise EmailExistsError(details, email)
            elif details.endswith(f"handler not found: {inbound_tag}"):
                raise InboundNotFoundError(details, inbound_tag)
            else:
                raise V2RayError(details)

    def remove_user(self, inbound_tag, email):
        """
        在一个传入连接中删除一个用户（仅支持 VMess）
        需几分钟生效，因为仅仅是把用户从用户列表中移除，没有移除对应的auth session，
        需要等这些session超时后，这个用户才会无法认证
        若email不存在，抛出EmailNotFoundError异常
        若inbound_tag不存在，抛出InboundNotFoundError异常
        """
        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.AlterInbound(command_pb2.AlterInboundRequest(
                tag=inbound_tag,
                operation=to_typed_message(command_pb2.RemoveUserOperation(
                    email=email
                ))
            ))
        except _Rendezvous as e:
            details = e.details()
            if details.endswith(f"User {email} not found."):
                raise EmailNotFoundError(details, email)
            elif details.endswith(f"handler not found: {inbound_tag}"):
                raise InboundNotFoundError(details, inbound_tag)
            else:
                raise V2RayError(details)

