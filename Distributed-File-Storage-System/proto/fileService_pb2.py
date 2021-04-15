# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fileService.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='fileService.proto',
  package='fileservice',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11\x66ileService.proto\x12\x0b\x66ileservice\"M\n\x08\x46ileData\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x0f\n\x07message\x18\x04 \x01(\t\"/\n\x08MetaData\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x11\n\tseqValues\x18\x02 \x01(\x0c\"\'\n\x03\x61\x63k\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1c\n\x08UserInfo\x12\x10\n\x08username\x18\x01 \x01(\t\".\n\x08\x46ileInfo\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\"%\n\x10\x46ileListResponse\x12\x11\n\tFilenames\x18\x01 \x01(\t\"<\n\x0b\x43lusterInfo\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\x12\x13\n\x0b\x63lusterName\x18\x03 \x01(\t\"\x07\n\x05\x45mpty\"G\n\x0c\x43lusterStats\x12\x11\n\tcpu_usage\x18\x01 \x01(\t\x12\x12\n\ndisk_space\x18\x02 \x01(\t\x12\x10\n\x08used_mem\x18\x03 \x01(\t2\xdf\x04\n\x0b\x46ileservice\x12\x35\n\nUploadFile\x12\x15.fileservice.FileData\x1a\x10.fileservice.ack\x12<\n\x0c\x44ownloadFile\x12\x15.fileservice.FileInfo\x1a\x15.fileservice.FileData\x12\x35\n\nFileSearch\x12\x15.fileservice.FileInfo\x1a\x10.fileservice.ack\x12:\n\rReplicateFile\x12\x15.fileservice.FileData\x1a\x10.fileservice.ack(\x01\x12@\n\x08\x46ileList\x12\x15.fileservice.UserInfo\x1a\x1d.fileservice.FileListResponse\x12\x35\n\nFileDelete\x12\x15.fileservice.FileInfo\x1a\x10.fileservice.ack\x12\x37\n\nUpdateFile\x12\x15.fileservice.FileData\x1a\x10.fileservice.ack(\x01\x12@\n\x0fgetClusterStats\x12\x12.fileservice.Empty\x1a\x19.fileservice.ClusterStats\x12;\n\rgetLeaderInfo\x12\x18.fileservice.ClusterInfo\x1a\x10.fileservice.ack\x12\x37\n\x0cMetaDataInfo\x12\x15.fileservice.MetaData\x1a\x10.fileservice.ackb\x06proto3'
)




_FILEDATA = _descriptor.Descriptor(
  name='FileData',
  full_name='fileservice.FileData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='fileservice.FileData.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filename', full_name='fileservice.FileData.filename', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='fileservice.FileData.data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='fileservice.FileData.message', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=34,
  serialized_end=111,
)


_METADATA = _descriptor.Descriptor(
  name='MetaData',
  full_name='fileservice.MetaData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='fileservice.MetaData.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='seqValues', full_name='fileservice.MetaData.seqValues', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=160,
)


_ACK = _descriptor.Descriptor(
  name='ack',
  full_name='fileservice.ack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='fileservice.ack.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='fileservice.ack.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=162,
  serialized_end=201,
)


_USERINFO = _descriptor.Descriptor(
  name='UserInfo',
  full_name='fileservice.UserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='fileservice.UserInfo.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=203,
  serialized_end=231,
)


_FILEINFO = _descriptor.Descriptor(
  name='FileInfo',
  full_name='fileservice.FileInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='fileservice.FileInfo.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filename', full_name='fileservice.FileInfo.filename', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=233,
  serialized_end=279,
)


_FILELISTRESPONSE = _descriptor.Descriptor(
  name='FileListResponse',
  full_name='fileservice.FileListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Filenames', full_name='fileservice.FileListResponse.Filenames', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=281,
  serialized_end=318,
)


_CLUSTERINFO = _descriptor.Descriptor(
  name='ClusterInfo',
  full_name='fileservice.ClusterInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='fileservice.ClusterInfo.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='fileservice.ClusterInfo.port', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clusterName', full_name='fileservice.ClusterInfo.clusterName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=320,
  serialized_end=380,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='fileservice.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=382,
  serialized_end=389,
)


_CLUSTERSTATS = _descriptor.Descriptor(
  name='ClusterStats',
  full_name='fileservice.ClusterStats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cpu_usage', full_name='fileservice.ClusterStats.cpu_usage', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='disk_space', full_name='fileservice.ClusterStats.disk_space', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='used_mem', full_name='fileservice.ClusterStats.used_mem', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=391,
  serialized_end=462,
)

DESCRIPTOR.message_types_by_name['FileData'] = _FILEDATA
DESCRIPTOR.message_types_by_name['MetaData'] = _METADATA
DESCRIPTOR.message_types_by_name['ack'] = _ACK
DESCRIPTOR.message_types_by_name['UserInfo'] = _USERINFO
DESCRIPTOR.message_types_by_name['FileInfo'] = _FILEINFO
DESCRIPTOR.message_types_by_name['FileListResponse'] = _FILELISTRESPONSE
DESCRIPTOR.message_types_by_name['ClusterInfo'] = _CLUSTERINFO
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['ClusterStats'] = _CLUSTERSTATS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FileData = _reflection.GeneratedProtocolMessageType('FileData', (_message.Message,), {
  'DESCRIPTOR' : _FILEDATA,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.FileData)
  })
_sym_db.RegisterMessage(FileData)

MetaData = _reflection.GeneratedProtocolMessageType('MetaData', (_message.Message,), {
  'DESCRIPTOR' : _METADATA,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.MetaData)
  })
_sym_db.RegisterMessage(MetaData)

ack = _reflection.GeneratedProtocolMessageType('ack', (_message.Message,), {
  'DESCRIPTOR' : _ACK,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.ack)
  })
_sym_db.RegisterMessage(ack)

UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), {
  'DESCRIPTOR' : _USERINFO,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.UserInfo)
  })
_sym_db.RegisterMessage(UserInfo)

FileInfo = _reflection.GeneratedProtocolMessageType('FileInfo', (_message.Message,), {
  'DESCRIPTOR' : _FILEINFO,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.FileInfo)
  })
_sym_db.RegisterMessage(FileInfo)

FileListResponse = _reflection.GeneratedProtocolMessageType('FileListResponse', (_message.Message,), {
  'DESCRIPTOR' : _FILELISTRESPONSE,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.FileListResponse)
  })
_sym_db.RegisterMessage(FileListResponse)

ClusterInfo = _reflection.GeneratedProtocolMessageType('ClusterInfo', (_message.Message,), {
  'DESCRIPTOR' : _CLUSTERINFO,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.ClusterInfo)
  })
_sym_db.RegisterMessage(ClusterInfo)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.Empty)
  })
_sym_db.RegisterMessage(Empty)

ClusterStats = _reflection.GeneratedProtocolMessageType('ClusterStats', (_message.Message,), {
  'DESCRIPTOR' : _CLUSTERSTATS,
  '__module__' : 'fileService_pb2'
  # @@protoc_insertion_point(class_scope:fileservice.ClusterStats)
  })
_sym_db.RegisterMessage(ClusterStats)



_FILESERVICE = _descriptor.ServiceDescriptor(
  name='Fileservice',
  full_name='fileservice.Fileservice',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=465,
  serialized_end=1072,
  methods=[
  _descriptor.MethodDescriptor(
    name='UploadFile',
    full_name='fileservice.Fileservice.UploadFile',
    index=0,
    containing_service=None,
    input_type=_FILEDATA,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DownloadFile',
    full_name='fileservice.Fileservice.DownloadFile',
    index=1,
    containing_service=None,
    input_type=_FILEINFO,
    output_type=_FILEDATA,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FileSearch',
    full_name='fileservice.Fileservice.FileSearch',
    index=2,
    containing_service=None,
    input_type=_FILEINFO,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ReplicateFile',
    full_name='fileservice.Fileservice.ReplicateFile',
    index=3,
    containing_service=None,
    input_type=_FILEDATA,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FileList',
    full_name='fileservice.Fileservice.FileList',
    index=4,
    containing_service=None,
    input_type=_USERINFO,
    output_type=_FILELISTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FileDelete',
    full_name='fileservice.Fileservice.FileDelete',
    index=5,
    containing_service=None,
    input_type=_FILEINFO,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateFile',
    full_name='fileservice.Fileservice.UpdateFile',
    index=6,
    containing_service=None,
    input_type=_FILEDATA,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getClusterStats',
    full_name='fileservice.Fileservice.getClusterStats',
    index=7,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_CLUSTERSTATS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getLeaderInfo',
    full_name='fileservice.Fileservice.getLeaderInfo',
    index=8,
    containing_service=None,
    input_type=_CLUSTERINFO,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='MetaDataInfo',
    full_name='fileservice.Fileservice.MetaDataInfo',
    index=9,
    containing_service=None,
    input_type=_METADATA,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FILESERVICE)

DESCRIPTOR.services_by_name['Fileservice'] = _FILESERVICE

# @@protoc_insertion_point(module_scope)
