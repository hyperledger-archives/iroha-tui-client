#!/usr/bin/env python3

from pprint import pprint
from .commands import ProtoCommandLoader, CommandWrapper, CommandPreview
from .parsers import ProtoMessageExplorer
from .message import MessageModel
from sys import exit

pc = ProtoCommandLoader()

# for _, cname, _ in pc.commands:
#   print()
#   print(cname)
#   wrapped = pc.wrapped_command_by_name(cname)
#   model = MessageModel(wrapped.unwrapped)
#   pprint(model.descriptor)

cr = pc.wrapped_command_by_name('SetAccountQuorum')


crmodel = MessageModel(cr.unwrapped)
# pprint(crmodel.descriptor)

f = '.account_id'
# crmodel.set_to(f, 'admin@test')

# crmodel.set_to('.quorum', 4)


print(crmodel.read(f))
print(cr.unwrapped.quorum)

preview = CommandPreview(cr.unwrapped)

print(preview.brief)
print(preview.full)


#####################################################################################
# pprint(crmodel.descriptor)


# pprint(pc.commands)

# ap = pc.command_message_by_name('AddPeer')

# ap.peer.address = 'someaddr'

# apmodel = MessageModel(ap)
# apmodel.set_to('.peer.address', 'anotheraddr')
# apmodel.clear('.peer.address')

# print(apmodel.read('.peer.address'))

# exit(0)

# ap2 = pc.command_message_by_name('AddPeer')

# print("'{}' '{}'".format(ap.peer.address, ap2.peer.address))

# props = ProtoMessageExplorer(ap).descriptor

# pprint(props)


# # name = input()
# name = 'CreateRole'

# saqd = pc.command_proto_descriptor_by_message_name(name)
# # print(dir(saqd))

# saq_model = ProtoMessageDescriptorParser(saqd).descriptor
# pprint(saq_model)

# # print(saqd2)

# # print(dir(saqd), saqd.fields_by_number[1])

# # saq = commands_pb2.SetAccountQuorum()
